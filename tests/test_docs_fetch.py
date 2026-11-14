"""scripts/docs-fetch.py: the address guard, the fetch rules over real HTTP, file checks, the store.

The fetcher's two network seams are swapped: names resolve through a table
(so no test depends on DNS), and the connection goes to a stub server on
127.0.0.1 over plain HTTP, whatever address was vetted. Everything between,
the guard, robots.txt, redirects, caps, pacing, the type checks and the
lock, is the script's own code running against real sockets.
"""

import contextlib
import hashlib
import http.client
import http.server
import importlib.util
import io
import ipaddress
import json
import pathlib
import random
import tempfile
import threading
import unittest
import zipfile

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "docs-fetch.py"
spec = importlib.util.spec_from_file_location("docs_fetch", SCRIPT)
df = importlib.util.module_from_spec(spec)
spec.loader.exec_module(df)

PDF = b"%PDF-1.7\n" + b"x" * 2000 + b"\n%%EOF\n"
EDS = b'[File]\r\n DescText = "t";\r\n[Device]\r\n VendCode = 48;\r\n ProdCode = 1;\r\n'


def zip_of(members: dict) -> bytes:
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        for name, body in members.items():
            z.writestr(name, body)
    return b.getvalue()


# host -> path -> (status, headers, body); a callable body is called with the handler
SITES = {}
SEEN = []  # (Host header, path, User-Agent)


