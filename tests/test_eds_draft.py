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
