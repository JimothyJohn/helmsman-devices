"""scripts/build-review.py: every claim of a folder, as data a public page renders.

The page shows these strings to strangers, so the build is the gate: a
text is bounded and printable, a number is a number in range, a list is
bounded, and a folder that breaks any of it stops the build by name
instead of reaching the page.
"""

import importlib.util
import json
import pathlib
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "build-review.py"
spec = importlib.util.spec_from_file_location("build_review", SCRIPT)
br = importlib.util.module_from_spec(spec)
spec.loader.exec_module(br)

BASE = '[device]\nvendor = "V"\nmodel = "M"\nkind = "remote-io"\n'
FULL = (
    BASE
    + """channels = "8 DI"
checked_on = 2026-11-02
firmware = "V3.1"

[identity.enip]
vendor_id = 991
product_code = 515
device_type = 12
revisions = ["3.1", "4.1"]
product_name = "E1213"

[protocols.enip]
driver = "enip-io"
map = "enip.map"
input_assembly = { instance = 101, bytes = 51 }
output_assembly = { instance = 102, bytes = 1 }
config_assembly = { instance = 1 }
eds = { name = "e.eds", size = 1, sha256 = "ab" }

[protocols.modbus]
driver = "modbus-tcp"
port = 502
unit = 1

[[points]]
name = "DI-00..DI-11"
enip = "in:0.0..in:1.3"
modbus = "di:0..di:11"
meaning = "digital input state, 1 = on"
source = "manual p. B-1"

[wiring]
note = "needs field power"
source = "manual p. 2-6"

[[questions]]
ask = "Which coil is the first output: 0 or 1?"
source = "manual p. 7 against p. 8"

[[sources]]
title = "Manual"
sha256 = "F8788816B2E0062A68F9B7F1EF9850A2D57F92946AC8B64077C4E77097744454"
where = "https://example.invalid/m.pdf"
"""
)


def entry(toml: str) -> dict:
    root = pathlib.Path(tempfile.mkdtemp())
    f = root / "devices" / "v" / "m"
    f.mkdir(parents=True)
    (f / "device.toml").write_text(toml)
    old = br.ROOT
    br.ROOT = root
    try:
        return br.entry(f)
    finally:
        br.ROOT = old


class Claims(unittest.TestCase):
    def test_a_full_folder_carries_every_claim(self):
        self.assertEqual(
            entry(FULL),
            {
                "folder": "devices/v/m",
                "vendor": "V",
                "model": "M",
                "channels": "8 DI",
                "firmware": "V3.1",
                "checked_on": "2026-11-02",
                "enip": {
                    "map": True,
                    "identity": {
                        "vendor_id": 991,
                        "product_code": 515,
                        "device_type": 12,
                        "revisions": ["3.1", "4.1"],
                        "product_name": "E1213",
                    },
                    "input": {"instance": 101, "bytes": 51},
                    "output": {"instance": 102, "bytes": 1},
                    "config": {"instance": 1},
                    "eds": "e.eds",
                },
                "modbus": {"map": False, "port": 502, "unit": 1},
                "points": [
                    {
                        "name": "DI-00..DI-11",
                        "enip": "in:0.0..in:1.3",
                        "modbus": "di:0..di:11",
                        "meaning": "digital input state, 1 = on",
                        "source": "manual p. B-1",
                    }
                ],
                "sources": [
                    {
                        "title": "Manual",
                        "sha256": "f8788816b2e0062a68f9b7f1ef9850a2d57f92946ac8b64077c4e77097744454",
                        "where": "https://example.invalid/m.pdf",
                    }
                ],
                "questions": [
                    {"ask": "Which coil is the first output: 0 or 1?", "source": "manual p. 7 against p. 8"}
                ],
                "wiring": {"note": "needs field power", "source": "manual p. 2-6"},
            },
        )

    def test_the_least_a_folder_can_say(self):
        self.assertEqual(
            entry(BASE), {"folder": "devices/v/m", "vendor": "V", "model": "M", "points": [], "sources": []}
        )

    def test_nothing_a_folder_does_not_say_is_filled_in(self):
        e = entry(BASE + '\n[protocols.enip]\ndriver = "enip-io"\n')
        self.assertEqual(e["enip"], {"map": False})
        self.assertNotIn("modbus", e)
        self.assertNotIn("checked_on", e)


