"""scripts/build-index.py: the catalog fields a page shows (channels, checked_on, firmware).

A box reads index.json by key and ignores the rest (helmsman-project's
devlib), so these fields are additive for every box in the field. They are
public data a page renders: bounded, printable, and a date is a date.
"""

import importlib.util
import pathlib
import tempfile
import unittest
from types import MappingProxyType

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


def build(folders: dict, *argv) -> tuple:
    """Run main() over a scratch library; (exit code, index, CATALOG.md text)."""
    import contextlib
    import io
    import json
    import sys

    root = pathlib.Path(tempfile.mkdtemp())
    for rel, toml in folders.items():
        f = root / "devices" / rel
        f.mkdir(parents=True)
        (f / "device.toml").write_text(toml)
    old_root, old_argv = bi.ROOT, sys.argv
    bi.ROOT, sys.argv = root, ["build-index.py"]
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as err:
            bi.main()
            sys.argv = ["build-index.py", *argv]
            code = bi.main() if argv else 0
        return (
            code,
            json.loads((root / "index.json").read_text()),
            (root / "CATALOG.md").read_text(),
            root,
            err,
        )
    finally:
        bi.ROOT, sys.argv = old_root, old_argv


def device(model: str, extra: str = "", kind: str = "remote-io") -> str:
    return f'[device]\nvendor = "V"\nmodel = "{model}"\nkind = "{kind}"\n{extra}'


class Categories(unittest.TestCase):
    """[device] category: the shelf in CATALOG.md and what find.py filters by."""

    def test_a_category_is_carried(self):
        self.assertEqual(entry('category = "io-block"\n')["category"], "io-block")

    def test_an_unknown_category_is_refused(self):
        for extra in (
            'category = "blocks"\n',
            'category = ""\n',
            "category = 3\n",
            'category = "unsorted"\n',
        ):
            with self.subTest(extra=extra), self.assertRaises(SystemExit):
                entry(extra)

    def test_a_draft_without_one_is_unsorted_not_guessed(self):
        self.assertEqual(entry("")["category"], "unsorted")
        self.assertEqual(entry('[protocols.enip]\ndriver = "enip-io"\n')["category"], "unsorted")

    def test_a_wired_sensor_without_one_is_a_sensor(self):
        root = pathlib.Path(tempfile.mkdtemp())
        f = root / "devices" / "v" / "m"
        f.mkdir(parents=True)
        (f / "device.toml").write_text(
            '[device]\nvendor = "V"\nmodel = "M"\nkind = "sensor"\n[wired]\nsio = true\n'
        )
        old, bi.ROOT = bi.ROOT, root
        try:
            self.assertEqual(bi.entry(f)["category"], "sensor")
        finally:
            bi.ROOT = old

    def test_the_index_names_only_the_categories_in_use_in_their_order(self):
        _, index, _, _, _ = build(
            {
                "v/a": device("A", 'category = "drive"\n', "drive"),
                "v/b": device("B", 'category = "io-block"\n'),
                "v/c": device("C"),
            }
        )
        self.assertEqual([c["id"] for c in index["categories"]], ["io-block", "drive", "unsorted"])
        self.assertEqual(index["format"], "helmsman-devices-index 1")
        self.assertEqual([d["category"] for d in index["devices"]], ["drive", "io-block", "unsorted"])

    def test_writing_names_the_folders_left_to_sort(self):
        *_, err = build({"v/a": device("A", 'category = "drive"\n', "drive"), "v/c": device("C")})
        self.assertIn("devices/v/c", err.getvalue())
        self.assertNotIn("devices/v/a", err.getvalue())


