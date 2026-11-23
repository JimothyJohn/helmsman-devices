"""scripts/eds-draft.py: the EDS reader on written vectors and fuzzed bytes, and the draft it writes.

The vectors are written here in the EDS grammar (CIP Vol. 1 ch. 7), not
copied from a vendor's file: a vendor's EDS has no redistribution terms.
A draft is held to what build-index.py accepts, so a drafted folder can be
committed without hand edits.
"""

import hashlib
import importlib.util
import json
import pathlib
import random
import tempfile
import tomllib
import unittest

HERE = pathlib.Path(__file__).resolve().parent.parent / "scripts"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ed = load("eds_draft", "eds-draft.py")
bi = load("build_index", "build-index.py")

EDS = """$ EZ-EDS Version 3.27 Generated Electronic Data Sheet
[File]
        DescText = "Block I/O; 8 channels";   $ a ';' inside a string
        CreateDate = 04-20-2023;
        ModDate = 03-16-2026;
        Revision = 2.0;

[Device]
        VendCode = 48;
        VendName = "Turck";
        ProdType = 12;
        ProdTypeStr = "Communications Adapter";
        ProdCode = 0x2a1;
        MajRev = 3;
        MinRev = 7;
        ProdName = "TBEN-S2-8DXP"
                   " block";
        Catalog = "6814076";

[Params]
        Param1 = 0, , , 0x0000, 0xC7, 2, "RPI", "us", "", 1000, 3200000, 10000, , , , , , , , ;

[Assembly]
        Assem103 = "Inputs $ not a comment", "20 04 24 67 30 03", 6, 0x0000, , , 48, ;
        Assem104 = "Outputs", "20 04 24 68 30 03", 2, 0x0000, , , 16, ;
        Assem106 = "Config", "20 04 24 6A 30 03", 0, 0x0000, , , ;

[Connection Manager]
        Connection1 =
                0x04010002, 0x44640405,
                Param1, 2, Assem104,
                Param1, 6, Assem103,
                0, ,
                , ,
                "Exclusive Owner",
                "",
                "20 04 24 6A 2C 68 2C 67";
        Connection2 =
                0x02030002, 0x44640305,
                Param1, 0, ,
                Param1, 6, Assem103,
                , , , ,
                "Input Only",
                "",
                "20 04 24 6A 2C C6 2C 67";
"""


