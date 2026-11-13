#!/usr/bin/env python3
"""Read and write a Moxa ioLogik E1200's settings through its web console, headless.

The console (devices/moxa/iologik-e1200-web-console.md) reads with plain GETs
and writes with a GET to set.htm carrying a page's form fields, its `code` and
the `token` the page was served with. This does what a browser does: load the
page, take its form as the browser would submit it, change only the fields
asked for, submit, then read the configuration export again and print every
line that changed.

  export HOST [FILE]                       the configuration export (ik12xx.txt)
  form HOST PAGE                           the fields PAGE's form would submit now
  set HOST PAGE KEY=VALUE ... [--dry-run]  change those fields and submit
  restart HOST                             Save/Restart: the unit reboots and applies what is staged
  import HOST FILE [--overwrite-network] [--dry-run]
                                           send an export back (the restore path); its network
                                           settings are kept OUT unless --overwrite-network
  password HOST OLD NEW [--dry-run]        change the console's password (code 7)

A checkbox is KEY=1 to tick it and KEY= to untick it. A write changes the
staged settings only: the unit applies them after `restart`. A write, a
restart and an import are never retried. Reading or writing a console that
HAS a password is not supported: how it asks for a login has not been seen
(firmware 3.1 ships without one; 3.3 and later default to "moxa").

Standard library only, Python 3.9 or later (macOS: Apple's /usr/bin/python3
from an agent session, for Local Network privacy).
"""

import hashlib
import html.parser
import http.client
import http.cookiejar
import re
import socket
import sys
import time
import urllib.parse
import urllib.request

GAP_S = 0.3  # the console drops a connection that comes right after the last one
TIMEOUT_S = 10
MAX_BYTES = 1 << 20

# Fields a page's script disables (so a browser does not submit them) while
# the checkbox named beside them is unticked: 04_1.htm's checkWDValue().
DISABLED_UNLESS = {"IdleTime": "EnableIDLE", "WDTime": "EnableWD"}


class Console:
    def __init__(self, host):
        if not re.fullmatch(r"[A-Za-z0-9.:-]{1,255}", host):
            raise ValueError(f"not a host: {host!r}")
        self.host = host
        self.base = f"http://{host}/"
        self.jar = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        self.get("")  # the session cookies the frameset sets (ChallID, MoxaPass)

    def cookie(self, name):
        for c in self.jar:
            if c.name == name:
                return c.value
        raise ValueError(f"the console set no {name} cookie")

    def post(self, path, body, content_type):
        """One POST, never retried (an import is a write)."""
        time.sleep(GAP_S)
        req = urllib.request.Request(self.base + path, data=body, headers={"Content-Type": content_type})
        with self.op.open(req, timeout=TIMEOUT_S * 3) as r:
            return r.read(MAX_BYTES).decode("latin-1")

    def http_ok(self):
        try:
            self.get("06_3.htm", retry=False)
            return True
        except (OSError, http.client.HTTPException):
            return False

    def modbus_ok(self):
        try:
            with socket.create_connection((self.host, 502), timeout=0.5):
                return True
        except OSError:
            return False

    def back_after_reboot(self, deadline_s=120.0):
        """Seconds until the unit is really back after a reboot it was asked for, or None."""
        watch = RebootWatch()
        t0 = time.monotonic()
        while time.monotonic() - t0 < deadline_s:
            if watch.feed(self.http_ok(), self.modbus_ok()):
                return time.monotonic() - t0
            time.sleep(0.3)
        return None

    def get(self, path, retry=True):
        time.sleep(GAP_S)
        try:
            with self.op.open(self.base + path, timeout=TIMEOUT_S) as r:
                body = r.read(MAX_BYTES + 1)
        except (OSError, http.client.HTTPException):
            if not retry:
                raise
            time.sleep(1.0)
            return self.get(path, retry=False)
        if len(body) > MAX_BYTES:
            raise ValueError(f"{path}: more than {MAX_BYTES} bytes")
        return body.decode("latin-1")

    def export(self):
        """The configuration export: the overview page names the model (E1213 serves ik1213.txt)."""
        page = self.get("06_6.htm")
        m = re.search(r'href="(ik12[0-9]{2}\.txt)"', page)
        if not m:
            raise ValueError("06_6.htm names no ik12xx.txt export")
        return self.get(m.group(1))


class RebootWatch:
    """Whether an E1200 is back after a reboot, from repeated probes of HTTP and Modbus.

    Measured on the E1213 (2026-11-12, twice): HTTP goes down about 1 s after the
    request and answers again at 11 s while Modbus is still down, then goes down a
    second time and is back for good at 20 s together with Modbus. So "HTTP
    answers" is not enough: back means HTTP answered after it was seen down AND
    Modbus TCP accepts. (EtherNet/IP is left out: it can be switched off.)
    """

    def __init__(self):
        self.went_down = False

    def feed(self, http_ok, modbus_ok):
        if not http_ok:
            self.went_down = True
            return False
        return self.went_down and modbus_ok