class CatalogFile(unittest.TestCase):
    """CATALOG.md: the same devices as a list, written and checked with the index."""

    FOLDERS = MappingProxyType(
        {
            "v/a": device("A", 'category = "drive"\nchannels = "none"\n', "drive")
            + '[protocols.enip]\ndriver = "enip-io"\ninput_assembly = { instance = 1, bytes = 2 }\n'
            + '[[points]]\nname = "x"\n[[points]]\nname = "y"\n',
            "v/b": device("B", 'category = "io-block"\nchecked_on = "2026-11-02"\n')
            + '[protocols.modbus]\ndriver = "modbus-tcp"\n',
            "w/c": device("C", 'category = "io-block"\n'),
        }
    )

    def test_every_device_is_under_its_category_with_what_it_gives(self):
        _, _, text, _, _ = build(self.FOLDERS)
        self.assertIn("3 devices in 2 categories.", text)
        self.assertIn("| [Drives](#drive) | 1 |", text)
        self.assertIn("| [I/O blocks (on the machine)](#io-block) | 2 |", text)
        drives = text.split('<a name="drive"></a>')[1]
        self.assertIn(
            "| [A](devices/v/a/) | V | EtherNet/IP | none | EDS connection, 2 points | documents |", drives
        )
        blocks = text.split('<a name="io-block"></a>')[1].split('<a name="drive"></a>')[0]
        self.assertIn("| [B](devices/v/b/) | V | Modbus TCP |  | identity and sources | 2026-11-02 |", blocks)
        self.assertIn("| [C](devices/w/c/) | V |  |  | identity and sources | documents |", blocks)
        self.assertLess(blocks.index("[B]"), blocks.index("[C]"))

    def test_the_index_counts_the_documented_points(self):
        _, index, _, _, _ = build(self.FOLDERS)
        by = {d["folder"]: d.get("points") for d in index["devices"]}
        self.assertEqual(by, {"devices/v/a": 2, "devices/v/b": None, "devices/w/c": None})

    def test_a_model_cannot_break_the_table_or_start_markup(self):
        _, _, text, _, _ = build(
            {"v/a": device("A | B <img src=x> [l](http://e) *b* `c` &amp;", 'category = "drive"\n')}
        )
        row = next(line for line in text.splitlines() if "devices/v/a/" in line)
        self.assertEqual(row.count(" | "), 5)
        self.assertNotIn("<img", row)
        self.assertNotIn("[l](", row)
        self.assertIn("&amp;amp;", row)

    def test_check_passes_when_current_and_fails_when_either_file_is_stale(self):
        code, _, _, root, _ = build(self.FOLDERS, "--check")
        self.assertEqual(code, 0)
        import sys

        old_root, old_argv = bi.ROOT, sys.argv
        bi.ROOT, sys.argv = root, ["build-index.py", "--check"]
        try:
            import contextlib
            import io

            for name in ("CATALOG.md", "index.json"):
                good = (root / name).read_text()
                (root / name).write_text(good + "\n")
                with contextlib.redirect_stderr(io.StringIO()) as err:
                    self.assertEqual(bi.main(), 1)
                self.assertIn(name, err.getvalue())
                (root / name).write_text(good)
            (root / "CATALOG.md").unlink()
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(bi.main(), 1)
        finally:
            bi.ROOT, sys.argv = old_root, old_argv


class Schema(unittest.TestCase):
    """docs/device.schema.json: a key it does not list, or a value of the wrong type, fails the build."""

    def test_the_schema_is_the_format_it_names(self):
        import json

        schema = json.loads(bi.SCHEMA.read_text())
        self.assertEqual(schema["format"], "helmsman-device-schema 1")
        self.assertIn("device", schema["root"])

    def test_every_device_in_the_library_conforms(self):
        for f in sorted((bi.ROOT / "devices").glob("*/*/device.toml")):
            with self.subTest(folder=f.parent.name):
                bi.entry(f.parent)

    def test_unknown_keys_refused_at_every_depth(self):
        for extra in (
            'surprise = "x"\n',
            "[surprise]\nx = 1\n",
            "[[surprise]]\nx = 1\n",
            '[device.photo]\nurl = "https://v.example/a.png"\npage = "https://v.example/a"\nseen = 2026-11-16\nx = 1\n',
            '[protocols.enip]\ndriver = "enip-io"\nrunaway = true\n',
            (
                '[protocols.enip]\ndriver = "enip-io"\n[protocols.enip.eds]\nname = "a.eds"\nsize = 1\n'
                f'sha256 = "{"a" * 64}"\nrunaway = 1\n'
            ),
            '[protocols.profinet]\ndriver = "enip-io"\n',
            '[[sources]]\ntitle = "t"\nsha256 = "aa"\nwhere = "p. 1"\nextra = "x"\n',
            '[[points]]\nname = "n"\nmeaning = "m"\nsource = "s"\ncolour = "red"\n',
        ):
            with self.subTest(extra=extra), self.assertRaises(SystemExit) as err:
                entry(extra)
            self.assertIn("not a key of docs/device.schema.json", str(err.exception))

    def test_unknown_key_in_the_device_table_refused(self):
        with self.assertRaises(SystemExit):
            entry('colour = "red"\n')

    def test_wrong_types_refused(self):
        for extra in (
            "channels = 8\n",
            'article = ["a"]\n',
            "checked_on = true\n",
            '[identity.enip]\nvendor_id = "48"\nproduct_code = 1\n',
            "[identity.enip]\nvendor_id = true\nproduct_code = 1\n",
            "[protocols.enip]\ndriver = 1\n",
            '[protocols.modbus]\ndriver = "modbus-tcp"\nport = "502"\n',
            "points = 3\n",
            'points = ["a"]\n',
            "[[points]]\nname = 1\n",
            '[protocols]\nenip = "x"\n',
        ):
            with self.subTest(extra=extra), self.assertRaises(SystemExit):
                entry(extra)

    def test_a_path_that_climbs_out_of_its_folder_refused(self):
        for name in ("../x.map", "/etc/passwd", "a/b.map", "..", "x\\\\y.map"):
            with self.subTest(map=name), self.assertRaises(SystemExit):
                entry(f'[protocols.modbus]\ndriver = "modbus-tcp"\nmap = "{name}"\n')
        for name in ("../x.device", "/x.device", "sub/x.device"):
            with self.subTest(profile=name), self.assertRaises(SystemExit):
                entry(f'profile = "{name}"\n')
        with self.assertRaises(SystemExit):
            entry(
                '[protocols.enip]\ndriver = "enip-io"\n'
                '[protocols.enip.eds]\nname = "../../x.eds"\nsize = 1\n'
                f'sha256 = "{"a" * 64}"\n'
            )
