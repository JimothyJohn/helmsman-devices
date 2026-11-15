"""scripts/build-records.py: record.json for a wired sensor or actuator, bounded and checked.

A controller fetches record.json for one device and shows what it says, so
every text is bounded and printable, every number is a number, and a
switching signal is never stated without where it was read.
"""

import contextlib
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent.parent / "scripts"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


br = load("build_records", "build-records.py")
bi = load("build_index", "build-index.py")

SENSOR = """[device]
vendor = "Bench"
model = "BX-12 inductive sensor"
kind = "sensor"
family = "BX inductive"

[identity.iolink]
vendor_id = 310
device_id = 666

[[variants]]
product_id = "BX-12 PNP"
name = "BX-12, M12 plug"

[wired]
sio = true

[[wired.connections]]
type = "M12-4"
products = ["BX-12 PNP"]
wires = [
  { n = 1, function = "L+", color = "BN" },
  { n = 2, function = "Other", color = "WH", name = "Q2" },
  { n = 4, function = "C/Q", color = "BK" },
]

[[signals]]
dir = "in"
name = "Switching signal 1"
type = "bool"
bits = "0"
off = "No target"
on = "Target present"

[[signals]]
dir = "in"
name = "Quality"
type = "uint"
bits = "8..15"
values = { 255 = "No echo" }

[[settings]]
name = "SSC1 Config: Logic"
index = 61
subindex = 1
default = "0"
default_name = "High active"
values = { 0 = "High active", 1 = "Low active" }
"""

NETWORKED = '[device]\nvendor = "V"\nmodel = "M"\nkind = "remote-io"\n'


def tree(files: dict) -> pathlib.Path:
    root = pathlib.Path(tempfile.mkdtemp())
    for rel, body in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(body)
    return root


def run(argv, root):
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        code = br.main(argv, root=root)
    return code, out.getvalue()