class Grammar(unittest.TestCase):
    def test_identity(self):
        d = ed.parse(EDS.encode())["device"]
        self.assertEqual(
            d,
            {
                "vendor_id": 48,
                "device_type": 12,
                "product_code": 0x2A1,
                "major_rev": 3,
                "minor_rev": 7,
                "vendor_name": "Turck",
                "device_type_name": "Communications Adapter",
                "product_name": "TBEN-S2-8DXP block",
                "catalog": "6814076",
            },
        )

    def test_file_assemblies_connections(self):
        e = ed.parse(EDS.encode())
        self.assertEqual((e["file_revision"], e["file_date"]), ("2.0", "03-16-2026"))
        self.assertEqual(
            e["assemblies"],
            [
                {"instance": 103, "name": "Inputs $ not a comment", "bytes": 6},
                {"instance": 104, "name": "Outputs", "bytes": 2},
                {"instance": 106, "name": "Config", "bytes": 0},
            ],
        )
        c1, c2 = e["connections"]
        self.assertEqual(
            c1,
            {
                "entry": "Connection1",
                "name": "Exclusive Owner",
                "o_to_t_bytes": 2,
                "t_to_o_bytes": 6,
                "config_bytes": 0,
                "config_instance": 0x6A,
                "o_to_t_instance": 0x68,
                "t_to_o_instance": 0x67,
            },
        )
        self.assertEqual((c2["name"], c2["o_to_t_instance"], c2["o_to_t_bytes"]), ("Input Only", 0xC6, 0))

    def test_size_from_members_when_the_size_field_is_empty(self):
        """Turck's TBEN-S EDS leave the size empty and list 16-bit members (CIP Vol. 1 7-3.6.11)."""
        text = EDS.replace(
            '"20 04 24 67 30 03", 6, 0x0000, , , 48, ;',
            '"20 04 24 67 30 03", , 0x0000, ,, 16,Param1, 16,Param1, 16,Param1;',
        ).replace(
            'Assem106 = "Config", "20 04 24 6A 30 03", 0, 0x0000, , , ;',
            'Assem106 = "Config", , , 0x0000, ,, 72,, 1,Param1, 1,Param1, 1,Param1, 5,;',
        )
        a = {x["instance"]: x.get("bytes") for x in ed.parse(text.encode())["assemblies"]}
        self.assertEqual(a, {103: 6, 104: 2, 106: 10})
        odd = EDS.replace(
            '"20 04 24 67 30 03", 6, 0x0000, , , 48, ;', '"20 04 24 67 30 03", , 0x0000, ,, 3,Param1;'
        )
        self.assertNotIn("bytes", ed.parse(odd.encode())["assemblies"][0])
        unknown = EDS.replace(
            '"20 04 24 67 30 03", 6, 0x0000, , , 48, ;', '"20 04 24 67 30 03", , 0x0000, ,, Param1,Param1;'
        )
        self.assertNotIn("bytes", ed.parse(unknown.encode())["assemblies"][0])

    def test_path_parameters_resolve_to_their_defaults(self):
        """WAGO's 750-363 picks its connection points by parameter: "2C [Param300] 2C [Param301]"."""
        text = EDS.replace(
            "[Assembly]",
            'Param300 = 0, , , 0x0000, 0xC6, 1, "O->T", "", "", 101, 103, 102, , , , , , , , , 0;\n'
            'Param301 = 0, , , 0x0000, 0xC6, 1, "T->O", "", "", 104, 109, 104, , , , , , , , , 0;\n'
            'Param302 = 0, , , 0x0000, 0xC7, 2, "wide", "", "", 0, 999, 300, , , , , , , , , 0;\n'
            "[Assembly]",
        ).replace('"20 04 24 6A 2C 68 2C 67"', '"20 04 24 01 2C [Param300] 2C [Param301]"')
        c = ed.parse(text.encode())["connections"][0]
        self.assertEqual((c["config_instance"], c["o_to_t_instance"], c["t_to_o_instance"]), (1, 102, 104), c)
        self.assertEqual(c["from_params"], ["Param300", "Param301"])
        for bad in ("[Param302]", "[Param999]", "[Param300"):
            t = text.replace("[Param301]", bad)
            c = ed.parse(t.encode())["connections"][0]
            self.assertNotIn("t_to_o_instance", c, bad)

    def test_connection_sizes_set_by_parameters_are_ranges(self):
        """Phoenix's AXL F BK EIP EF: "Param1,Param3,Assem100" with Param3 2..502, default 2."""
        text = (
            EDS.replace(
                "[Assembly]",
                'Param2 = 0, , , 0x0000, 0xC7, 2, "Input Size", "", "", 2, 502, 2, , , , , , , , , 0;\n'
                'Param3 = 0, , , 0x0000, 0xC7, 2, "Output Size", "", "", 2, 502, 4, , , , , , , , , 0;\n'
                "[Assembly]",
            )
            .replace("Param1, 2, Assem104,", "Param1, Param3, Assem104,")
            .replace(
                "Param1, 6, Assem103,\n                0, ,",
                "Param1, Param2, Assem103,\n                0, ,",
            )
        )
        e = ed.parse(text.encode())
        c = e["connections"][0]
        self.assertNotIn("o_to_t_bytes", c)
        self.assertEqual(c["o_to_t_size"], {"param": "Param3", "min": 2, "max": 502, "default": 4})
        self.assertEqual(c["t_to_o_size"], {"param": "Param2", "min": 2, "max": 502, "default": 2})
        sha = "0" * 64
        t = tomllib.loads(ed.draft(e, {"name": "x.eds", "size": 1, "sha256": sha}, [], "V", "M"))
        enip = t["protocols"]["enip"]
        self.assertNotIn("bytes", enip["input_assembly"])
        self.assertNotIn("bytes", enip["output_assembly"])
        self.assertIn(
            "Param3: 2..502 bytes, default 4",
            ed.draft(e, {"name": "x.eds", "size": 1, "sha256": sha}, [], "V", "M"),
        )

    def test_generic_device_is_remote_io(self):
        """Balluff's BNI EIP-302 declares ProdType 43, "Generic Device"; I/O blocks commonly do."""
        e = ed.parse(EDS.replace("ProdType = 12;", "ProdType = 43;").encode())
        t = tomllib.loads(ed.draft(e, {"name": "x.eds", "size": 1, "sha256": "0" * 64}, [], "V", "M"))
        self.assertEqual(t["device"]["kind"], "remote-io")

    def test_crlf_latin1_and_bom(self):
        text = "﻿" + EDS.replace("Turck", "Türck").replace("\n", "\r\n")
        self.assertEqual(ed.parse(text[1:].encode("latin-1"))["device"]["vendor_name"], "Türck")
        self.assertEqual(ed.parse(text.encode("utf-8"))["device"]["vendor_name"], "Türck")

    def test_epaths(self):
        self.assertEqual(ed.path_instances("20 04 24 80 2C 96 2C 64"), [0x80, 0x96, 0x64])
        self.assertEqual(ed.path_instances("20 04 25 00 2C 01 2C 96 2C 64"), [0x12C, 0x96, 0x64])
        self.assertEqual(ed.path_instances("20 04 24 [Param1]"), [])
        self.assertEqual(ed.path_instances(""), [])
        self.assertEqual(ed.path_instances("20 04 24"), [])

    def test_malformed(self):
        for bad in [
            "",
            "[Device]\nVendCode = 1;\n",  # no product code
            "[Device]\nVendCode = 70000;\nProdCode = 1;\n",
            "VendCode = 1;\n",  # before any section
            '[Device]\nProdName = "open;\n',
            "[Device]\nVendCode = 1; ProdCode = 2",  # no final ';'
            "[Device\nVendCode = 1;\n",
            "[Device]\nVendCode 1;\n",
            "[File]\n",
        ]:
            with self.subTest(bad=bad), self.assertRaises(ed.EdsError):
                ed.parse(bad.encode())
        with self.assertRaises(ed.EdsError):
            ed.parse(b"[Device]\x00")
        with self.assertRaises(ed.EdsError):
            ed.parse(b" " * (ed.MAX_EDS + 1))

    def test_fuzz_only_eds_errors(self):
        """Mutated vectors: parse succeeds or raises EdsError, never anything else."""
        rng = random.Random(55086)
        base = EDS.encode()
        alphabet = b'[];,="$\\\n\r \x00\xff0x9aZ'
        for _ in range(3000):
            b = bytearray(base)
            for _ in range(rng.randint(1, 12)):
                op = rng.randrange(3)
                i = rng.randrange(len(b) + 1)
                if op == 0 and b:
                    del b[min(i, len(b) - 1)]
                elif op == 1:
                    b.insert(i, rng.choice(alphabet))
                else:
                    b[i:i] = bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 8)))
            try:
                ed.parse(bytes(b))
            except ed.EdsError:
                pass


