#!/usr/bin/env python3 -I
"""Fetch the vendor documents a collect/<vendor>.toml names, safely, into a hash-keyed store.

The candidates file says which URL holds which document for which library
folder (the collect-docs skill writes it from a web search; a person may
too). This script downloads each one, checks it is the kind of file it
claims to be, hashes it, keeps it under cache/sha256/<hex> (ignored by git),
optionally copies it to the private S3 bucket named by HELMSMAN_DOCS_BUCKET,
and records what it got in collect/<vendor>.lock.json, which is committed:
name, size, SHA-256, the URL after redirects, when. Vendor files themselves
are never committed (README, Vendor files).

Fetching is held to these rules, every hop of every redirect included:
https on port 443 only, no userinfo; the host's every address must be a
global unicast one, and the connection goes to the address that was checked
(no second lookup to rebind); robots.txt is honoured (RFC 9309: 4xx allows,
5xx or unreachable disallows); one request a second per host; a size cap;
at most 5 redirects, never to http.

Usage: python3 -I scripts/docs-fetch.py collect/<vendor>.toml [--refresh] [--only FOLDER]
  --refresh      download again even when the store has the file; report a changed hash
  --only FOLDER  only the documents for that library folder

A document is looked for in the local store, then the bucket, then the URL.
Standard library only (tomllib needs Python 3.11); S3 goes through the aws CLI.
"""

import datetime
import hashlib
import http.client
import io
import ipaddress
import json
import os
import pathlib
import re
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import tomllib
import urllib.parse
import urllib.robotparser
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORMAT = "helmsman-devices-collect 1"
LOCK_FORMAT = "helmsman-devices-collect-lock 1"
FOLDER = re.compile(r"devices/[a-z0-9][a-z0-9_.-]{0,63}/[a-z0-9][a-z0-9_.-]{0,63}")
USER_AGENT = "helmsman-devices-collect/1 (+https://github.com/JimothyJohn/helmsman-devices)"
MAX_BYTES = 64 * 1024 * 1024
ROBOTS_MAX_BYTES = 512 * 1024
MAX_REDIRECTS = 5
TIMEOUT_S = 30.0
GAP_S = 1.0
ZIP_MAX_MEMBERS = 2000
ZIP_MAX_TOTAL = 256 * 1024 * 1024
KINDS = {
    # kind: the file types it may arrive as
    "eds": ("eds", "zip"),
    "gsdml": ("xml", "zip"),
    "esi": ("xml", "zip"),
    "manual": ("pdf",),
    "release-notes": ("pdf",),
    "register-map": ("pdf",),
    "datasheet": ("pdf",),
    "archive": ("zip",),
}


class Refused(Exception):
    """A fetch the rules do not allow, or a file that is not what it claims to be."""


# --- the address guard -----------------------------------------------------


def check_url(url: str) -> urllib.parse.SplitResult:
    """The URL's shape: https, port 443, a host name, no userinfo. Raises Refused."""
    if not isinstance(url, str) or len(url) > 2048 or any(ord(c) < 33 or ord(c) == 127 for c in url):
        raise Refused("url: printable, no spaces, at most 2048 characters")
    u = urllib.parse.urlsplit(url)
    if u.scheme != "https":
        raise Refused(f"url: https only, got {u.scheme or 'none'}")
    if "@" in u.netloc:
        raise Refused("url: no userinfo")
    try:
        port = u.port
    except ValueError as e:
        raise Refused(f"url: bad port: {e}") from None
    if port not in (None, 443):
        raise Refused("url: port 443 only")
    if not u.hostname:
        raise Refused("url: no host")
    return u


def global_address(addr: str) -> bool:
    try:
        ip = ipaddress.ip_address(addr.split("%", 1)[0])
    except ValueError:
        return False
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
        ip = ip.ipv4_mapped
    return ip.is_global and not ip.is_multicast


