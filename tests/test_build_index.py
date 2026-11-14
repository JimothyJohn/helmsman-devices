"""scripts/build-index.py: the catalog fields a page shows (channels, checked_on, firmware).

A box reads index.json by key and ignores the rest (helmsman-project's
devlib), so these fields are additive for every box in the field. They are
public data a page renders: bounded, printable, and a date is a date.
"""

import importlib.util
import pathlib
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "build-index.py"
spec = importlib.util.spec_from_file_location("build_index", SCRIPT)
bi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bi)

BASE = '[device]\nvendor = "V"\nmodel = "M"\nkind = "remote-io"\n'


def entry(device_extra: str) -> dict:
    root = pathlib.Path(tempfile.mkdtemp())
    f = root / "devices" / "v" / "m"
    f.mkdir(parents=True)
    (f / "device.toml").write_text(BASE + device_extra)
    old = bi.ROOT
    bi.ROOT = root
    try:
        return bi.entry(f)
    finally:
        bi.ROOT = old


class Catalog(unittest.TestCase):
    def test_checked_device_carries_its_check(self):
        e = entry('channels = "8 DI, 4 DO"\nchecked_on = "2026-11-02"\nfirmware = "V3.1 Build19110615"\n')
        self.assertEqual(
            (e["channels"], e["checked_on"], e["firmware"]),
            ("8 DI, 4 DO", "2026-11-02", "V3.1 Build19110615"),
        )

    def test_draft_has_no_check(self):
        e = entry('channels = "8 DI"\n')
        self.assertNotIn("checked_on", e)
        self.assertNotIn("firmware", e)

    def test_a_toml_date_is_a_date_too(self):
        self.assertEqual(entry("checked_on = 2026-11-02\n")["checked_on"], "2026-11-02")

    def test_bad_values_refused(self):
        for extra in (
            'checked_on = "2026-13-40"\n',
            'checked_on = "yesterday"\n',
            'checked_on = "2026-11-02T10:00"\n',
            "checked_on = 20261102\n",
            'channels = "<script>alert(1)</script>' + "x" * 200 + '"\n',
            'channels = "a\\nb"\n',
            'firmware = "\\u001b[31mred"\n',
            'channels = ""\n',
        ):
            with self.subTest(extra=extra), self.assertRaises(SystemExit):
                entry(extra)

    def test_markup_is_kept_as_text(self):
        """The index stays data; a page must escape it (it does: textContent)."""
        self.assertEqual(entry('channels = "<b>8</b> DI"\n')["channels"], "<b>8</b> DI")


if __name__ == "__main__":
    unittest.main()