class Draft(unittest.TestCase):
    def folder(self, eds: dict, vendor="Turck", model="TBEN-S2-8DXP"):
        root = pathlib.Path(tempfile.mkdtemp())
        f = root / "devices" / "turck" / "tben-s2-8dxp"
        f.mkdir(parents=True)
        sha = hashlib.sha256(EDS.encode()).hexdigest()
        eds_file = {"name": "x.eds", "size": len(EDS), "sha256": sha, "url": "https://v.example/x.zip"}
        sources = [{"title": "EDS", "sha256": sha, "where": "https://v.example/x.zip; retrieved 2026-11-14"}]
        (f / "device.toml").write_text(ed.draft(eds, eds_file, sources, vendor, model))
        return root, f

    def entry(self, root, f):
        old = bi.ROOT
        bi.ROOT = root
        try:
            return bi.entry(f)
        finally:
            bi.ROOT = old

    def test_draft_passes_the_index(self):
        root, f = self.folder(ed.parse(EDS.encode()))
        t = tomllib.loads((f / "device.toml").read_text())
        self.assertNotIn("checked_on", t["device"])
        self.assertEqual(t["protocols"]["enip"]["input_assembly"], {"instance": 0x67, "bytes": 6})
        self.assertEqual(t["protocols"]["enip"]["output_assembly"], {"instance": 0x68, "bytes": 2})
        self.assertEqual(t["protocols"]["enip"]["config_assembly"], {"instance": 0x6A, "bytes": 0})
        e = self.entry(root, f)
        self.assertEqual(e["identity"], {"enip": {"vendor_id": 48, "product_code": 0x2A1}}, json.dumps(e))
        self.assertEqual(e["kind"], "remote-io")

    def test_hostile_strings_stay_strings(self):
        eds = ed.parse(EDS.encode())
        eds["device"]["product_name"] = 'x"\n[device]\nvendor = "pwned'
        eds["device"]["catalog"] = '"""'
        for name in ("a\\b", "é ☃", '"; rm -rf /'):
            _, f = self.folder(eds, vendor=name, model=name[:3] or "m")
            t = tomllib.loads((f / "device.toml").read_text())
            self.assertEqual(t["device"]["vendor"], name)
            self.assertEqual(t["identity"]["enip"]["product_name"], 'x"\n[device]\nvendor = "pwned')
            self.assertEqual(t["device"]["article"], '"""')

    def test_no_connection_still_drafts(self):
        e = ed.parse(EDS.split("[Connection Manager]")[0].encode())
        root, f = self.folder(e)
        t = tomllib.loads((f / "device.toml").read_text())
        self.assertNotIn("input_assembly", t["protocols"]["enip"])
        self.entry(root, f)