def resolve(host: str) -> list[str]:
    """Every address the system resolver gives for host (port 443, TCP)."""
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except (socket.gaierror, UnicodeError) as e:
        raise Refused(f"{host}: does not resolve: {e}") from None
    return sorted({i[4][0] for i in infos})


def vetted_address(host: str, resolver=resolve) -> str:
    """An address of host to connect to, once every one of them is global. Raises Refused."""
    addrs = resolver(host)
    if not addrs:
        raise Refused(f"{host}: no address")
    bad = [a for a in addrs if not global_address(a)]
    if bad:
        raise Refused(f"{host}: resolves to a non-global address ({', '.join(bad)})")
    return addrs[0]


class PinnedHTTPS(http.client.HTTPSConnection):
    """HTTPS to an address already checked; the certificate is checked against the host name."""

    def __init__(self, host: str, address: str, timeout: float):
        super().__init__(host, 443, timeout=timeout, context=ssl.create_default_context())
        self._address = address

    def connect(self):
        sock = socket.create_connection((self._address, 443), self.timeout)
        self.sock = self._context.wrap_socket(sock, server_hostname=self.host)


def https_connection(host: str, address: str, timeout: float):
    return PinnedHTTPS(host, address, timeout)


# --- the fetcher -----------------------------------------------------------


class Fetcher:
    """GETs under the rules above. resolver, connect, clock and sleep are the seams tests use."""

    def __init__(
        self,
        resolver=resolve,
        connect=https_connection,
        clock=time.monotonic,
        sleep=time.sleep,
        max_bytes=MAX_BYTES,
    ):
        self.resolver = resolver
        self.connect = connect
        self.clock = clock
        self.sleep = sleep
        self.max_bytes = max_bytes
        self.last = {}  # host -> clock() of its last request
        self.robots = {}  # host -> RobotFileParser, or False for "disallow all"

    def _pace(self, host: str):
        then = self.last.get(host)
        if then is not None:
            wait = GAP_S - (self.clock() - then)
            if wait > 0:
                self.sleep(wait)
        self.last[host] = self.clock()

    def _get_once(self, u: urllib.parse.SplitResult, limit: int):
        host = u.hostname
        address = vetted_address(host, self.resolver)
        self._pace(host)
        conn = self.connect(host, address, TIMEOUT_S)
        try:
            path = urllib.parse.urlunsplit(("", "", u.path or "/", u.query, ""))
            conn.request(
                "GET",
                path,
                headers={
                    "Host": host,
                    "User-Agent": USER_AGENT,
                    "Accept": "*/*",
                    "Accept-Encoding": "identity",
                },
            )
            r = conn.getresponse()
            if r.status in (301, 302, 303, 307, 308):
                return r.status, r.getheader("Location"), b"", r.getheader("Content-Type", "")
            length = r.getheader("Content-Length")
            if length is not None and length.strip().isdigit() and int(length) > limit:
                raise Refused(f"{host}: {length} bytes is over the {limit}-byte cap")
            buf = io.BytesIO()
            while True:
                chunk = r.read(65536)
                if not chunk:
                    break
                buf.write(chunk)
                if buf.tell() > limit:
                    raise Refused(f"{host}: more than the {limit}-byte cap")
            return r.status, None, buf.getvalue(), r.getheader("Content-Type", "")
        except (OSError, http.client.HTTPException) as e:
            raise Refused(f"{host}: {type(e).__name__}: {e}") from None
        finally:
            conn.close()

    def get(self, url: str, limit: int | None = None, robots: bool = True):
        """(final URL, status, body, content type), following redirects under the rules."""
        limit = self.max_bytes if limit is None else limit
        for _ in range(MAX_REDIRECTS + 1):
            u = check_url(url)
            vetted_address(u.hostname, self.resolver)  # the address first, so a refusal names it
            if robots and not self.allowed(u):
                raise Refused(f"{u.hostname}: robots.txt disallows {u.path or '/'}")
            status, location, body, ctype = self._get_once(u, limit)
            if location is None:
                return url, status, body, ctype
            url = urllib.parse.urljoin(url, location)
        raise Refused(f"more than {MAX_REDIRECTS} redirects")

    def allowed(self, u: urllib.parse.SplitResult) -> bool:
        host = u.hostname
        if host not in self.robots:
            try:
                _, status, body, _ = self.get(f"https://{host}/robots.txt", ROBOTS_MAX_BYTES, robots=False)
            except Refused:
                status, body = 503, b""
            if 200 <= status < 300:
                rp = urllib.robotparser.RobotFileParser()
                rp.parse(body.decode("utf-8", "replace").splitlines())
                self.robots[host] = rp
            elif 400 <= status < 500:
                self.robots[host] = None  # no robots.txt: everything allowed
            else:
                self.robots[host] = False  # unreachable: nothing allowed (RFC 9309 2.3.1.4)
        rp = self.robots[host]
        if rp is None:
            return True
        if rp is False:
            return False
        return rp.can_fetch(USER_AGENT, urllib.parse.urlunsplit(u))


