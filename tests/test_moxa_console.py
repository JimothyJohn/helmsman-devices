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


class Diff(unittest.TestCase):
    def test_changed_lines_and_a_length_change_are_both_reported(self):
        self.assertEqual(console.diff("A=1\nB=2\n", "A=1\nB=3\n"), [("B=2", "B=3")])
        self.assertEqual(console.diff("A=1\n", "A=1\nB=2\n"), [("(1 lines)", "(2 lines)")])
        self.assertEqual(console.diff("same\r\n", "same\r\n"), [])


if __name__ == "__main__":
    unittest.main()