class Stub(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        host = self.headers.get("Host", "")
        SEEN.append((host, self.path, self.headers.get("User-Agent")))
        status, headers, body = SITES.get(host, {}).get(self.path, (404, {}, b"no"))
        if callable(body):
            body(self)
            return
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        if "Content-Length" not in headers:
            self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


NAMES = {
    "vendor.example": ["93.184.216.34"],
    "mirror.example": ["151.101.1.1"],
    "evil.example": ["10.0.0.7"],
    "mixed.example": ["93.184.216.35", "127.0.0.1"],
    "meta.example": ["169.254.169.254"],
}


def table_resolver(host):
    if host not in NAMES:
        raise df.Refused(f"{host}: does not resolve")
    return NAMES[host]


class Clock:
    def __init__(self):
        self.t = 1000.0
        self.slept = []

    def now(self):
        return self.t

    def sleep(self, s):
        self.slept.append(s)
        self.t += s


class Guard(unittest.TestCase):
    def test_url_shapes_refused(self):
        for url in [
            "http://vendor.example/a.pdf",
            "file:///etc/passwd",
            "ftp://vendor.example/a.pdf",
            "https://user:pw@vendor.example/a.pdf",
            "https://vendor.example@evil.example/a.pdf",
            "https://vendor.example:8443/a.pdf",
            "https://vendor.example:0/a.pdf",
            "https://vendor.example:99999/a.pdf",
            "https:///a.pdf",
            "https://vendor.example/a b.pdf",
            "https://vendor.example/a\r\nX-Injected: 1",
            "https://vendor.example/\x00",
            "https://vendor.example/" + "a" * 2100,
            "",
        ]:
            with self.subTest(url=url), self.assertRaises(df.Refused):
                df.check_url(url)

    def test_url_shapes_allowed(self):
        for url in [
            "https://vendor.example/a.pdf",
            "https://vendor.example:443/x?y=1",
            "https://VENDOR.example",
        ]:
            df.check_url(url)

    def test_non_global_addresses(self):
        for a in [
            "127.0.0.1",
            "10.1.2.3",
            "172.16.0.1",
            "192.168.3.60",
            "169.254.169.254",
            "100.64.0.1",
            "0.0.0.0",
            "255.255.255.255",
            "224.0.0.1",
            "::1",
            "::",
            "fe80::1",
            "fc00::1",
            "::ffff:127.0.0.1",
            "::ffff:10.0.0.1",
            "ff02::1",
            "2130706433",
            "0x7f000001",
            "not-an-ip",
        ]:
            with self.subTest(a=a):
                self.assertFalse(df.global_address(a))

    def test_global_property(self):
        """Random IPv4 addresses: global exactly when outside every special-purpose block."""
        special = [
            ipaddress.ip_network(n)
            for n in [
                "0.0.0.0/8",
                "10.0.0.0/8",
                "100.64.0.0/10",
                "127.0.0.0/8",
                "169.254.0.0/16",
                "172.16.0.0/12",
                "192.0.0.0/24",
                "192.0.2.0/24",
                "192.168.0.0/16",
                "198.18.0.0/15",
                "198.51.100.0/24",
                "203.0.113.0/24",
                "224.0.0.0/3",
            ]
        ]
        exceptions = {ipaddress.ip_address("192.0.0.9"), ipaddress.ip_address("192.0.0.10")}
        rng = random.Random(1213)
        for _ in range(20000):
            ip = ipaddress.IPv4Address(rng.getrandbits(32))
            expect = ip in exceptions or not any(ip in n for n in special)
            self.assertEqual(df.global_address(str(ip)), expect, str(ip))
            mapped = f"::ffff:{ip}"
            self.assertEqual(df.global_address(mapped), expect, mapped)

    def test_one_bad_address_refuses_the_host(self):
        with self.assertRaises(df.Refused):
            df.vetted_address("mixed.example", table_resolver)
        with self.assertRaises(df.Refused):
            df.vetted_address("meta.example", table_resolver)
        self.assertEqual(df.vetted_address("vendor.example", table_resolver), "93.184.216.34")

    def test_store_paths_are_hashes_only(self):
        s = df.Store(pathlib.Path(tempfile.mkdtemp()))
        for bad in ["../" + "a" * 61, "A" * 64, "a" * 63, "a" * 63 + "/", "a" * 63 + "\x00"]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                s.path(bad)


class Sniff(unittest.TestCase):
    def test_types(self):
        self.assertEqual(df.sniff(PDF), "pdf")
        self.assertEqual(df.sniff(zip_of({"a.eds": EDS})), "zip")
        self.assertEqual(df.sniff(EDS), "eds")
        self.assertEqual(df.sniff(b"\xef\xbb\xbf<?xml version='1.0'?><ISO15745Profile/>"), "xml")
        self.assertEqual(df.sniff(b"<!DOCTYPE html><html>login</html>"), "html")
        self.assertEqual(df.sniff(b"\n\n  <HTML><body>404</body>"), "html")
        self.assertEqual(df.sniff(b"<?xml version='1.0'?>\n<html xmlns='x'>"), "html")
        self.assertEqual(df.sniff(b"[File]\n[Device]\x00"), "unknown")
        self.assertEqual(df.sniff(b""), "unknown")

    def test_kind_mismatch_refused(self):
        with self.assertRaises(df.Refused):
            df.check_kind("manual", b"<html>please log in</html>")
        with self.assertRaises(df.Refused):
            df.check_kind("eds", PDF)
        self.assertEqual(df.check_kind("eds", EDS), "eds")

    def test_archive_caps(self):
        old = df.ZIP_MAX_TOTAL
        df.ZIP_MAX_TOTAL = 10_000
        try:
            with self.assertRaises(df.Refused):
                df.zip_members(zip_of({"bomb.eds": b"\0" * 50_000}))
        finally:
            df.ZIP_MAX_TOTAL = old
        old = df.ZIP_MAX_MEMBERS
        df.ZIP_MAX_MEMBERS = 3
        try:
            with self.assertRaises(df.Refused):
                df.zip_members(zip_of({f"{i}.txt": b"x" for i in range(4)}))
        finally:
            df.ZIP_MAX_MEMBERS = old
        with self.assertRaises(df.Refused):
            df.zip_members(b"PK\x03\x04garbage")

    def test_archive_names_are_labels(self):
        m = df.zip_members(zip_of({"../../etc/evil.eds": EDS, "/abs/x.eds": EDS}))
        self.assertEqual(sorted(n for n, _ in m), ["../../etc/evil.eds", "/abs/x.eds"])


class OverHttp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Stub)
        cls.port = cls.server.server_address[1]
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        SITES.clear()
        SEEN.clear()
        SITES["vendor.example"] = {"/robots.txt": (200, {}, b"User-agent: *\nDisallow: /private/\n")}
        SITES["mirror.example"] = {"/robots.txt": (404, {}, b"")}
        self.clock = Clock()
        self.connects = []
        self.fetcher = df.Fetcher(
            resolver=table_resolver,
            connect=self._connect,
            clock=self.clock.now,
            sleep=self.clock.sleep,
            max_bytes=100_000,
        )
        self.dir = pathlib.Path(tempfile.mkdtemp())
        self.store = df.Store(self.dir)

    def _connect(self, host, address, timeout):
        self.connects.append((host, address))
        return http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)

    def doc(self, url, kind="manual"):
        return {"folders": ["devices/v/m"], "kind": kind, "url": url, "title": "T", "found": "test"}

    def collect(self, url, kind="manual", entry=None, refresh=False):
        return df.collect_one(
            self.doc(url, kind), entry, self.fetcher, self.store, refresh, "2026-11-14T00:00:00Z"
        )

    def test_fetch_records_and_stores(self):
        SITES["vendor.example"]["/m.pdf"] = (200, {"Content-Type": "application/pdf"}, PDF)
        e, what = self.collect("https://vendor.example/m.pdf")
        self.assertEqual(what, "fetched", e)
        self.assertEqual(e["sha256"], hashlib.sha256(PDF).hexdigest())
        self.assertEqual((e["size"], e["type"], e["name"]), (len(PDF), "pdf", "m.pdf"))
        self.assertEqual(self.store.get(e["sha256"]), PDF)
        self.assertTrue(all(ua == df.USER_AGENT for _, _, ua in SEEN), SEEN)
        self.assertEqual({a for _, a in self.connects}, {"93.184.216.34"})

    def test_stored_document_is_not_fetched_again(self):
        SITES["vendor.example"]["/m.pdf"] = (200, {}, PDF)
        e, _ = self.collect("https://vendor.example/m.pdf")
        SEEN.clear()
        e2, what = self.collect("https://vendor.example/m.pdf", entry=e)
        self.assertEqual((what, e2), ("stored", e))
        self.assertEqual(SEEN, [])

    def test_refresh_reports_a_changed_file(self):
        SITES["vendor.example"]["/m.pdf"] = (200, {}, PDF)
        e, _ = self.collect("https://vendor.example/m.pdf")
        SITES["vendor.example"]["/m.pdf"] = (200, {}, PDF + b"v2")
        e2, what = self.collect("https://vendor.example/m.pdf", entry=e, refresh=True)
        self.assertTrue(what.startswith("changed (was "), what)
        self.assertNotEqual(e2["sha256"], e["sha256"])

    def test_a_tampered_store_file_is_fetched_again(self):
        SITES["vendor.example"]["/m.pdf"] = (200, {}, PDF)
        e, _ = self.collect("https://vendor.example/m.pdf")
        self.store.path(e["sha256"]).write_bytes(b"%PDF-tampered")
        _, what = self.collect("https://vendor.example/m.pdf", entry=e)
        self.assertEqual(what, "fetched")
        self.assertEqual(self.store.get(e["sha256"]), PDF)

    def test_html_instead_of_a_manual_is_refused(self):
        SITES["vendor.example"]["/m.pdf"] = (
            200,
            {"Content-Type": "application/pdf"},
            b"<html>Sign in</html>",
        )
        e, what = self.collect("https://vendor.example/m.pdf")
        self.assertIsNone(e)
        self.assertIn("the bytes are html", what)

    def test_not_found_is_refused(self):
        e, what = self.collect("https://vendor.example/missing.pdf")
        self.assertEqual((e, what), (None, "refused: HTTP 404"))

    def test_redirect_to_a_private_address_is_never_connected(self):
        SITES["vendor.example"]["/m.pdf"] = (302, {"Location": "https://evil.example/m.pdf"}, b"")
        e, what = self.collect("https://vendor.example/m.pdf")
        self.assertIsNone(e)
        self.assertIn("non-global", what)
        self.assertNotIn("evil.example", [h for h, _ in self.connects])

    def test_redirect_to_http_is_refused(self):
        SITES["vendor.example"]["/m.pdf"] = (301, {"Location": "http://vendor.example/m.pdf"}, b"")
        _, what = self.collect("https://vendor.example/m.pdf")
        self.assertIn("https only", what)

    def test_redirect_to_another_site_follows_its_robots(self):
        SITES["vendor.example"]["/m.pdf"] = (302, {"Location": "https://mirror.example/files/m.pdf"}, b"")
        SITES["mirror.example"]["/files/m.pdf"] = (200, {}, PDF)
        e, what = self.collect("https://vendor.example/m.pdf")
        self.assertEqual(what, "fetched", what)
        self.assertEqual(e["final_url"], "https://mirror.example/files/m.pdf")
        self.assertIn(("mirror.example", "/robots.txt", df.USER_AGENT), SEEN)

    def test_redirect_loop_is_capped(self):
        SITES["vendor.example"]["/a"] = (302, {"Location": "/b"}, b"")
        SITES["vendor.example"]["/b"] = (302, {"Location": "/a"}, b"")
        _, what = self.collect("https://vendor.example/a")
        self.assertIn("redirects", what)
        self.assertLessEqual(len([p for _, p, _ in SEEN if p in ("/a", "/b")]), df.MAX_REDIRECTS + 1)

    def test_declared_length_over_the_cap(self):
        SITES["vendor.example"]["/big.pdf"] = (200, {"Content-Length": "200000"}, PDF)
        _, what = self.collect("https://vendor.example/big.pdf")
        self.assertIn("cap", what)

    def test_streamed_body_over_the_cap(self):
        def endless(h):
            h.send_response(200)
            h.send_header("Connection", "close")
            h.end_headers()
            h.wfile.write(b"%PDF-1.7\n")
            with contextlib.suppress(OSError):
                for _ in range(40):
                    h.wfile.write(b"y" * 8192)
            h.close_connection = True

        SITES["vendor.example"]["/stream.pdf"] = (200, {}, endless)
        _, what = self.collect("https://vendor.example/stream.pdf")
        self.assertIn("cap", what)

    def test_robots_disallow_is_honoured(self):
        SITES["vendor.example"]["/private/m.pdf"] = (200, {}, PDF)
        _, what = self.collect("https://vendor.example/private/m.pdf")
        self.assertIn("robots.txt disallows", what)
        self.assertNotIn("/private/m.pdf", [p for _, p, _ in SEEN])

    def test_unreachable_robots_disallows_everything(self):
        SITES["vendor.example"]["/robots.txt"] = (503, {}, b"busy")
        SITES["vendor.example"]["/m.pdf"] = (200, {}, PDF)
        _, what = self.collect("https://vendor.example/m.pdf")
        self.assertIn("robots.txt disallows", what)

    def test_hosts_are_paced(self):
        SITES["vendor.example"]["/a.pdf"] = (200, {}, PDF)
        SITES["vendor.example"]["/b.pdf"] = (200, {}, PDF + b"b")
        self.collect("https://vendor.example/a.pdf")
        self.collect("https://vendor.example/b.pdf")
        self.assertEqual(len(self.clock.slept), 2, self.clock.slept)  # robots -> a, a -> b
        self.assertTrue(all(abs(s - df.GAP_S) < 1e-9 for s in self.clock.slept), self.clock.slept)

    def test_zipped_eds_records_its_members(self):
        z = zip_of({"pkg/dev.eds": EDS, "pkg/icon.ico": b"\x00\x00\x01\x00", "pkg/manual.pdf": PDF})
        SITES["vendor.example"]["/eds.zip"] = (200, {}, z)
        e, what = self.collect("https://vendor.example/eds.zip", kind="eds")
        self.assertEqual(what, "fetched", what)
        self.assertEqual(
            [(m["name"], m["type"]) for m in e["members"]],
            [("pkg/dev.eds", "eds"), ("pkg/manual.pdf", "pdf")],
        )
        self.assertEqual(self.store.get(hashlib.sha256(EDS).hexdigest()), EDS)

    def test_zip_without_an_eds_is_refused(self):
        SITES["vendor.example"]["/eds.zip"] = (200, {}, zip_of({"readme.txt": b"hello"}))
        _, what = self.collect("https://vendor.example/eds.zip", kind="eds")
        self.assertIn("holds no eds", what)