# --- what a file is --------------------------------------------------------


def sniff(data: bytes) -> str:
    """pdf | zip | xml | eds | html | unknown, from the bytes alone."""
    head = data[:4096]
    if head.startswith(b"%PDF-"):
        return "pdf"
    if head.startswith(b"PK\x03\x04"):
        return "zip"
    text = head.lstrip(b"\xef\xbb\xbf \t\r\n").lower()
    if text.startswith((b"<!doctype html", b"<html")) or b"<html" in text[:512]:
        return "html"
    if text.startswith(b"<?xml"):
        return "xml"
    if b"\x00" not in head:
        low = data[:65536].lower()
        if b"[file]" in low and b"[device]" in low:
            return "eds"
    return "unknown"


def zip_members(data: bytes) -> list[tuple[str, bytes]]:
    """(name, bytes) of every file in an archive, within the caps. Names are only labels here."""
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
        infos = [i for i in z.infolist() if not i.is_dir()]
        if len(infos) > ZIP_MAX_MEMBERS:
            raise Refused(f"archive: {len(infos)} members, over {ZIP_MAX_MEMBERS}")
        total, out = 0, []
        for i in infos:
            if i.flag_bits & 0x1:
                raise Refused(f"archive: {i.filename!r} is encrypted")
            with z.open(i) as f:
                body = f.read(ZIP_MAX_TOTAL - total + 1)
            total += len(body)
            if total > ZIP_MAX_TOTAL:
                raise Refused(f"archive: more than {ZIP_MAX_TOTAL} bytes unpacked")
            out.append((i.filename, body))
        return out
    except (zipfile.BadZipFile, zipfile.LargeZipFile, NotImplementedError, EOFError, OSError) as e:
        raise Refused(f"archive: {e}") from None


def check_kind(kind: str, data: bytes) -> str:
    """The file's type, once it is one the document's kind allows. Raises Refused."""
    got = sniff(data)
    if got not in KINDS[kind]:
        raise Refused(f"a {kind} should be {' or '.join(KINDS[kind])}, the bytes are {got}")
    return got


# --- the store -------------------------------------------------------------