if __name__ == "__main__":
    unittest.main()


class FromLock(unittest.TestCase):
    """A family package (Turck's TBEN-S zip holds 21 EDS) must not draft a folder from a sibling's EDS."""

    def setUp(self):
        self.store = pathlib.Path(tempfile.mkdtemp())
        (self.store / "sha256").mkdir()
        self.members = []
        for name in ("pkg/TBEN-S1-4DIP-4DOP_R2.7.eds", "pkg/TBEN-S2-8DXP_R1.1.eds"):
            body = EDS.replace("TBEN-S2-8DXP", pathlib.PurePosixPath(name).stem).encode()
            sha = hashlib.sha256(body).hexdigest()
            (self.store / "sha256" / sha).write_bytes(body)
            self.members.append({"name": name, "sha256": sha, "size": len(body), "type": "eds"})
        self.lock = {
            "docs": {
                "https://v.example/pkg.zip": {
                    "folders": ["devices/turck/tben-s2-8dxp", "devices/turck/tben-s1-4dip-4dop"],
                    "kind": "eds",
                    "type": "zip",
                    "name": "pkg.zip",
                    "title": "pkg",
                    "sha256": "0" * 64,
                    "size": 1,
                    "retrieved": "2026-11-14T00:00:00Z",
                    "members": self.members,
                }
            }
        }

    def test_several_eds_refuse_to_guess(self):
        with self.assertRaises(SystemExit) as e:
            ed.eds_from_lock(self.lock, "devices/turck/tben-s2-8dxp", self.store)
        self.assertIn("TBEN-S2-8DXP_R1.1.eds", str(e.exception))

    def test_the_named_eds_is_the_one_drafted(self):
        data, f, _ = ed.eds_from_lock(
            self.lock, "devices/turck/tben-s2-8dxp", self.store, "TBEN-S2-8DXP_R1.1.eds"
        )
        self.assertEqual(f["name"], "TBEN-S2-8DXP_R1.1.eds")
        self.assertIn(b"TBEN-S2-8DXP_R1.1", data)

    def test_a_shared_document_serves_each_folder(self):
        _, f, _ = ed.eds_from_lock(
            self.lock, "devices/turck/tben-s1-4dip-4dop", self.store, "TBEN-S1-4DIP-4DOP_R2.7.eds"
        )
        self.assertEqual(f["sha256"], self.members[0]["sha256"])

    def test_a_vendor_name_with_spaces_is_written_with_underscores(self):
        # Balluff's zip names its EDS "BNI EIP-302-105-Z015.eds"; a box
        # refuses the whole index over a space (2026-11-18). The vendor's
        # name still picks the member, the drafted name has none.
        self.members[1]["name"] = "pkg/BNI EIP-302-105-Z015.eds"
        _, f, _ = ed.eds_from_lock(
            self.lock, "devices/turck/tben-s2-8dxp", self.store, "BNI EIP-302-105-Z015.eds"
        )
        self.assertEqual(f["name"], "BNI_EIP-302-105-Z015.eds")
        self.assertEqual(f["sha256"], self.members[1]["sha256"])
        bi.file_name(f["name"], "drafted name")

    def test_names_keep_only_what_a_box_reads(self):
        for vendor, ours in (
            ("A  B.eds", "A_B.eds"),
            ("Ünïcode (v2).EDS", "n_code_v2_.EDS"),
            ("plain-name_1.2.eds", "plain-name_1.2.eds"),
        ):
            with self.subTest(vendor=vendor):
                self.assertEqual(ed.file_name(vendor), ours)
                bi.file_name(ed.file_name(vendor), "x")

    def test_unknown_name_refused(self):
        with self.assertRaises(SystemExit):
            ed.eds_from_lock(self.lock, "devices/turck/tben-s2-8dxp", self.store, "nope.eds")