class Candidates(unittest.TestCase):
    def write(self, body):
        p = pathlib.Path(tempfile.mkdtemp()) / "v.toml"
        p.write_text(body)
        return p

    HEAD = 'format = "helmsman-devices-collect 1"\nvendor = "V"\n'
    DOC = '[[doc]]\nfolder = "{f}"\nkind = "{k}"\nurl = "{u}"\ntitle = "T"\nfound = "s"\n'

    def test_bad_entries(self):
        for f, k, u in [
            ("devices/../../etc", "manual", "https://a.example/x"),
            ("devices/v/.git", "manual", "https://a.example/x"),
            ("devices/v", "manual", "https://a.example/x"),
            ("other/v/m", "manual", "https://a.example/x"),
            ("devices/v/m", "firmware", "https://a.example/x"),
            ("devices/v/m", "manual", "http://a.example/x"),
            ("devices/v/m\n", "manual", "https://a.example/x"),
            ("devices/v/m\\n", "manual", "https://a.example/x"),
            ("devices/V/m", "manual", "https://a.example/x"),
            ("devices/v/m%2f..", "manual", "https://a.example/x"),
        ]:
            with self.subTest(f=f, k=k, u=u), self.assertRaises(SystemExit):
                df.load_candidates(self.write(self.HEAD + self.DOC.format(f=f, k=k, u=u)))

    def test_a_url_listed_twice_is_refused(self):
        doc = self.DOC.format(f="devices/v/m", k="eds", u="https://a.example/x")
        with self.assertRaises(SystemExit):
            df.load_candidates(self.write(self.HEAD + doc + doc.replace("devices/v/m", "devices/v/n")))

    def test_folders_list(self):
        body = self.HEAD + self.DOC.format(f="devices/v/m", k="eds", u="https://a.example/x").replace(
            'folder = "devices/v/m"', 'folders = ["devices/v/n", "devices/v/m", "devices/v/m"]'
        )
        self.assertEqual(
            df.load_candidates(self.write(body))["doc"][0]["folders"], ["devices/v/m", "devices/v/n"]
        )

    def test_wrong_format(self):
        with self.assertRaises(SystemExit):
            df.load_candidates(self.write('format = "x"\nvendor = "V"\n'))

    def test_lock_is_deterministic(self):
        d = pathlib.Path(tempfile.mkdtemp())
        lock = {"format": df.LOCK_FORMAT, "docs": {"https://b": {"z": 1, "a": 2}, "https://a": {"k": 1}}}
        df.write_lock(d / "l.json", lock)
        first = (d / "l.json").read_text()
        df.write_lock(d / "l.json", json.loads(first))
        self.assertEqual(first, (d / "l.json").read_text())
        self.assertLess(first.index("https://a"), first.index("https://b"))


if __name__ == "__main__":
    unittest.main()