class Form(html.parser.HTMLParser):
    """The first form on a page with a `code` field, as a browser would submit it."""

    def __init__(self):
        super().__init__()
        self.depth, self.forms, self.cur, self.select = 0, [], None, None

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "form":
            self.cur = []
            self.forms.append(self.cur)
        elif self.cur is None:
            return
        elif tag == "input":
            t = a.get("type", "text").lower()
            name = a.get("name")
            if not name or t in ("button", "file", "image", "reset"):
                return
            if t in ("checkbox", "radio") and "checked" not in a:
                self.cur.append([name, None, t])  # known, not submitted
                return
            if t == "submit" and name != "Submit":
                return  # other submit buttons (Clear_Safe_Flag) act on their own
            self.cur.append([name, a.get("value", ""), t])
        elif tag == "select":
            self.select = [a.get("name"), None, "select"]
            self.cur.append(self.select)
        elif tag == "option" and self.select is not None and (self.select[1] is None or "selected" in a):
            self.select[1] = a.get("value", "")

    def handle_endtag(self, tag):
        if tag == "form":
            self.cur = None
        elif tag == "select":
            self.select = None


def form_of(page):
    f = Form()
    f.feed(page)
    for fields in f.forms:
        if any(n == "code" for n, _, _ in fields):
            return fields
    raise ValueError("the page has no settings form (no code= field)")


def submitted(fields):
    """The (name, value) pairs a browser sends: unticked boxes and script-disabled fields left out."""
    ticked = {n for n, v, t in fields if t in ("checkbox", "radio") and v is not None}
    out = []
    for n, v, _ in fields:
        if v is None:
            continue
        if n in DISABLED_UNLESS and DISABLED_UNLESS[n] not in ticked:
            continue
        out.append((n, v))
    return out


def apply(fields, changes):
    known = {n for n, _, _ in fields}
    for key, value in changes.items():
        if key not in known:
            raise ValueError(f"{key}: not a field of this form ({', '.join(sorted(known))})")
        if key in ("token", "code"):
            raise ValueError(f"{key}: set by the page, not by hand")
        for f in fields:
            if f[0] == key:
                if f[2] == "checkbox":
                    f[1] = "1" if value not in ("", "0") else None
                else:
                    f[1] = value
    return fields


def diff(before, after):
    b, a = before.splitlines(), after.splitlines()
    # by index, not zip(strict=...): that keyword needs 3.10, and this runs on Apple's 3.9
    rows = [(b[i].strip(), a[i].strip()) for i in range(min(len(b), len(a))) if b[i] != a[i]]
    if len(b) != len(a):
        rows.append((f"({len(b)} lines)", f"({len(a)} lines)"))
    return rows


def printable(s, most, what):
    if len(s) > most or any(not (32 <= ord(ch) <= 126) for ch in s):
        raise ValueError(f"{what}: at most {most} printable ASCII characters")
    return s


def password_fields(challenge, old, new):
    """OldPwd, NewPwd and ChallID as 07.htm's ChangePassword() computes them.

    ChallID is MD5 of the ChallID cookie; OldPwd MD5 of the old password; NewPwd
    MD5(cookie) XORed byte by byte with the new password's ASCII codes (the rest
    of the 16 bytes unchanged), all lowercase hex. Checked against Moxa's own
    md5.js and Xor() (tests/test_moxa_console.py, VENDOR_VECTORS).
    """
    printable(old, 24, "old password")  # OldPassword maxlength="24"
    printable(new, 16, "new password")  # NewPassword maxlength="16"
    chall = hashlib.md5(challenge.encode("ascii")).digest()
    mixed = bytes(b ^ ord(new[i]) if i < len(new) else b for i, b in enumerate(chall))
    return {
        "OldPwd": hashlib.md5(old.encode("ascii")).hexdigest(),
        "NewPwd": mixed.hex(),
        "ChallID": chall.hex(),
    }


BOUNDARY = "----helmsman-moxa-import"


def multipart(fields, file_field, file_name, file_bytes, boundary=BOUNDARY):
    """A multipart/form-data body: the text fields in order, then the file."""
    if boundary.encode() in file_bytes:
        raise ValueError("the file contains the multipart boundary")
    out = []
    for name, value in fields:
        out.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode(
                "latin-1"
            )
        )
    out.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; filename="{file_name}"\r\n'
        "Content-Type: text/plain\r\n\r\n".encode("latin-1")
    )
    out.append(file_bytes + f"\r\n--{boundary}--\r\n".encode("latin-1"))
    return b"".join(out), f"multipart/form-data; boundary={boundary}"


def import_fields(token, overwrite_network):
    """What 06_5.htm's form sends, except the network-overwrite box: off unless asked."""
    fields = [("token", token)]
    if overwrite_network:
        fields.append(("NetConfig_OverWrite", "1"))
    fields.append(("import", "Import"))
    return fields


def token_of(page):
    m = re.search(r'name="token"\s+value="([^"]*)"', page)
    if not m:
        raise ValueError("the page carries no token")
    return m.group(1)


