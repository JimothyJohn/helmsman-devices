"""scripts/moxa-e1200-console.py without a device: what it would send, on pages written here.

The pages are synthetic, shaped like the E1213's (firmware 3.1) forms; no
Moxa page is in the repository. Run: python3 -I -m unittest discover -s tests
"""

import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "moxa-e1200-console.py"
spec = importlib.util.spec_from_file_location("console", SCRIPT)
console = importlib.util.module_from_spec(spec)
spec.loader.exec_module(console)

GENERAL = """<HTML><BODY><FORM name="network" method="get" action="set.htm">
<INPUT type="hidden" name="token" value="T0K3N"/>
<INPUT type="text" name="MOD_DESC" value="">
<INPUT type="text" name="MOD_LOC" value="">
<INPUT type="checkbox" name="EnableIDLE" value="1" CHECKED>
<INPUT type="text" name="IdleTime" value="60">
<INPUT type="checkbox" name="EnableWD" value="1">
<INPUT type="text" name="WDTime" value="0">
<INPUT type="checkbox" name="EnableSafeModeAutoClear" value="1">
<INPUT type="submit" value="Submit" name="Submit">
<Input type="hidden" name="code" value="41">
</FORM>
<form id="LocateForm" action="set_locate.htm" method="get"><input type='hidden' name="Locate"></input></form>
</BODY></HTML>"""

SAFE = """<FORM name="P2P_DO_SAFEMODE_FORM" method="GET" action="set.htm">
<SELECT name="SetSM00"><OPTION value="0" selected>Off</OPTION><OPTION value="1">On</OPTION></SELECT>
<SELECT name="SetSM01"><OPTION value="0">Off</OPTION><OPTION value="2" selected>Hold</OPTION></SELECT>
<INPUT type="hidden" name="token" value="T"/><INPUT type="hidden" name="code" value="116">
<INPUT type="submit" value="Submit" name="Submit">
<INPUT type="submit" name="Clear_Safe_Flag1" value="Clear_Safe_Flag">
</FORM>"""


def sent(page, **changes):
    return console.submitted(console.apply(console.form_of(page), changes))


class Browser(unittest.TestCase):
    def test_the_general_form_as_a_browser_submits_it(self):
        # the request the E1213 accepted on 2026-11-12, field for field and in order
        self.assertEqual(
            sent(GENERAL),
            [
                ("token", "T0K3N"),
                ("MOD_DESC", ""),
                ("MOD_LOC", ""),
                ("EnableIDLE", "1"),
                ("IdleTime", "60"),
                ("Submit", "Submit"),
                ("code", "41"),
            ],
        )

    def test_one_field_changes_and_nothing_else(self):
        before, after = sent(GENERAL), sent(GENERAL, MOD_LOC="helmsman bench")
        self.assertEqual([a for a in after if a not in before], [("MOD_LOC", "helmsman bench")])

    def test_ticking_the_watchdog_sends_its_time_unticking_idle_drops_its_time(self):
        s = dict(sent(GENERAL, EnableWD="1", WDTime="5", EnableIDLE=""))
        self.assertEqual((s.get("EnableWD"), s.get("WDTime")), ("1", "5"))
        self.assertNotIn("EnableIDLE", s)
        self.assertNotIn("IdleTime", s)

    def test_selects_send_their_selected_option_and_other_submit_buttons_stay_out(self):
        s = sent(SAFE)
        self.assertIn(("SetSM00", "0"), s)
        self.assertIn(("SetSM01", "2"), s)
        self.assertNotIn("Clear_Safe_Flag1", dict(s))

    def test_the_settings_form_is_found_past_a_form_without_code(self):
        page = '<form action="x"><input name="a" value="1"></form>' + GENERAL
        self.assertEqual(dict(sent(page))["code"], "41")


