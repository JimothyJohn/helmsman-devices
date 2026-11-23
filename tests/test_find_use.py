"""scripts/find.py and scripts/use.py: finding a device by category and words,
and what its folder gives a project.

Both read the repository's own files, which are public data anyone may send
a pull request for: a hostile index or folder name must be refused or shown
as text, never followed. use.py's lines are held to the I/O map's grammar
(helmsman-io `text`, `enip` and `profile_driver`), and it must have an answer
for every folder the library holds.
"""

import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import re
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), REPO / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


find = load("find")
use = load("use")

CATS = [
    {"id": "drive", "label": "Drives", "what": "x"},
    {"id": "io-block", "label": "I/O blocks", "what": "x"},
]
DEVICES = [
    {
        "folder": "devices/acme/vfd-9",
        "vendor": "Acme",
        "model": "VFD 9",
        "kind": "drive",
        "category": "drive",
        "identity": {"enip": {"vendor_id": 1, "product_code": 9}},
        "protocols": {"enip": {"driver": "enip-io", "eds": {"name": "a.eds", "size": 1, "sha256": "0" * 64}}},
    },
    {
        "folder": "devices/acme/block-8",
        "vendor": "Acme",
        "model": "Block 8",
        "kind": "remote-io",
        "category": "io-block",
        "checked_on": "2026-11-02",
        "channels": "8 DI, 4 relays",
        "points": 3,
        "profile": "acme-block-8.device",
        "protocols": {"enip": {"driver": "enip-io", "map": "enip.map"}, "modbus": {"driver": "modbus-tcp"}},
    },
    {
        "folder": "devices/zeta/eye",
        "vendor": "Zeta",
        "model": "Eye",
        "kind": "sensor",
        "category": "drive",
        "identity": {"iolink": {"vendor_id": 310, "device_id": 666}},
        "products": ["ZE-1001", "ZE-1002"],
        "record": "record.json",
    },
]