def restart(c):
    """Save/Restart (09.htm's form: GET set_ok.htm with an empty token), then wait for the console."""
    t0 = time.monotonic()
    try:
        c.get("set_ok.htm?token=", retry=False)
    except (OSError, http.client.HTTPException):
        pass  # the unit may drop the connection as it goes down
    if c.back_after_reboot() is None:
        raise ValueError("the unit was not back (HTTP after a drop, and Modbus) within 120 s of the restart")
    return time.monotonic() - t0


def main(argv):
    if len(argv) < 2 or argv[0] not in ("export", "form", "set", "restart", "import", "password"):
        print(__doc__)
        return 2
    cmd, host, rest = argv[0], argv[1], argv[2:]
    c = Console(host)
    if cmd == "export":
        text = c.export()
        if rest:
            with open(rest[0], "w", encoding="latin-1", newline="") as f:
                f.write(text)
            print(f"wrote {rest[0]}: {len(text.splitlines())} lines")
        else:
            sys.stdout.write(text)
        return 0
    if cmd == "restart":
        print("GET /set_ok.htm?token= (Save/Restart)")
        print(f"the unit is back {restart(c):.1f} s after the request")
        return 0
    if cmd == "import":
        flags = {x for x in rest if x.startswith("--")}
        args = [x for x in rest if not x.startswith("--")]
        if len(args) != 1 or flags - {"--overwrite-network", "--dry-run"}:
            print("import HOST FILE [--overwrite-network] [--dry-run]", file=sys.stderr)
            return 2
        with open(args[0], "rb") as f:
            data = f.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES or not data.startswith(b"ioLogik E12"):
            raise ValueError(f"{args[0]}: not an ioLogik E1200 export")
        fields = import_fields(token_of(c.get("06_5.htm")), "--overwrite-network" in flags)
        shown = [(n, "<token>" if n == "token" else v) for n, v in fields]
        print(f"POST /06_5_1.htm multipart: {shown} + importfile ({len(data)} bytes)")
        if "--dry-run" in flags:
            return 0
        body, ctype = multipart(fields, "importfile", "ik12xx.txt", data)
        t0 = time.monotonic()
        reply = c.post("06_5_1.htm", body, ctype)
        print("reply:", " ".join(re.sub(r"<[^>]*>", " ", reply).split())[:300])
        if "--overwrite-network" in flags:
            print("not waiting: the imported network settings may have moved the unit to another address")
            return 0
        # the import reboots the unit ("imported and restart successfully", 2026-11-12)
        if c.back_after_reboot() is None:
            raise ValueError("the unit was not back within 120 s of the import")
        print(f"the unit is back {time.monotonic() - t0:.1f} s after the import")
        return 0
    if cmd == "password":
        dry = "--dry-run" in rest
        args = [x for x in rest if x != "--dry-run"]
        if len(args) != 2:
            print("password HOST OLD NEW [--dry-run]", file=sys.stderr)
            return 2
        fields = form_of(c.get("07.htm"))
        computed = password_fields(c.cookie("ChallID"), args[0], args[1])
        changes = dict(computed, OldPassword="", NewPassword="", ReTypePassword="")
        query = urllib.parse.urlencode(submitted(apply(fields, changes)))
        shown = re.sub(r"(token|OldPwd|NewPwd)=[^&]*", r"\1=<hidden>", query)
        print(f"GET /set.htm?{shown}")
        if dry:
            return 0
        reply = c.get("set.htm?" + query, retry=False)
        ok = "Configuration Complete" in reply
        print(
            f"reply: {'Configuration Complete' if ok else ' '.join(re.sub(r'<[^>]*>', ' ', reply).split())[:300]}"
        )
        return 0 if ok else 1
    if not rest or not re.fullmatch(r"[0-9a-zA-Z_]{1,32}\.htm", rest[0]):
        print("PAGE is a console page such as 04_1.htm", file=sys.stderr)
        return 2
    page = rest[0]
    fields = form_of(c.get(page))
    if cmd == "form":
        for n, v in submitted(fields):
            print(f"{n}={'<token>' if n == 'token' else v}")
        return 0
    dry = "--dry-run" in rest
    pairs = [x for x in rest[1:] if x != "--dry-run"]
    if not pairs or any("=" not in x for x in pairs):
        print("set needs KEY=VALUE ...", file=sys.stderr)
        return 2
    changes = dict(x.split("=", 1) for x in pairs)
    query = urllib.parse.urlencode(submitted(apply(fields, changes)))
    shown = re.sub(r"token=[^&]*", "token=<token>", query)
    print(f"GET /set.htm?{shown}")
    if dry:
        return 0
    before = c.export()
    reply = c.get("set.htm?" + query, retry=False)
    ok = "Configuration Complete" in reply
    after = c.export()
    rows = diff(before, after)
    print(f"reply: {'Configuration Complete' if ok else 'not the success page'}; {len(rows)} line(s) changed")
    for x, y in rows:
        print(f"  - {x}\n  + {y}")
    if "Save/Restart" in reply:
        print("staged: the unit applies it after Save/Restart (`restart HOST`)")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except ValueError as e:
        writes = ("set", "import", "password")
        print(f"refused: {e}" if sys.argv[1:2] and sys.argv[1] in writes else f"error: {e}", file=sys.stderr)
        sys.exit(2)