class Refusals(unittest.TestCase):
    def test_an_unknown_field_is_refused(self):
        with self.assertRaises(ValueError):
            sent(GENERAL, NotAField="1")

    def test_token_and_code_cannot_be_set_by_hand(self):
        for k in ("token", "code"):
            with self.assertRaises(ValueError):
                sent(GENERAL, **{k: "99"})

    def test_a_page_without_a_settings_form_is_refused(self):
        for page in ("", "<html>", "<form><input name=a></form>", "<<<>>>&#x;", "\x00" * 100):
            with self.assertRaises(ValueError):
                console.form_of(page)

    def test_hostile_markup_does_not_break_the_parser(self):
        page = GENERAL.replace(
            '<INPUT type="text" name="MOD_DESC" value="">',
            '<INPUT type="text" name="MOD_DESC" value="a&b=c&token=EVIL"><input><select><option></select><!-- -->',
        )
        q = console.urllib.parse.urlencode(sent(page))
        self.assertIn("MOD_DESC=a%26b%3Dc%26token%3DEVIL", q)
        self.assertEqual(console.urllib.parse.parse_qs(q)["token"], ["T0K3N"])

    def test_a_host_is_a_host(self):
        for h in ("", "a/b", "x y", "1.2.3.4/../", "h@evil", "a" * 300):
            with self.assertRaises(ValueError):
                console.Console(h)


class Fuzz(unittest.TestCase):
    """Seeded: the same 2000 pages every run."""

    PIECES = (
        "<form>",
        "</form>",
        "<FORM action=set.htm>",
        '<input name="code" value="41">',
        "<input type=checkbox name=c checked>",
        "<select name=s>",
        "<option value=1 selected>",
        "</select>",
        '<input name="token" value="T">',
        "<",
        ">",
        "&",
        '"',
        "'",
        "<!--",
        "-->",
        "\x00",
        "é",
        "퟿",
        "<input>",
        "<input name=>",
        "<script>",
        "</script>",
        "x" * 50,
    )

    def test_any_page_gives_a_form_or_a_refusal_never_a_crash(self):
        import random

        rng = random.Random(20261112)
        for _ in range(2000):
            page = "".join(rng.choice(self.PIECES) for _ in range(rng.randint(0, 40)))
            try:
                fields = console.form_of(page)
            except ValueError:
                continue
            pairs = console.submitted(fields)
            self.assertTrue(
                any(n == "code" for n, _ in pairs) or any(n == "code" for n, _, _ in fields), page
            )
            console.urllib.parse.urlencode(pairs)  # always encodable


# Computed by running Moxa's own md5.js and 07.htm's Xor() under node on
# 2026-11-12: (ChallID cookie, password) -> (MD5(cookie), MD5(password), NewPwd).
VENDOR_VECTORS = [
    (
        "",
        "moxa",
        "d41d8cd98f00b204e9800998ecf8427e",
        "d3bff8450106a52369b8b4dbca7b1b16",
        "b972f4b88f00b204e9800998ecf8427e",
    ),
    (
        "4739",
        "",
        "f3507289cfdc8c9ae93f4098111a13f9",
        "d41d8cd98f00b204e9800998ecf8427e",
        "f3507289cfdc8c9ae93f4098111a13f9",
    ),
    (
        "4739",
        "moxa",
        "f3507289cfdc8c9ae93f4098111a13f9",
        "d3bff8450106a52369b8b4dbca7b1b16",
        "9e3f0ae8cfdc8c9ae93f4098111a13f9",
    ),
    (
        "12345",
        "Abc!~ 09",
        "827ccb0eea8a706c4c34a16891f84e7b",
        "54832070cac8fae13e9debcb61ec8ecf",
        "c31ea82f94aa40554c34a16891f84e7b",
    ),
    (
        "65535",
        "sixteen-chars-xx",
        "3c9b5f1cd6a030bcb7bed9eac80589fb",
        "db5dbdd94d28c99f28055567d9500bd9",
        "4ff22768b3c55e91d4d6b898bb28f183",
    ),
    (
        "0",
        "0123456789",
        "cfcd208495d565ef66e7dff9f98764da",
        "781e5e245d69b566979b86e28d23f2c7",
        "fffc12b7a1e053d85ededff9f98764da",
    ),
]


