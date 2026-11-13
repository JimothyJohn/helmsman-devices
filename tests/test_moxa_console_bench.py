"""scripts/moxa-e1200-console.py against a real ioLogik E1200, opt-in.

MOXA_E1200_HOST=192.168.3.60 /usr/bin/python3 -I -m unittest discover -s tests

Reads the export and the forms, then writes the Server Location and puts it
back (a staged change, no Save/Restart). Without the variable every test here
is skipped: CI has no unit. A unit with a Server Location already set is
refused rather than overwritten.
"""

import importlib.util
import os
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "moxa-e1200-console.py"
spec = importlib.util.spec_from_file_location("console", SCRIPT)
console = importlib.util.module_from_spec(spec)
spec.loader.exec_module(console)
HOST = os.environ.get("MOXA_E1200_HOST")
MARK = "helmsman bench test"


@unittest.skipUnless(HOST, "MOXA_E1200_HOST names no unit")
class OnTheBench(unittest.TestCase):
    def setUp(self):
        self.c = console.Console(HOST)

    def test_the_export_names_the_firmware_and_its_sections(self):
        text = self.c.export()
        self.assertIn("[System Information]", text, text[:500])
        self.assertIn("FW_Ver=", text, text[:500])
        self.assertIn("[9. Protocol Enable]", text, text[-500:])

    def test_the_general_form_carries_a_fresh_token_and_code_41(self):
        a = dict(console.submitted(console.form_of(self.c.get("04_1.htm"))))
        b = dict(console.submitted(console.form_of(self.c.get("04_1.htm"))))
        self.assertEqual(a["code"], "41", a)
        self.assertTrue(a["token"] and b["token"], (a, b))

    def test_a_write_changes_one_line_and_its_undo_restores_it(self):
        before = self.c.export()
        loc = [x for x in before.splitlines() if x.startswith("MOD_LOC=")]
        self.assertEqual(loc, ["MOD_LOC="], f"refusing to overwrite a set Server Location: {loc}")

        def write(value):
            fields = console.apply(console.form_of(self.c.get("04_1.htm")), {"MOD_LOC": value})
            q = console.urllib.parse.urlencode(console.submitted(fields))
            reply = self.c.get("set.htm?" + q, retry=False)
            self.assertIn("Configuration Complete", reply, reply[:800])

        write(MARK)
        try:
            mid = self.c.export()
            self.assertEqual(console.diff(before, mid), [("MOD_LOC=", f"MOD_LOC={MARK}")])
        finally:
            write("")
        self.assertEqual(console.diff(before, self.c.export()), [])


if __name__ == "__main__":
    unittest.main()
