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


PHOTO = '[device.photo]\nurl = "{url}"\npage = "{page}"\nseen = {seen}\n'
GOOD = {
    "url": "https://vendor.example/img/m.png",
    "page": "https://vendor.example/product/m",
    "seen": "2026-11-16",
}


def with_photo(**kw) -> dict:
    return entry(PHOTO.format(**{**GOOD, **kw}))


class Photo(unittest.TestCase):
    """A page puts photo.url in an <img src> and photo.page in an <a href>."""

    def test_photo_carries_link_and_credit(self):
        self.assertEqual(
            with_photo()["photo"],
            {"url": GOOD["url"], "page": GOOD["page"]},
        )

    def test_vendor_paths_with_brackets_and_queries_kept(self):
        url = "https://cdn.example/PIS/ADAM-6050/Product%20-%20Photo(Main)/a.png?w=576&h=576"
        self.assertEqual(with_photo(url=url)["photo"]["url"], url)

    def test_no_photo_no_key(self):
        self.assertNotIn("photo", entry(""))

    def test_hostile_links_refused(self):
        for bad in (
            "http://vendor.example/m.png",
            "javascript:alert(1)",
            "data:image/png;base64,AAAA",
            "//vendor.example/m.png",
            "https://",
            "https:///m.png",
            'https://v.example/a\\" onerror=\\"alert(1)',  # TOML \\" is a quote
            "https://v.example/a'b",
            "https://v.example/<svg>",
            "https://v.example/a b.png",
            "https://v.example/a\\u0000b",
            "https://v.example/a\\nb",
            "https://v.example/a{b}",
            "https://v.example/caf\u00e9.png",
            "https://v.example/" + "a" * 400,
        ):
            for field in ("url", "page"):
                with self.subTest(field=field, bad=bad), self.assertRaises(SystemExit):
                    with_photo(**{field: bad})

    def test_seen_is_a_date(self):
        for bad in ('"last week"', '"2026-02-30"', "2026"):
            with self.subTest(seen=bad), self.assertRaises(SystemExit):
                entry(PHOTO.format(**{**GOOD, "seen": bad}))

    def test_missing_parts_refused(self):
        for toml in (
            '[device.photo]\nurl = "https://v.example/m.png"\nseen = 2026-11-16\n',
            '[device.photo]\npage = "https://v.example/m"\nseen = 2026-11-16\n',
            '[device.photo]\nurl = "https://v.example/m.png"\npage = "https://v.example/m"\n',
            'photo = "https://v.example/m.png"\n',
        ):
            with self.subTest(toml=toml), self.assertRaises(SystemExit):
                entry(toml)


if __name__ == "__main__":
    unittest.main()


SHA = "5f0ffe695186c8d23c55f6435b9a9021bc0fa0b06678a1b22111da485d093b38"


def with_eds(name: str) -> dict:
    return entry(
        '[protocols.enip]\ndriver = "enip-io"\n'
        f'eds = {{ name = {name!r}, size = 1, sha256 = "{SHA}" }}\n'.replace("'", '"')
    )


class FileNames(unittest.TestCase):
    """A box takes a file name of letters, digits, `.`, `_` and `-` only
    (helmsman-project devlib `file_ok`) and refuses the whole index for one
    that is not: one EDS named with spaces took the library off every box
    (2026-11-18). The index never carries such a name."""

    def test_a_name_with_a_space_is_refused(self):
        with self.assertRaises(SystemExit) as e:
            with_eds("BNI EIP-302-105-Z015.eds")
        self.assertIn("not a file name", str(e.exception))

    def test_other_names_a_box_refuses_are_refused(self):
        for bad in ("../x.eds", "a/b.eds", "..", "xé.eds", "a+b.eds", "x" * 121 + ".eds"):
            with self.subTest(bad=bad), self.assertRaises(SystemExit):
                with_eds(bad)

    def test_an_underscored_name_is_taken(self):
        self.assertEqual(
            with_eds("BNI_EIP-302-105-Z015.eds")["protocols"]["enip"]["eds"]["name"],
            "BNI_EIP-302-105-Z015.eds",
        )