def run(mod, *argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = mod.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def index_file(devices=DEVICES, cats=CATS, fmt="helmsman-devices-index 1", raw=None):
    p = pathlib.Path(tempfile.mkdtemp()) / "index.json"
    p.write_text(
        raw if raw is not None else json.dumps({"format": fmt, "categories": cats, "devices": devices})
    )
    return str(p)


class Find(unittest.TestCase):
    def folders(self, *argv):
        code, out, _ = run(find, "--index", index_file(), "--json", *argv)
        return code, [json.loads(line)["folder"] for line in out.splitlines()]

    def test_no_arguments_lists_the_categories_with_counts(self):
        code, out, _ = run(find, "--index", index_file())
        self.assertEqual(code, 0)
        self.assertRegex(out, r"drive\s+2\s+Drives")
        self.assertRegex(out, r"io-block\s+1\s+I/O blocks")

    def test_a_category_lists_only_its_devices(self):
        self.assertEqual(self.folders("io-block"), (0, ["devices/acme/block-8"]))

    def test_words_narrow_a_category_and_are_case_blind(self):
        self.assertEqual(self.folders("drive", "ACME"), (0, ["devices/acme/vfd-9"]))

    def test_words_alone_search_everything_and_all_must_match(self):
        self.assertEqual(self.folders("acme")[1], ["devices/acme/block-8", "devices/acme/vfd-9"])
        self.assertEqual(self.folders("acme", "eye"), (1, []))

    def test_an_order_number_finds_the_record(self):
        self.assertEqual(self.folders("ze-1002"), (0, ["devices/zeta/eye"]))

    def test_identity_protocol_ready_and_checked_filter(self):
        self.assertEqual(self.folders("--id", "1:9")[1], ["devices/acme/vfd-9"])
        self.assertEqual(self.folders("--id", "1:10"), (1, []))
        self.assertEqual(self.folders("--protocol", "modbus")[1], ["devices/acme/block-8"])
        self.assertEqual(self.folders("--protocol", "iolink")[1], ["devices/zeta/eye"])
        self.assertEqual(self.folders("--ready")[1], ["devices/acme/block-8"])
        self.assertEqual(self.folders("--checked")[1], ["devices/acme/block-8"])

    def test_json_says_what_the_folder_gives(self):
        _, out, _ = run(find, "--index", index_file(), "--json", "io-block")
        self.assertEqual(json.loads(out)["gives"], ["profile", "map", "3 points"])

    def test_what_a_device_has_is_searched_and_shown(self):
        self.assertEqual(self.folders("relay"), (0, ["devices/acme/block-8"]))
        self.assertEqual(self.folders("drive", "relay"), (1, []))
        _, out, _ = run(find, "--index", index_file(), "acme")
        self.assertRegex(
            out, r"Acme Block 8\s+8 DI, 4 relays\s+enip,modbus\s+profile, map, 3 points\s+2026-11-02"
        )
        self.assertRegex(out, r"Acme VFD 9\s+-\s+enip\s+eds\s+documents")

    def test_one_device_is_not_called_devices(self):
        _, out, _ = run(find, "--index", index_file(), "io-block")
        self.assertTrue(out.startswith("1 device under I/O blocks\n"), out)
        _, out, _ = run(find, "--index", index_file(), "acme")
        self.assertTrue(out.startswith("2 devices\n"), out)

    def test_a_folder_with_nothing_to_paste_says_identity_only(self):
        bare = [{"folder": "devices/a/b", "vendor": "A", "model": "B", "category": "drive", "points": True}]
        _, out, _ = run(find, "--index", index_file(bare), "drive")
        self.assertIn("identity only", out)

    def test_the_list_points_at_use(self):
        _, out, _ = run(find, "--index", index_file(), "drive", "vfd")
        self.assertIn("python3 -I scripts/use.py devices/acme/vfd-9", out)

    def test_nothing_found_is_exit_1_and_names_the_categories(self):
        code, out, err = run(find, "--index", index_file(), "nosuchthing")
        self.assertEqual((code, out), (1, ""))
        self.assertIn("drive io-block", err)

    def test_bad_arguments_are_exit_2(self):
        for argv in (
            ["--id", "1"],
            ["--id", "70000:1"],
            ["--id", "a:b"],
            ["--protocol", "profinet"],
            ["--nope"],
            ["--id"],
        ):
            with self.subTest(argv=argv):
                code, _, err = run(find, "--index", index_file(), *argv)
                self.assertEqual(code, 2)
                self.assertTrue(err.startswith("find.py: "))

    def test_an_index_that_is_not_one_is_refused(self):
        for path in (
            index_file(fmt="helmsman-devices-index 2"),
            index_file(raw="not json"),
            index_file(raw="[]"),
            index_file(raw=json.dumps({"format": "helmsman-devices-index 1", "devices": "x"})),
            index_file(raw=json.dumps({"format": "helmsman-devices-index 1", "devices": [1, 2]})),
            index_file(
                raw=json.dumps({"format": "helmsman-devices-index 1", "devices": [], "categories": {}})
            ),
            index_file(raw=" " * ((4 << 20) + 1)),
            "/nonexistent/index.json",
        ):
            with self.subTest(path=path):
                self.assertEqual(run(find, "--index", path)[0], 2)

    def test_control_characters_in_an_index_never_reach_the_terminal(self):
        evil = [{**DEVICES[0], "model": "VFD\x1b[2J\x07 9", "vendor": "Ac\rme", "folder": "devices/a\nb/c"}]
        cats = [{"id": "drive", "label": "Dri\x1b[31mves", "what": "x"}]
        for argv in ([], ["drive"]):
            _, out, _ = run(find, "--index", index_file(evil, cats), *argv)
            self.assertFalse(re.search(r"[\x00-\x09\x0b-\x1f\x7f]", out), out)

    def test_entries_with_fields_of_the_wrong_type_do_not_crash(self):
        odd = [
            {
                "folder": 7,
                "vendor": None,
                "model": ["x"],
                "category": "drive",
                "protocols": "enip",
                "identity": 3,
            }
        ]
        code, _, _ = run(find, "--index", index_file(odd), "drive")
        self.assertEqual(code, 0)

    def test_the_library_itself_has_every_device_in_a_named_category(self):
        cats, devices = find.load(REPO / "index.json")
        ids = {c["id"] for c in cats}
        self.assertTrue(devices)
        self.assertEqual([d["folder"] for d in devices if d.get("category") not in ids], [])


DEVICE_LINE = re.compile(
    r"device [a-z][a-z0-9_]* (enip-io|modbus-tcp|device:[a-z0-9][a-z0-9_-]*) \S+( [a-z_.]+=\S+)*"
)
EXPLICIT = re.compile(r"device \S+ enip-io \S+ config=\d+ o2t=\d+:\d+ t2o=\d+:\d+( rpi_ms=\d+)?")
SIGNAL_LINE = re.compile(
    r"(in |out) [a-z][a-z0-9_]* (bool|int|real) [a-z][a-z0-9_]* ch:[A-Za-z][A-Za-z0-9_-]*"
)


class Library:
    """A scratch library with one folder, in place of the repository's."""

    def __init__(self, toml, files=None, index=None):
        self.root = pathlib.Path(tempfile.mkdtemp())
        self.folder = self.root / "devices" / "acme" / "block-8"
        self.folder.mkdir(parents=True)
        (self.folder / "device.toml").write_text(toml)
        for name, text in (files or {}).items():
            (self.folder / name).write_text(text)
        (self.root / "index.json").write_text(json.dumps(index or {"format": "x", "devices": []}))

    def __enter__(self):
        self.old, use.ROOT = use.ROOT, self.root
        return self

    def __exit__(self, *exc):
        use.ROOT = self.old


BASE = '[device]\nvendor = "Acme"\nmodel = "Block 8"\nkind = "remote-io"\ncategory = "io-block"\n'
ENIP = (
    '[identity.enip]\nvendor_id = 48\nproduct_code = 14076\n[protocols.enip]\ndriver = "enip-io"\n'
    "input_assembly = { instance = 103, bytes = 20 }\noutput_assembly = { instance = 104, bytes = 14 }\n"
    "config_assembly = { instance = 106, bytes = 10 }\n"
)


def sheet(toml, *argv, files=None, index=None):
    with Library(toml, files, index):
        code, out, err = run(use, "acme/block-8", "--json", *argv)
    return json.loads(out) if code == 0 else (code, err)


def lines(s, how):
    return [line for w in s["ways"] if w["how"] == how for line in w["lines"]]


class Use(unittest.TestCase):
    def test_the_explicit_line_is_the_entrys_assemblies(self):
        s = sheet(BASE + ENIP)
        self.assertEqual(lines(s, "explicit"), ["device dev enip-io ADDR config=106 o2t=104:14 t2o=103:20"])
        self.assertIn("cip=48:14076", " ".join(s["hints"]))

    def test_id_and_address_go_into_every_device_line(self):
        s = sheet(
            BASE + ENIP + '[protocols.modbus]\ndriver = "modbus-tcp"\nunit = 3\n',
            "--id",
            "rio",
            "--address",
            "10.1.2.3",
        )
        self.assertEqual(
            lines(s, "explicit"), ["device rio enip-io 10.1.2.3 config=106 o2t=104:14 t2o=103:20"]
        )
        self.assertEqual(lines(s, "modbus"), ["device rio modbus-tcp 10.1.2.3:502 unit=3"])
        self.assertEqual(s["hints"], [])

    def test_a_missing_size_or_instance_writes_no_explicit_line(self):
        for broken in (
            ENIP.replace("{ instance = 103, bytes = 20 }", "{ instance = 103 }"),
            ENIP.replace("config_assembly = { instance = 106, bytes = 10 }\n", ""),
            ENIP.replace("output_assembly = { instance = 104, bytes = 14 }\n", ""),
            ENIP.replace("instance = 104", 'instance = "104 rpi_ms=1"'),
        ):
            with self.subTest(broken=broken):
                self.assertEqual(lines(sheet(BASE + broken), "explicit"), [])

    def test_an_eds_is_named_with_its_hash_and_the_check(self):
        eds = f'eds = {{ name = "b8.eds", size = 5, sha256 = "{"a" * 64}", url = "https://acme.example/b8.zip" }}\n'
        s = sheet(BASE + ENIP + eds)
        way = next(w for w in s["ways"] if w["how"] == "eds")
        self.assertEqual(way["lines"], ["device dev enip-io ADDR eds=b8.eds"])
        self.assertIn("a" * 64, " ".join(way["notes"]))
        self.assertIn("--eds PATH", " ".join(way["steps"]))
        self.assertEqual([w["how"] for w in s["ways"]], ["eds", "explicit"])

    def test_a_profile_comes_first_with_a_channel_of_each_direction(self):
        profile = (
            "helmsman-device 1\nvendor Acme\ntransport enip-io config=1 o2t=2:1 t2o=3:1\ntransport modbus-tcp unit=1\n"
            "in  DI-00 bool enip-io=in:0.0 modbus-tcp=di:0\nout DO-00 bool safe=false enip-io=out:0.0 modbus-tcp=coil:0\n"
            "in  bad name bool\nin  x!y bool enip-io=in:0.1\n"
        )
        s = sheet(
            BASE + 'profile = "acme-block-8.device"\n' + ENIP,
            "--id",
            "rio",
            files={"acme-block-8.device": profile},
        )
        self.assertEqual(s["ways"][0]["how"], "profile")
        self.assertEqual(
            s["ways"][0]["lines"],
            [
                "device rio device:acme-block-8 ADDR",
                "in  rio_di_00 bool rio ch:DI-00",
                "out rio_do_00 bool rio ch:DO-00",
            ],
        )
        self.assertIn("enip-io, then modbus-tcp", " ".join(s["ways"][0]["notes"]))
        self.assertIn("2 channels: DI-00, DO-00", " ".join(s["ways"][0]["notes"]))

    def test_a_map_gets_the_address_on_its_device_lines_only(self):
        text = "# ADDR is the unit\ndevice b8 modbus-tcp ADDR:502 unit=1\nin  ADDR bool b8 di:0\n"
        toml = BASE + '[protocols.modbus]\ndriver = "modbus-tcp"\nmap = "modbus.map"\n'
        got = lines(sheet(toml, "--address", "10.1.2.3", files={"modbus.map": text}), "map")
        self.assertEqual(
            got, ["# ADDR is the unit", "device b8 modbus-tcp 10.1.2.3:502 unit=1", "in  ADDR bool b8 di:0"]
        )
        got = lines(sheet(toml, "--address", "10.1.2.3:1502", files={"modbus.map": text}), "map")
        self.assertEqual(got[1], "device b8 modbus-tcp 10.1.2.3:1502 unit=1")
        self.assertEqual(
            lines(sheet(toml, files={"modbus.map": text}), "map")[1], "device b8 modbus-tcp ADDR:502 unit=1"
        )
        self.assertEqual(lines(sheet(toml, files={"modbus.map": text}), "modbus"), [])

    def test_id_names_a_maps_one_device_and_the_signals_on_it(self):
        text = "device b8 modbus-tcp ADDR:502 unit=1  # b8 is the block\nin  b8  bool b8 di:0\nout x bool box do:0\n"
        toml = BASE + '[protocols.modbus]\ndriver = "modbus-tcp"\nmap = "modbus.map"\n'
        got = sheet(toml, "--id", "rio", files={"modbus.map": text})
        self.assertEqual(
            lines(got, "map"),
            [
                "device rio modbus-tcp ADDR:502 unit=1  # b8 is the block",
                "in  b8  bool rio di:0",
                "out x bool box do:0",
            ],
        )
        kept = sheet(toml, files={"modbus.map": text})
        self.assertEqual(lines(kept, "map")[0], "device b8 modbus-tcp ADDR:502 unit=1  # b8 is the block")
        self.assertIn("--id sets it", " ".join(kept["ways"][0]["notes"]))
        two = text + "device other modbus-tcp ADDR:502\n"
        got = sheet(toml, "--id", "rio", files={"modbus.map": two})
        self.assertEqual(lines(got, "map")[0].split()[1], "b8")
        self.assertIn("several devices", " ".join(got["ways"][0]["notes"]))

    def test_an_eds_inside_a_zip_is_said_to_be_inside_it(self):
        eds = 'eds = { name = "b8.eds", size = 5, sha256 = "%s", url = "https://acme.example/f.zip (member of f.zip)" }\n'
        step = next(w for w in sheet(BASE + ENIP + eds % ("a" * 64))["ways"] if w["how"] == "eds")["steps"][0]
        self.assertEqual(
            step, "Get f.zip from https://acme.example/f.zip and take b8.eds (5 bytes) out of it."
        )

    def test_modbus_without_a_unit_says_so_and_does_not_invent_one(self):
        s = sheet(BASE + '[protocols.modbus]\ndriver = "modbus-tcp"\nport = 1502\n')
        self.assertEqual(lines(s, "modbus"), ["device dev modbus-tcp ADDR:1502"])
        self.assertIn("no unit id", " ".join(s["ways"][0]["notes"]))

    def test_a_wired_sensor_gets_the_wired_word(self):
        toml = '[device]\nvendor = "Acme"\nmodel = "Eye"\nkind = "sensor"\n[wired]\nsio = true\n'
        s = sheet(toml)
        self.assertEqual([w["how"] for w in s["ways"]], ["wired"])
        self.assertTrue(lines(s, "wired")[0].endswith(" wired=acme/block-8"))

    def test_what_nobody_confirmed_is_said(self):
        s = sheet(BASE + ENIP + '[[questions]]\nask = "Which coil?"\nsource = "p. 7"\n')
        text = " ".join(s["open"])
        self.assertIn("No unit has confirmed", text)
        self.assertIn("No channel is mapped", text)
        self.assertIn("Which coil? (p. 7)", text)
        self.assertIsNone(s["checked_on"])
        checked = sheet(BASE.replace("kind", 'checked_on = "2026-11-02"\nfirmware = "V3"\nkind') + ENIP)
        self.assertEqual((checked["checked_on"], checked["firmware"]), ("2026-11-02", "V3"))
        self.assertNotIn("No unit has confirmed", " ".join(checked["open"]))
        self.assertNotIn("no unit has opened", " ".join(n for w in checked["ways"] for n in w["notes"]))

    def test_points_carry_their_source(self):
        s = sheet(
            BASE
            + '[[points]]\nname = "DI"\nmodbus = "di:0..di:7"\nmeaning = "1 = on"\nsource = "Manual p. 4"\n'
        )
        self.assertEqual(
            s["points"],
            [{"name": "DI", "modbus": "di:0..di:7", "meaning": "1 = on", "source": "Manual p. 4"}],
        )

    def test_identity_and_sources_only_says_there_is_nothing_to_paste(self):
        s = sheet(BASE + '[[sources]]\ntitle = "Manual"\nsha256 = "x"\nwhere = "https://acme.example"\n')
        self.assertEqual(s["ways"], [])
        self.assertIn("nothing to paste yet", " ".join(s["open"]))

    def test_bad_arguments_are_exit_2(self):
        for argv in (
            ["--id", "box"],
            ["--id", "Rio"],
            ["--id", "a b"],
            ["--id", "x" * 25],
            ["--address", "10.0.0.1 unit=9"],
            ["--address", "$(reboot)"],
            ["--address", "a;b"],
            ["--address", ""],
            ["--nope"],
            ["--address"],
        ):
            with self.subTest(argv=argv), Library(BASE + ENIP):
                code, out, err = run(use, "acme/block-8", *argv)
                self.assertEqual((code, out), (2, ""))
                self.assertTrue(err.startswith("use.py: "))

    def test_a_folder_outside_the_library_is_never_read(self):
        with Library(BASE + ENIP) as lib:
            (lib.root / "secret").mkdir()
            (lib.root / "secret" / "device.toml").write_text(BASE)
            (lib.root / "devices" / "acme" / "link").symlink_to(lib.root / "secret")
            for name in (
                "../secret",
                "devices/../secret",
                "acme/../../secret",
                "/etc/passwd",
                "acme/link",
                "acme/BLOCK-8",
                "",
            ):
                with self.subTest(name=name):
                    code, out, _ = run(use, name)
                    self.assertEqual((code, out), (2, ""))

    def test_words_must_match_exactly_one_device(self):
        index = {
            "format": "x",
            "devices": [
                {
                    "folder": "devices/acme/block-8",
                    "vendor": "Acme",
                    "model": "Block 8",
                    "products": ["B8-001"],
                },
                {"folder": "devices/acme/other", "vendor": "Acme", "model": "Other"},
            ],
        }
        with Library(BASE + ENIP, index=index):
            self.assertEqual(run(use, "b8-001")[0], 0)
            self.assertEqual(run(use, "block", "8")[0], 0)
            code, _, err = run(use, "acme")
            self.assertEqual(code, 2)
            self.assertIn("matches 2 devices", err)
            self.assertIn("devices/acme/other", err)
            self.assertEqual(run(use, "nosuch")[0], 2)

    def test_eds_check_accepts_the_file_and_refuses_another(self):
        data = b"[File]\n"
        digest = hashlib.sha256(data).hexdigest()
        eds = f'eds = {{ name = "b8.eds", size = {len(data)}, sha256 = "{digest}" }}\n'
        with Library(BASE + ENIP + eds) as lib:
            good, other, same_size = lib.root / "good.eds", lib.root / "other.eds", lib.root / "same.eds"
            good.write_bytes(data)
            other.write_bytes(data + b"x")
            same_size.write_bytes(b"[Fila]\n")
            self.assertEqual(run(use, "acme/block-8", "--eds", str(good))[0], 0)
            for bad in (other, same_size):
                code, out, err = run(use, "acme/block-8", "--eds", str(bad))
                self.assertEqual((code, out), (1, ""))
                self.assertIn("NOT the file", err)
            self.assertEqual(run(use, "acme/block-8", "--eds", str(lib.root / "missing.eds"))[0], 2)
        with Library(BASE + ENIP):
            self.assertEqual(run(use, "acme/block-8", "--eds", "/dev/null")[0], 2)

    def test_control_characters_in_a_folder_never_reach_the_terminal(self):
        toml = (
            BASE.replace("Block 8", "Block\\u001b[2J 8")
            + '[[points]]\nname = "a\\u0007b"\nmeaning = "x\\ry"\n'
        )
        with Library(toml, files={}):
            _, out, _ = run(use, "acme/block-8")
        self.assertFalse(re.search(r"[\x00-\x09\x0b-\x1f\x7f]", out), out)

    def test_every_folder_of_the_library_has_an_answer_in_the_maps_grammar(self):
        folders = sorted(p.parent for p in (REPO / "devices").glob("*/*/device.toml"))
        self.assertGreater(len(folders), 100)
        for f in folders:
            rel = f.relative_to(REPO).as_posix()
            with self.subTest(folder=rel):
                code, out, err = run(use, rel, "--json", "--address", "192.0.2.10")
                self.assertEqual(code, 0, err)
                s = json.loads(out)
                self.assertEqual(s["folder"], rel)
                self.assertTrue(s["ways"] or any("nothing to paste" in o for o in s["open"]))
                for w in s["ways"]:
                    if w["how"] in ("map", "wired"):
                        continue
                    self.assertRegex(w["lines"][0], DEVICE_LINE)
                    self.assertIn(" 192.0.2.10", w["lines"][0])
                    if w["how"] == "explicit":
                        self.assertRegex(w["lines"][0], EXPLICIT)
                    for line in w["lines"][1:]:
                        self.assertRegex(line, SIGNAL_LINE)
                self.assertEqual(run(use, rel)[0], 0)


if __name__ == "__main__":
    unittest.main()