class Store:
    """cache/sha256/<hex> on disk, mirrored to s3://BUCKET/sha256/<hex> when a bucket is set."""

    def __init__(self, root: pathlib.Path, bucket: str | None = None, aws: str = "aws"):
        self.dir = root / "sha256"
        self.bucket = bucket
        self.aws = aws

    def path(self, sha: str) -> pathlib.Path:
        if len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            raise ValueError(f"not a sha256: {sha!r}")
        return self.dir / sha

    def get(self, sha: str) -> bytes | None:
        p = self.path(sha)
        if p.is_file():
            data = p.read_bytes()
            if hashlib.sha256(data).hexdigest() == sha:
                return data
        if self.bucket:
            with tempfile.TemporaryDirectory() as d:
                tmp = pathlib.Path(d) / "f"
                r = subprocess.run(
                    [
                        self.aws,
                        "s3",
                        "cp",
                        "--only-show-errors",
                        f"s3://{self.bucket}/sha256/{sha}",
                        str(tmp),
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if r.returncode == 0 and tmp.is_file():
                    data = tmp.read_bytes()
                    if hashlib.sha256(data).hexdigest() == sha:
                        self._write(sha, data)
                        return data
        return None

    def _write(self, sha: str, data: bytes):
        p = self.path(sha)
        p.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=p.parent)
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, p)

    def put(self, sha: str, data: bytes, url: str = "") -> bool:
        """Keep data; True when the bucket got a new copy."""
        if hashlib.sha256(data).hexdigest() != sha:
            raise ValueError("data does not match its hash")
        self._write(sha, data)
        if not self.bucket:
            return False
        key = f"sha256/{sha}"
        head = subprocess.run(
            [self.aws, "s3api", "head-object", "--bucket", self.bucket, "--key", key],
            check=False,
            capture_output=True,
            text=True,
        )
        if head.returncode == 0:
            return False
        r = subprocess.run(
            [
                self.aws,
                "s3",
                "cp",
                "--only-show-errors",
                "--sse",
                "AES256",
                str(self.path(sha)),
                f"s3://{self.bucket}/{key}",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            raise Refused(f"s3 upload of {sha[:12]}: {r.stderr.strip()[:300]}")
        return True


# --- candidates and the lock -----------------------------------------------


def load_candidates(path: pathlib.Path) -> dict:
    try:
        t = tomllib.loads(path.read_text())
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as e:
        raise SystemExit(f"{path}: {e}") from None
    if t.get("format") != FORMAT:
        raise SystemExit(f"{path}: format must be {FORMAT!r}")
    if not isinstance(t.get("vendor"), str) or not t["vendor"]:
        raise SystemExit(f'{path}: vendor = "..." is required')
    docs = t.get("doc", [])
    seen = set()
    for n, d in enumerate(docs, 1):
        where = f"{path}: doc {n}"
        if "folder" in d:
            d["folders"] = [d.pop("folder")]
        folders = d.get("folders")
        if not isinstance(folders, list) or not folders or not all(isinstance(f, str) for f in folders):
            raise SystemExit(f'{where}: folder = "..." or folders = [...] is required')
        d["folders"] = sorted(set(folders))
        for key in ("kind", "url", "title", "found"):
            if not isinstance(d.get(key), str) or not d[key]:
                raise SystemExit(f"{where}: {key} is required")
        if d["url"] in seen:
            raise SystemExit(f"{where}: {d['url']} is listed twice; give one doc its folders = [...]")
        seen.add(d["url"])
        if d["kind"] not in KINDS:
            raise SystemExit(f"{where}: kind must be one of {', '.join(sorted(KINDS))}")
        for f in d["folders"]:
            if not FOLDER.fullmatch(f):
                raise SystemExit(f"{where}: folder {f!r} must be devices/<vendor>/<model>, a-z 0-9 . _ -")
        try:
            check_url(d["url"])
        except Refused as e:
            raise SystemExit(f"{where}: {e}") from None
    return t


def lock_path(candidates: pathlib.Path) -> pathlib.Path:
    return candidates.with_name(candidates.name.removesuffix(".toml") + ".lock.json")


def load_lock(path: pathlib.Path) -> dict:
    if not path.exists():
        return {"format": LOCK_FORMAT, "docs": {}}
    lock = json.loads(path.read_text())
    if lock.get("format") != LOCK_FORMAT:
        raise SystemExit(f"{path}: format must be {LOCK_FORMAT!r}")
    return lock


def write_lock(path: pathlib.Path, lock: dict):
    lock["docs"] = dict(sorted(lock["docs"].items()))
    path.write_text(json.dumps(lock, indent=1, sort_keys=True, ensure_ascii=False) + "\n")


def file_name(final_url: str, sha: str, kind: str, typ: str) -> str:
    base = pathlib.PurePosixPath(urllib.parse.unquote(urllib.parse.urlsplit(final_url).path)).name
    base = "".join(c for c in base if c.isalnum() or c in "._-+")[:120]
    return base or f"{kind}-{sha[:12]}.{typ}"


def collect_one(doc: dict, entry: dict | None, fetcher: Fetcher, store: Store, refresh: bool, now: str):
    """(lock entry, what happened): fetched | stored | changed | refused: why."""
    if entry and not refresh and store.get(entry["sha256"]) is not None:
        return entry, "stored"
    try:
        final, status, data, ctype = fetcher.get(doc["url"])
        if status != 200:
            raise Refused(f"HTTP {status}")
        typ = check_kind(doc["kind"], data)
        members = []
        if typ == "zip":
            for name, body in zip_members(data):
                mtype = sniff(body)
                if mtype in ("eds", "xml", "pdf"):
                    msha = hashlib.sha256(body).hexdigest()
                    store.put(msha, body)
                    members.append({"name": name[:200], "sha256": msha, "size": len(body), "type": mtype})
            if doc["kind"] in ("eds", "gsdml", "esi") and not any(
                m["type"] == ("eds" if doc["kind"] == "eds" else "xml") for m in members
            ):
                raise Refused(f"the archive holds no {doc['kind']} file")
    except Refused as e:
        return entry, f"refused: {e}"
    sha = hashlib.sha256(data).hexdigest()
    store.put(sha, data, final)
    new = {
        "folders": doc["folders"],
        "kind": doc["kind"],
        "title": doc["title"],
        "name": file_name(final, sha, doc["kind"], typ),
        "size": len(data),
        "sha256": sha,
        "type": typ,
        "final_url": final,
        "content_type": ctype[:100],
        "retrieved": now,
    }
    if members:
        new["members"] = sorted(members, key=lambda m: m["name"])
    if doc.get("terms"):
        new["terms"] = doc["terms"]
    what = "fetched" if entry is None or entry["sha256"] == sha else f"changed (was {entry['sha256'][:12]})"
    return new, what


def main(argv: list[str]) -> int:
    args = list(argv)
    refresh = "--refresh" in args
    if refresh:
        args.remove("--refresh")
    only = None
    if "--only" in args:
        i = args.index("--only")
        if i + 1 >= len(args):
            raise SystemExit("--only needs a folder")
        only = args[i + 1]
        del args[i : i + 2]
    if len(args) != 1:
        print("usage: docs-fetch.py collect/<vendor>.toml [--refresh] [--only FOLDER]", file=sys.stderr)
        return 2
    cpath = pathlib.Path(args[0])
    cand = load_candidates(cpath)
    lpath = lock_path(cpath)
    lock = load_lock(lpath)
    bucket = os.environ.get("HELMSMAN_DOCS_BUCKET") or None
    if bucket and not shutil.which("aws"):
        raise SystemExit("HELMSMAN_DOCS_BUCKET is set and the aws CLI is not on PATH")
    store = Store(ROOT / "cache", bucket)
    fetcher = Fetcher()
    now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    failed = 0
    for doc in cand.get("doc", []):
        if only and only not in doc["folders"]:
            continue
        entry, what = collect_one(doc, lock["docs"].get(doc["url"]), fetcher, store, refresh, now)
        if entry is not None:
            lock["docs"][doc["url"]] = entry
        if what.startswith("refused"):
            failed += 1
        sha = entry["sha256"][:12] if entry else "-" * 12
        fs = doc["folders"]
        where = fs[0] if len(fs) == 1 else f"{len(fs)} folders ({fs[0]}, ...)"
        print(f"{what.split(':')[0]:8} {sha} {doc['kind']:13} {where}  {what.partition(': ')[2]}")
    write_lock(lpath, lock)
    print(
        f"{lpath.relative_to(ROOT) if lpath.is_relative_to(ROOT) else lpath}: {len(lock['docs'])} document(s)"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
