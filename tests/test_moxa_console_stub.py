"""scripts/moxa-e1200-console.py over real HTTP, against a stub console on 127.0.0.1.

The stub serves what the client reads first (the front page with its cookies,
06_6.htm, an export) and records every request, so the client's own request
path is exercised end to end, not only its pure functions. It is not a model
of the device; helmsman's simulator is that.
"""

import contextlib
import http.server
import importlib.util
import io
import pathlib
import threading
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "moxa-e1200-console.py"
spec = importlib.util.spec_from_file_location("console", SCRIPT)
console = importlib.util.module_from_spec(spec)
spec.loader.exec_module(console)

EXPORT = "ioLogik E1213 Remote Ethernet I/O Server Configuration\r\n[1. Model]\r\nMOD_LOC=\r\n<END>\r\n"
PAGES = {
    "/": ("<HTML><FRAMESET></FRAMESET></HTML>", ["ChallID=4739", "MoxaPass=abc"]),
    "/06_6.htm": ('<a href="ik1213.txt">ik1213.txt</a>', []),
    "/ik1213.txt": (EXPORT, []),
}


SEEN = []  # (path, Cookie header) of every request the stub answered


class Stub(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        SEEN.append((self.path, self.headers.get("Cookie")))
        body, cookies = PAGES.get(self.path, ("", None))
        if cookies is None:
            self.send_response(404)
            self.end_headers()
            return
        data = body.encode("latin-1")
        self.send_response(200)
        for c in cookies:
            self.send_header("Set-Cookie", c)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


class OverHttp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        console.GAP_S = 0.0
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Stub)
        cls.host = f"127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        SEEN.clear()

    def test_a_console_session_starts_and_reads_the_export(self):
        c = console.Console(self.host)
        self.assertEqual(c.cookie("ChallID"), "4739")
        self.assertEqual(c.export(), EXPORT)
        paths = [p for p, _ in SEEN]
        self.assertEqual(paths, ["/", "/06_6.htm", "/ik1213.txt"], SEEN)
        # the cookies the front page set go back on every later request
        self.assertTrue(all("ChallID=4739" in (ck or "") for _, ck in SEEN[1:]), SEEN)

    def test_every_documented_command_gets_past_the_session_start(self):
        # each command's first step is Console(host); none may die there
        for argv in (["export", self.host], ["form", self.host, "nope.htm"]):
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    console.main(argv)
            except (OSError, ValueError, console.http.client.HTTPException):
                pass  # the stub has no forms; reaching the request is the point


LOGIN_TOKEN = "TOK123"  # the real console's is 39 characters, fresh per login page
LOGIN_PAGE = (
    '<HTML><FORM name=InputPassword method="post" action=home.htm onSubmit="return SetPass(this);">'
    f'<INPUT type=password name=Password><INPUT type="hidden" name="Token" value="{LOGIN_TOKEN}">'
    "<INPUT type=submit value=Submit name=Submit></FORM></HTML>"
)
SESSION = "MoxaPass=session-ok"


class Locked(Stub):
    """The same pages behind a login with the password "moxa", as the E1213 does with one set."""

    def do_GET(self):
        if SESSION not in (self.headers.get("Cookie") or ""):
            SEEN.append((self.path, "login page"))
            self.reply(LOGIN_PAGE, [])
            return
        super().do_GET()

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        form = dict(console.urllib.parse.parse_qsl(self.rfile.read(min(n, 4096)).decode("ascii")))
        SEEN.append((self.path, "POST"))
        want = console.hashlib.md5(("moxa" + LOGIN_TOKEN).encode()).hexdigest()
        if self.path == "/home.htm" and form.get("Password") == want and form.get("Token") == LOGIN_TOKEN:
            self.reply("<HTML><FRAMESET></FRAMESET></HTML>", ["ChallID=4739", SESSION])
        else:
            self.reply(LOGIN_PAGE, [])

    def reply(self, body, cookies):
        data = body.encode("latin-1")
        self.send_response(200)
        for c in cookies:
            self.send_header("Set-Cookie", c)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class BehindALogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        console.GAP_S = 0.0
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Locked)
        cls.host = f"127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        SEEN.clear()

    def test_the_right_password_logs_in_and_the_export_reads(self):
        c = console.Console(self.host, "moxa")
        self.assertEqual(c.export(), EXPORT)
        self.assertEqual(SEEN[:2], [("/", "login page"), ("/home.htm", "POST")], SEEN)

    def test_a_wrong_password_is_refused_after_one_attempt(self):
        with self.assertRaisesRegex(ValueError, "refused the password"):
            console.Console(self.host, "wrong")
        self.assertEqual([p for p, k in SEEN if k == "POST"], ["/home.htm"], SEEN)

    def test_no_password_says_which_variable_to_set_and_posts_nothing(self):
        with self.assertRaisesRegex(ValueError, "MOXA_E1200_PASSWORD"):
            console.Console(self.host, None)
        self.assertFalse([p for p, k in SEEN if k == "POST"], SEEN)

    def test_a_write_answered_by_the_login_page_is_not_repeated(self):
        c = console.Console(self.host, "moxa")
        c.jar.clear()  # the session expires between the read and the write
        SEEN.clear()
        with self.assertRaisesRegex(ValueError, "nothing written"):
            c.get("set.htm?code=41&MOD_LOC=x", retry=False)
        self.assertEqual([p for p, _ in SEEN].count("/set.htm?code=41&MOD_LOC=x"), 1, SEEN)

    def test_the_login_field_is_md5_of_password_and_token(self):
        f = dict(console.login_fields("moxa", "TOK123"))
        self.assertEqual(f["Password"], console.hashlib.md5(b"moxaTOK123").hexdigest())
        self.assertEqual((f["Token"], f["Submit"]), ("TOK123", "Submit"))
        for bad in ("x" * 25, "é", "a\nb"):
            with self.assertRaises(ValueError):
                console.login_fields(bad, "T")


if __name__ == "__main__":
    unittest.main()