class Refused(unittest.TestCase):
    """Each of these names the folder and the field, and writes nothing."""

    def refused(self, toml, field):
        with self.assertRaises(SystemExit) as c:
            entry(toml)
        self.assertIn("devices/v/m", str(c.exception))
        self.assertIn(field, str(c.exception))

    def test_text_a_page_must_not_render(self):
        point = '\n[[points]]\nname = "p"\nmeaning = {}\n'
        for bad, field in (
            ('"line\\nbreak"', "points[0].meaning"),
            ('"esc\\u001b[31m"', "points[0].meaning"),
            ('"nul\\u0000"', "points[0].meaning"),
            ('"del\\u007f"', "points[0].meaning"),
            ('""', "points[0].meaning"),
            ('"' + "x" * 601 + '"', "points[0].meaning"),
            ("7", "points[0].meaning"),
            ('["a"]', "points[0].meaning"),
        ):
            with self.subTest(bad=bad[:20]):
                self.refused(BASE + point.format(bad), field)

    def test_markup_is_carried_as_text_not_refused(self):
        # Escaping is the page's job; the data stays what the folder said.
        e = entry(BASE + '\n[[points]]\nname = "<script>alert(1)</script>"\n')
        self.assertEqual(e["points"][0]["name"], "<script>alert(1)</script>")

    def test_numbers_out_of_range_or_not_numbers(self):
        for body, field in (
            ("[identity.enip]\nvendor_id = 65536\nproduct_code = 1", "identity.enip.vendor_id"),
            ("[identity.enip]\nvendor_id = -1\nproduct_code = 1", "identity.enip.vendor_id"),
            ('[identity.enip]\nvendor_id = "991"\nproduct_code = 1', "identity.enip.vendor_id"),
            ("[identity.enip]\nvendor_id = true\nproduct_code = 1", "identity.enip.vendor_id"),
            ("[identity.enip]\nvendor_id = 1.5\nproduct_code = 1", "identity.enip.vendor_id"),
            ('[identity.enip]\nrevisions = "3.1"', "identity.enip.revisions"),
            ("[identity.enip]\nrevisions = [3]", "identity.enip.revisions"),
            ("input_assembly = { instance = 70000 }", "input_assembly.instance"),
            ("input_assembly = { bytes = 4 }", "input_assembly.instance"),
            ('input_assembly = "101"', "input_assembly"),
            ('eds = "file.eds"', "protocols.enip.eds"),
        ):
            with self.subTest(body=body):
                toml = BASE + '\n[protocols.enip]\ndriver = "enip-io"\n'
                toml += body + "\n" if not body.startswith("[") else "\n" + body + "\n"
                self.refused(toml, field)
        self.refused(
            BASE + '\n[protocols.modbus]\ndriver = "modbus-tcp"\nunit = 256\n', "protocols.modbus.unit"
        )
        self.refused(
            BASE + '\n[protocols.modbus]\ndriver = "modbus-tcp"\nport = 65536\n', "protocols.modbus.port"
        )

    def test_a_checksum_is_64_hex_digits(self):
        for sha in ("abc", "g" * 64, "a" * 63, "a" * 65, "a" * 63 + "١"):
            with self.subTest(sha=sha[:8]):
                self.refused(BASE + f'\n[[sources]]\ntitle = "t"\nsha256 = "{sha}"\n', "sources[0].sha256")

    def test_a_date_is_a_date(self):
        for bad in ('"2026-13-01"', '"yesterday"', "2026-11-02T10:00:00", "20261102"):
            with self.subTest(bad=bad):
                self.refused(BASE + f"checked_on = {bad}\n", "device.checked_on")

    def test_shapes_that_are_not_what_the_format_says(self):
        # Top-level keys go before [device], or TOML reads them as device's.
        self.refused('points = "none"\n' + BASE, "points")
        self.refused("points = [1, 2]\n" + BASE, "points[0]")
        self.refused(BASE + '\n[sources]\ntitle = "t"\n', "sources")
        self.refused('wiring = "see manual"\n' + BASE, "wiring")
        self.refused('protocols = "enip"\n' + BASE, "protocols")
        self.refused('device = "x"\n', "device")
        self.refused(BASE + '\n[wiring]\nsource = "p. 1"\n', "wiring.note")
        self.refused(BASE + "\n" + '[[points]]\nname = "p"\n' * 257, "points")
        self.refused(BASE + '\n[[questions]]\nsource = "p. 1"\n', "questions[0].ask")
        self.refused(BASE + '\n[[questions]]\nask = "line\\nbreak"\n', "questions[0].ask")
        self.refused('questions = "none"\n' + BASE, "questions")


class Built(unittest.TestCase):
    def test_the_committed_file_is_what_the_folders_say(self):
        review = json.loads((br.ROOT / "review.json").read_text())
        self.assertEqual(review["format"], "helmsman-devices-review 1")
        folders = sorted(p.parent for p in (br.ROOT / "devices").glob("*/*/device.toml"))
        self.assertEqual(review["devices"], [br.entry(f) for f in folders])

    def test_it_lists_the_same_folders_as_the_index(self):
        review = json.loads((br.ROOT / "review.json").read_text())
        index = json.loads((br.ROOT / "index.json").read_text())
        self.assertEqual([d["folder"] for d in review["devices"]], [d["folder"] for d in index["devices"]])


if __name__ == "__main__":
    unittest.main()
