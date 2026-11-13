#!/usr/bin/env python3
"""Read and write a Moxa ioLogik E1200's settings through its web console, headless.

The console (devices/moxa/iologik-e1200-web-console.md) reads with plain GETs
and writes with a GET to set.htm carrying a page's form fields, its `code` and
the `token` the page was served with. This does what a browser does: load the
page, take its form as the browser would submit it, change only the fields
asked for, submit, then read the configuration export again and print every
line that changed.

  export HOST [FILE]                      the configuration export (ik12xx.txt)
  form HOST PAGE                          the fields PAGE's form would submit now
  set HOST PAGE KEY=VALUE ... [--dry-run] change those fields and submit

A checkbox is KEY=1 to tick it and KEY= to untick it. A write changes the
staged settings only: the unit applies them after Save/Restart, which this
does not do. A write is never retried. The console must have no password
set (firmware 3.1 ships without one; 3.3 and later default to "moxa", which
this does not handle yet).

Standard library only, Python 3.9 or later (macOS: Apple's /usr/bin/python3
from an agent session, for Local Network privacy).
"""

import html.parser
import http.client
import http.cookiejar
import re
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
        self.base = f"http://{host}/"
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.get("")  # the session cookies the frameset sets (ChallID, MoxaPass)

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


def main(argv):
    if len(argv) < 2 or argv[0] not in ("export", "form", "set"):
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
        print("staged: the unit applies it after Save/Restart (09.htm), which this did not do")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except ValueError as e:
        print(f"refused, nothing sent: {e}" if "set" in sys.argv[1:2] else f"error: {e}", file=sys.stderr)
        sys.exit(2)