class Records(unittest.TestCase):
    def test_a_wired_device_gets_a_record_and_a_networked_one_none(self):
        root = tree({"devices/bench/bx-12/device.toml": SENSOR, "devices/v/m/device.toml": NETWORKED})
        code, said = run([], root)
        self.assertEqual(code, 0, said)
        self.assertFalse((root / "devices/v/m/record.json").exists())
        rec = json.loads((root / "devices/bench/bx-12/record.json").read_text())
        self.assertEqual(rec["format"], "helmsman-device-record 1")
        self.assertEqual(
            {k: rec[k] for k in ("folder", "vendor", "model", "kind", "family", "draft")},
            {
                "folder": "devices/bench/bx-12",
                "vendor": "Bench",
                "model": "BX-12 inductive sensor",
                "kind": "sensor",
                "family": "BX inductive",
                "draft": True,
            },
        )
        self.assertEqual(rec["iolink"], {"vendor_id": 310, "device_id": 666})
        self.assertEqual(rec["variants"], [{"product_id": "BX-12 PNP", "name": "BX-12, M12 plug"}])
        self.assertEqual(rec["wired"]["sio"], True)
        self.assertNotIn("switching", rec["wired"])
        self.assertEqual(
            rec["wired"]["connections"][0]["wires"][1],
            {"n": 2, "function": "Other", "color": "WH", "name": "Q2"},
        )
        self.assertEqual(
            rec["signals"][0],
            {
                "dir": "in",
                "name": "Switching signal 1",
                "type": "bool",
                "bits": "0",
                "on": "Target present",
                "off": "No target",
            },
        )
        self.assertEqual(rec["signals"][1]["values"], {"255": "No echo"})
        self.assertEqual(
            rec["settings"],
            [
                {
                    "name": "SSC1 Config: Logic",
                    "index": 61,
                    "subindex": 1,
                    "default": "0",
                    "default_name": "High active",
                    "values": {"0": "High active", "1": "Low active"},
                }
            ],
        )

    def test_check_says_what_is_stale_and_writes_nothing(self):
        root = tree({"devices/bench/bx-12/device.toml": SENSOR, "devices/v/m/device.toml": NETWORKED})
        code, said = run(["--check"], root)
        self.assertEqual(code, 1)
        self.assertIn("devices/bench/bx-12/record.json: out of date", said)
        self.assertFalse((root / "devices/bench/bx-12/record.json").exists())
        run([], root)
        self.assertEqual(run(["--check"], root)[0], 0)
        # An edit to device.toml makes it stale; a record left beside a networked device too.
        toml = root / "devices/bench/bx-12/device.toml"
        toml.write_text(toml.read_text().replace("No target", "Free"))
        (root / "devices/v/m/record.json").write_text("{}")
        code, said = run(["--check"], root)
        self.assertEqual(code, 1)
        self.assertIn("devices/v/m/record.json: its device.toml has no [wired]", said)
        self.assertTrue((root / "devices/v/m/record.json").exists())
        run([], root)
        self.assertFalse((root / "devices/v/m/record.json").exists())
        self.assertEqual(run(["--check"], root)[0], 0)

    def test_a_checked_record_with_its_switching_signal_is_not_a_draft(self):
        text = SENSOR.replace('kind = "sensor"', 'kind = "sensor"\nchecked_on = "2026-11-15"').replace(
            "sio = true", 'sio = true\nswitching = "Switching signal 1"\nsource = "data sheet, p. 2"'
        )
        root = tree({"devices/bench/bx-12/device.toml": text})
        run([], root)
        rec = json.loads((root / "devices/bench/bx-12/record.json").read_text())
        self.assertIs(rec["draft"], False)
        self.assertEqual(
            (rec["wired"]["switching"], rec["wired"]["source"]), ("Switching signal 1", "data sheet, p. 2")
        )

    def test_what_a_record_refuses(self):
        cases = [
            ("sio = true", 'sio = "yes"', "wired.sio"),
            ("sio = true", 'sio = true\nswitching = "Switching signal 1"', "needs its source"),
            ('dir = "in"\nname = "Quality"', 'dir = "both"\nname = "Quality"', "signals[1].dir"),
            ('type = "uint"', 'type = "decimal"', "signals[1].type"),
            ('name = "Quality"', 'name = "a\\u0007b"', "signals[1].name"),
            ('name = "Quality"', 'name = "' + "x" * 161 + '"', "signals[1].name"),
            ('name = "Quality"', "name = 7", "signals[1].name"),
            ("index = 61", "index = 65536", "settings[0].index"),
            ("index = 61", 'index = "61"', "settings[0].index"),
            ("subindex = 1", "subindex = 0", "settings[0].subindex"),
            ('default = "0"', "default = 0", "settings[0].default"),
            ("{ n = 1,", "{ n = 10,", "wires[0].n"),
            ("vendor_id = 310", "vendor_id = 0", "identity.iolink.vendor_id"),
            ("device_id = 666", "device_id = 16777216", "identity.iolink.device_id"),
            ('product_id = "BX-12 PNP"', "product_id = 12", "variants[0].product_id"),
            ('vendor = "Bench"', 'vendor = ""', "device.vendor"),
        ]
        for old, new, why in cases:
            self.assertIn(old, SENSOR, old)
            root = tree({"devices/bench/bx-12/device.toml": SENSOR.replace(old, new, 1)})
            with self.assertRaises(SystemExit, msg=new) as caught:
                run([], root)
            self.assertIn(why, str(caught.exception), new)
            self.assertLess(len(str(caught.exception)), 300)
            self.assertFalse((root / "devices/bench/bx-12/record.json").exists())
        many = SENSOR + "".join(
            f'[[signals]]\ndir = "in"\nname = "s{i}"\ntype = "bool"\n' for i in range(256)
        )
        with self.assertRaises(SystemExit) as caught:
            run([], tree({"devices/bench/bx-12/device.toml": many}))
        self.assertIn("at most 256", str(caught.exception))

    def test_the_index_says_a_record_is_there(self):
        root = tree({"devices/bench/bx-12/device.toml": SENSOR, "devices/v/m/device.toml": NETWORKED})
        old = bi.ROOT
        bi.ROOT = root
        try:
            sensor = bi.entry(root / "devices/bench/bx-12")
            block = bi.entry(root / "devices/v/m")
        finally:
            bi.ROOT = old
        self.assertEqual(sensor["record"], "record.json")
        self.assertNotIn("record", block)

    def test_every_record_in_the_library_is_current(self):
        code, said = run(["--check"], br.ROOT)
        self.assertEqual(code, 0, said)


if __name__ == "__main__":
    unittest.main()