CONNECTION = """
[Connection Manager]
        Connection1 = 0x04010002, 0x44640405, , 2, Assem2, , 4, Assem1, , 0, , "Exclusive Owner", "", "20 04 24 06 2C 02 2C 01";
[Assembly]
        Assem1 = "in", , 4, , , , ;
        Assem2 = "out", , 2, , , , ;
"""


class Network(unittest.TestCase):
    """An EDS is written for one network. ODVA lists DeviceNet and ControlNet files beside the
    EtherNet/IP ones, and a draft from one of them is an entry for a device nobody can reach
    over Ethernet (two were drafted on 2026-11-22 and removed the next day)."""

    def draft(self, extra):
        e = ed.parse((EDS + extra).encode())
        return ed.draft(e, {"name": "x.eds", "size": 1, "sha256": "0" * 64}, [], "V", "M")

    def test_an_ethernet_ip_classification_drafts(self):
        for classes in (
            "Class1 = EtherNetIP;",
            "Class1 = 1_RSNetWorx_Adapter;\nClass2 = ethernetip;",
            "Class1 = ControlNet;\nClass2 = EtherNetIP;",
        ):
            with self.subTest(classes=classes):
                self.assertIn(
                    "[identity.enip]", self.draft("[Device Classification]\n" + classes + CONNECTION)
                )

    def test_no_classification_drafts_when_the_connections_are_there(self):
        self.assertIn("[identity.enip]", self.draft(CONNECTION))

    def test_a_controlnet_or_devicenet_classification_is_refused_by_name(self):
        for classes, name in (
            ("Class1 = 1_RSNetWorx_Adapter;\nClass2 = ControlNet;", "ControlNet"),
            ("Class1 = DeviceNet;", "DeviceNet"),
            ("Class1 = CompoNet;", "CompoNet"),
        ):
            with self.subTest(classes=classes), self.assertRaises(ed.EdsError) as c:
                self.draft("[Device Classification]\n" + classes + CONNECTION)
            self.assertIn(name, str(c.exception))
            self.assertIn("EtherNet/IP", str(c.exception))

    def test_a_devicenet_file_with_no_classification_is_refused(self):
        """As ODVA's VS_32.eds was: [IO_Info] for its I/O and no [Connection Manager]."""
        text = (
            "[File]\n Revision = 2.8;\n[Device]\n VendCode = 42;\n ProdType = 27;\n ProdCode = 332;\n"
            ' MajRev = 2;\n MinRev = 8;\n ProdName = "VSxx 32";\n'
            "[IO_Info]\n Default = 0x0001;\n PollInfo = 0x0001, 1, 1;\n"
            ' Output1 = 4, 0, 0x0001, "Outputs", 6, "20 04 24 23 30 03", "";\n'
        )
        e = ed.parse(text.encode())
        with self.assertRaises(ed.EdsError) as c:
            ed.draft(e, {"name": "x.eds", "size": 1, "sha256": "0" * 64}, [], "V", "M")
        self.assertIn("DeviceNet", str(c.exception))

    def test_show_still_reads_such_a_file_and_says_what_it_is(self):
        e = ed.parse((EDS + "[Device Classification]\nClass1 = ControlNet;\n" + CONNECTION).encode())
        self.assertEqual(e["device"]["product_name"], "TBEN-S2-8DXP block")
        self.assertIn("ControlNet", e["not_ethernet_ip"])