class Password(unittest.TestCase):
    def test_the_fields_match_the_vendors_own_javascript(self):
        for chall, pw, md5_chall, md5_pw, newpwd in VENDOR_VECTORS:
            # the vector's password is both the old one (OldPwd) and the new one (NewPwd)
            f = console.password_fields(chall, pw, pw)
            self.assertEqual(
                (f["ChallID"], f["OldPwd"], f["NewPwd"]), (md5_chall, md5_pw, newpwd), (chall, pw)
            )

    def test_long_or_unprintable_passwords_are_refused(self):
        for old, new in (("x" * 25, "a"), ("a", "x" * 17), ("a", "é"), ("a", "a\nb"), ("\x00", "a")):
            with self.assertRaises(ValueError, msg=(old, new)):
                console.password_fields("1", old, new)

    def test_the_change_password_form_sends_the_hashes_and_empties_the_plain_fields(self):
        page = """<FORM method="GET" action="set.htm"><INPUT type="hidden" name="token" value="T"/>
<INPUT type="password" name="OldPassword"><INPUT type="password" name="NewPassword">
<INPUT type="password" name="ReTypePassword"><INPUT type="hidden" name="OldPwd" value="1">
<INPUT type="hidden" name="NewPwd" value="1"><INPUT type="hidden" name="ChallID" value="1">
<INPUT type="hidden" name="code" value="7"><INPUT type="submit" value="Submit" name="Submit"></FORM>"""
        changes = dict(
            console.password_fields("4739", "moxa", "moxa"), OldPassword="", NewPassword="", ReTypePassword=""
        )
        s = dict(sent(page, **changes))
        self.assertEqual((s["OldPassword"], s["NewPassword"], s["ReTypePassword"]), ("", "", ""))
        self.assertEqual(s["NewPwd"], "9e3f0ae8cfdc8c9ae93f4098111a13f9")
        self.assertNotIn("moxa", console.urllib.parse.urlencode(list(s.items())))


class Import(unittest.TestCase):
    def test_network_settings_stay_out_unless_asked(self):
        self.assertEqual(console.import_fields("T", False), [("token", "T"), ("import", "Import")])
        self.assertIn(("NetConfig_OverWrite", "1"), console.import_fields("T", True))

    def test_the_multipart_body_has_each_field_then_the_file(self):
        body, ctype = console.multipart(
            [("token", "T"), ("import", "Import")],
            "importfile",
            "ik.txt",
            b"ioLogik E1213\r\nA=1\r\n",
            boundary="B",
        )
        self.assertEqual(ctype, "multipart/form-data; boundary=B")
        self.assertEqual(
            body,
            b'--B\r\nContent-Disposition: form-data; name="token"\r\n\r\nT\r\n'
            b'--B\r\nContent-Disposition: form-data; name="import"\r\n\r\nImport\r\n'
            b'--B\r\nContent-Disposition: form-data; name="importfile"; filename="ik.txt"\r\nContent-Type: text/plain\r\n\r\n'
            b"ioLogik E1213\r\nA=1\r\n\r\n--B--\r\n",
        )

    def test_a_file_holding_the_boundary_is_refused(self):
        with self.assertRaises(ValueError):
            console.multipart([], "f", "x", b"a --B b", boundary="B")

    def test_the_token_is_read_from_the_page(self):
        self.assertEqual(console.token_of('<INPUT type="hidden" name="token" value="67wq"/>'), "67wq")
        with self.assertRaises(ValueError):
            console.token_of("<form></form>")


class Diff(unittest.TestCase):
    def test_changed_lines_and_a_length_change_are_both_reported(self):
        self.assertEqual(console.diff("A=1\nB=2\n", "A=1\nB=3\n"), [("B=2", "B=3")])
        self.assertEqual(console.diff("A=1\n", "A=1\nB=2\n"), [("(1 lines)", "(2 lines)")])
        self.assertEqual(console.diff("same\r\n", "same\r\n"), [])


if __name__ == "__main__":
    unittest.main()
