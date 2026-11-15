"""scripts/iodd-draft.py: the IODD reader on a written description and fuzzed bytes, and the draft it writes.

The description is written here against the IODD 1.1 schemas, not copied
from a vendor's file: a vendor's IODD has no redistribution terms. A draft
is held to what build-index.py accepts, so a drafted folder can be
committed without hand edits.
"""

import contextlib
import importlib.util
import io
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


iod = load("iodd_draft", "iodd-draft.py")
bi = load("build_index", "build-index.py")

IODD = """<?xml version="1.0" encoding="UTF-8"?>
<!-- a description written for the tests, not a real device -->
<IODevice xmlns="http://www.io-link.com/IODD/2010/10" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <DocumentInfo version="V1.2" releaseDate="2026-11-14" copyright="none"/>
  <ProfileBody>
    <DeviceIdentity vendorId="310" vendorName="Bench &amp; Co" deviceId="666">
      <VendorText textId="T_Vendor"/>
      <VendorUrl textId="T_Url"/>
      <DeviceName textId="T_Device"/>
      <DeviceFamily textId="T_Family"/>
      <DeviceVariantCollection>
        <DeviceVariant productId="BX-12 PNP">
          <Name textId="T_VarA"/><Description textId="T_VarADescr"/>
        </DeviceVariant>
        <DeviceVariant productId="BX-12 cable"><Name textId="T_Missing"/></DeviceVariant>
      </DeviceVariantCollection>
    </DeviceIdentity>
    <DeviceFunction>
      <DatatypeCollection>
        <Datatype id="D_Switch" xsi:type="BooleanT">
          <SingleValue value="false"><Name textId="T_Free"/></SingleValue>
          <SingleValue value="true"><Name textId="T_Target"/></SingleValue>
        </Datatype>
        <Datatype id="D_In" xsi:type="RecordT" bitLength="32">
          <RecordItem subindex="3" bitOffset="0"><DatatypeRef datatypeId="D_Switch"/><Name textId="T_Sw1"/>
            <Description textId="T_Sw1Descr"/></RecordItem>
          <RecordItem subindex="1" bitOffset="16"><SimpleDatatype xsi:type="IntegerT" bitLength="16"/>
            <Name textId="T_Dist"/></RecordItem>
          <RecordItem subindex="2" bitOffset="8"><SimpleDatatype xsi:type="UIntegerT" bitLength="8">
            <SingleValue value="255"><Name textId="T_NoEcho"/></SingleValue></SimpleDatatype>
            <Name textId="T_Qual"/></RecordItem>
          <RecordItem subindex="4" bitOffset="1"><DatatypeRef datatypeId="D_Switch"/><Name textId="T_Sw2"/></RecordItem>
        </Datatype>
      </DatatypeCollection>
      <ProcessDataCollection>
        <ProcessData id="P_PD">
          <ProcessDataIn id="PI" bitLength="32"><DatatypeRef datatypeId="D_In"/><Name textId="T_In"/></ProcessDataIn>
          <ProcessDataOut id="PO" bitLength="8">
            <Datatype xsi:type="BooleanT"/><Name textId="T_Teach"/>
          </ProcessDataOut>
        </ProcessData>
      </ProcessDataCollection>
    </DeviceFunction>
  </ProfileBody>
  <CommNetworkProfile xsi:type="IOLinkCommNetworkProfileT" iolinkRevision="V1.1">
    <TransportLayers>
      <PhysicalLayer bitrate="COM2" minCycleTime="2300" sioSupported="true" mSequenceCapability="27">
        <Connection xsi:type="M12-4ConnectionT">
          <ProductRef productId="BX-12 PNP"/>
          <Wire1 function="L+"/><Wire2 function="Other"/><Wire3 function="L-"/><Wire4 function="C/Q"/>
        </Connection>
        <Connection xsi:type="CableConnectionT">
          <ProductRef productId="BX-12 cable"/>
          <Wire1 function="L+" color="BN"/>
          <Wire2 function="Other" color="WH"><Name textId="T_Q2"/></Wire2>
          <Wire3 function="L-" color="BU"/>
          <Wire4 function="C/Q" color="BK"/>
        </Connection>
      </PhysicalLayer>
    </TransportLayers>
  </CommNetworkProfile>
  <ExternalTextCollection>
    <PrimaryLanguage xml:lang="en">
      <Text id="T_Vendor" value="Sensors since 1950"/>
      <Text id="T_Url" value="https://bench.example"/>
      <Text id="T_Device" value="BX-12 inductive sensor"/>
      <Text id="T_Family" value="BX inductive"/>
      <Text id="T_VarA" value="BX-12, M12 plug"/>
      <Text id="T_VarADescr" value="12 mm, PNP, normally open"/>
      <Text id="T_Free" value="No target"/>
      <Text id="T_Target" value="Target present"/>
      <Text id="T_Sw1" value="Switching signal 1"/>
      <Text id="T_Sw1Descr" value="On while a target is inside the set distance"/>
      <Text id="T_Sw2" value="Switching signal 2"/>
      <Text id="T_Dist" value="Distance"/>
      <Text id="T_Qual" value="Signal quality"/>
      <Text id="T_NoEcho" value="No echo"/>
      <Text id="T_In" value="Measurement"/>
      <Text id="T_Teach" value="Teach"/>
      <Text id="T_Q2" value="Q2 (second switching output)"/>
    </PrimaryLanguage>
    <Language xml:lang="de"><Text id="T_Device" value="BX-12 induktiver Sensor"/></Language>
  </ExternalTextCollection>
</IODevice>
"""

URL = "https://bench.example/iodd/BX-12-20261114-IODD1.1.zip"


class Read(unittest.TestCase):
    def setUp(self):
        self.iodd = iod.parse(IODD.encode())

    def test_identity_and_variants(self):
        d = self.iodd
        self.assertEqual((d["vendor_id"], d["device_id"]), (310, 666))
        self.assertEqual(d["vendor_name"], "Bench & Co")
        self.assertEqual(d["device_name"], "BX-12 inductive sensor")
        self.assertEqual(d["family"], "BX inductive")
        self.assertEqual(d["vendor_url"], "https://bench.example")
        self.assertEqual((d["iodd_version"], d["iodd_date"]), ("V1.2", "2026-11-14"))
        self.assertEqual(
            d["variants"],
            [
                {
                    "product_id": "BX-12 PNP",
                    "name": "BX-12, M12 plug",
                    "description": "12 mm, PNP, normally open",
                },
                # no such text in the primary language: the reference stands in
                {"product_id": "BX-12 cable", "name": "T_Missing"},
            ],
        )

    def test_wiring(self):
        d = self.iodd
        self.assertIs(d["sio"], True)
        self.assertEqual((d["bitrate"], d["min_cycle_us"]), ("COM2", 2300))
        plug, cable = d["connections"]
        self.assertEqual((plug["type"], plug["products"]), ("M12-4", ["BX-12 PNP"]))
        self.assertEqual([w["function"] for w in plug["wires"]], ["L+", "Other", "L-", "C/Q"])
        self.assertEqual(cable["type"], "Cable")
        self.assertEqual(
            cable["wires"][1],
            {"n": 2, "function": "Other", "color": "WH", "name": "Q2 (second switching output)"},
        )
        self.assertEqual(cable["wires"][3], {"n": 4, "function": "C/Q", "color": "BK"})

    def test_signals_by_name_in_subindex_order(self):
        (layout,) = self.iodd["process_data"]
        self.assertEqual(layout["in"]["bit_length"], 32)
        got = [(s["name"], s["type"], s["bit_offset"], s["bit_length"]) for s in layout["in"]["signals"]]
        self.assertEqual(
            got,
            [
                ("Distance", "int", 16, 16),
                ("Signal quality", "uint", 8, 8),
                ("Switching signal 1", "bool", 0, 1),
                ("Switching signal 2", "bool", 1, 1),
            ],
        )
        sw1 = layout["in"]["signals"][2]
        self.assertEqual(sw1["values"], {"false": "No target", "true": "Target present"})
        self.assertEqual(sw1["description"], "On while a target is inside the set distance")
        self.assertEqual(layout["in"]["signals"][1]["values"], {"255": "No echo"})
        self.assertEqual(
            layout["out"]["signals"],
            [{"name": "Teach", "subindex": 0, "bit_offset": 0, "type": "bool", "bit_length": 1}],
        )

    def test_an_array_packs_its_highest_subindex_at_the_right(self):
        text = IODD.replace(
            '<Datatype xsi:type="BooleanT"/><Name textId="T_Teach"/>',
            '<Datatype xsi:type="ArrayT" count="4"><SimpleDatatype xsi:type="UIntegerT" bitLength="2"/></Datatype>'
            '<Name textId="T_Teach"/>',
        )
        out = iod.parse(text.encode())["process_data"][0]["out"]["signals"]
        self.assertEqual(
            [(s["name"], s["bit_offset"]) for s in out],
            [("Teach 1", 6), ("Teach 2", 4), ("Teach 3", 2), ("Teach 4", 0)],
        )

    def test_conditional_layouts_keep_their_condition(self):
        one = IODD[IODD.index("<ProcessData id=") : IODD.index("</ProcessData>") + len("</ProcessData>")]
        two = one.replace('id="P_PD">', 'id="P_B"><Condition variableId="V_Mode" value="1"/>').replace(
            'id="PI"', 'id="PI2"'
        )
        first = one.replace('id="P_PD">', 'id="P_A"><Condition variableId="V_Mode" value="0"/>')
        d = iod.parse(IODD.replace(one, first + two).encode())
        self.assertEqual(
            [(p["id"], p["condition"]) for p in d["process_data"]],
            [("P_A", {"variable": "V_Mode", "value": 0}), ("P_B", {"variable": "V_Mode", "value": 1})],
        )

    def test_a_device_with_no_process_data_or_profile_reads(self):
        text = IODD[: IODD.index("<ProcessDataCollection>")] + IODD[IODD.index("</DeviceFunction>") :]
        text = text[: text.index("<CommNetworkProfile")] + text[text.index("<ExternalTextCollection>") :]
        d = iod.parse(text.encode())
        self.assertEqual((d["process_data"], d["connections"]), ([], []))
        self.assertNotIn("sio", d)
        self.assertEqual(iod.guess_kind(d), "other")

    def test_malformed(self):
        cases = [
            ("<IODevice ", '<!DOCTYPE x [<!ENTITY a "aaaa">]><IODevice ', "DOCTYPE"),
            ('vendorId="310"', 'vendorId="0"', "from 1 to 65535"),
            ('vendorId="310"', 'vendorId="0x136"', "not a number"),
            ('vendorId="310" ', "", "no vendorId="),
            ('deviceId="666"', 'deviceId="16777216"', "from 1 to 16777215"),
            ('vendorName="Bench &amp; Co"', 'vendorName=" "', "no vendorName="),
            ('<DeviceName textId="T_Device"/>', "", "no <DeviceName textId=>"),
            ('sioSupported="true"', 'sioSupported="maybe"', "true or false"),
            ('minCycleTime="2300"', 'minCycleTime="-1"', "not a number"),
            (
                '<DatatypeRef datatypeId="D_In"/>',
                '<DatatypeRef datatypeId="D_Gone"/>',
                "no Datatype with id 'D_Gone'",
            ),
            ('<DatatypeRef datatypeId="D_In"/>', "", "has no data type"),
            ('id="PI" bitLength="32"', 'id="PI" bitLength="24"', "a record of 32 bits as 24"),
            ('id="PI" bitLength="32"', 'id="PI" bitLength="257"', "from 1 to 256"),
            ('subindex="1" bitOffset="16"', 'subindex="1" bitOffset="17"', "ends at bit 33 of 32"),
            ('subindex="2" bitOffset="8"', 'subindex="2" bitOffset="12"', "shares bits"),
            ('xsi:type="IntegerT" bitLength="16"', 'xsi:type="IntegerT" bitLength="65"', "from 2 to 64"),
            (
                'xsi:type="IntegerT" bitLength="16"',
                'xsi:type="RecordT" bitLength="16"',
                "where a simple type is needed",
            ),
            (
                '<Datatype xsi:type="BooleanT"/>',
                '<Datatype xsi:type="ProcessDataOutUnionT"/>',
                "where a simple type",
            ),
            ('<Datatype xsi:type="BooleanT"/>', "<Datatype/>", "where a simple type"),
            ("</IODevice>", "", "not well-formed"),
        ]
        for old, new, why in cases:
            self.assertIn(old, IODD, old)
            with self.assertRaises(iod.IoddError, msg=new) as caught:
                iod.parse(IODD.replace(old, new, 1).encode())
            self.assertIn(why, str(caught.exception), new)
            self.assertLess(len(str(caught.exception)), 300)
        with self.assertRaises(iod.IoddError) as caught:
            iod.parse(IODD.replace("IODevice", "Device").encode())
        self.assertIn("not an IODD", str(caught.exception))
        with self.assertRaises(iod.IoddError) as caught:
            iod.parse(IODD.replace("PrimaryLanguage", "OtherLanguage").encode())
        self.assertIn("no <PrimaryLanguage>", str(caught.exception))
        with self.assertRaises(iod.IoddError) as caught:
            iod.parse(IODD.replace('encoding="UTF-8"', 'encoding="UT-8"').encode())
        self.assertIn("not readable XML", str(caught.exception))
        with self.assertRaises(iod.IoddError):
            iod.parse(b" " * (iod.MAX_IODD + 1))
        with self.assertRaises(iod.IoddError):
            iod.parse(b"<a>" * 100000 + b"</a>" * 100000)
        with self.assertRaises(iod.IoddError):
            iod.parse(b"\xff\xfe\x00")

    def test_fuzz_only_iodd_errors(self):
        """Mutated descriptions: parse succeeds or raises IoddError, never anything else."""
        rng = random.Random(10012)
        base = IODD.encode()
        alphabet = b'<>/="&;: \n\x00\xffTt0129'
        for _ in range(1500):
            b = bytearray(base)
            for _ in range(rng.randint(1, 8)):
                op = rng.randrange(3)
                i = rng.randrange(len(b) + 1)
                if op == 0:
                    del b[min(i, len(b) - 1)]
                elif op == 1:
                    b.insert(i, rng.choice(alphabet))
                else:
                    b[i:i] = bytes(rng.getrandbits(8) for _ in range(rng.randint(1, 8)))
            try:
                iod.parse(bytes(b))
            except iod.IoddError:
                pass


class Draft(unittest.TestCase):
    def run_main(self, argv, root):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = iod.main(argv, root=root)
        return code, out.getvalue()

    def drafted(self, text=IODD, extra=()):
        root = pathlib.Path(tempfile.mkdtemp())
        src = root / "BX-12-IODD1.1.xml"
        src.write_text(text)
        folder = "devices/bench/bx-12"
        code, said = self.run_main(["draft", str(src), folder, "--url", URL, *extra], root)
        self.assertEqual(code, 0, said)
        return root, root / folder

    def entry(self, root, f):
        old = bi.ROOT
        bi.ROOT = root
        try:
            return bi.entry(f)
        finally:
            bi.ROOT = old

    def test_draft_says_what_the_iodd_says_and_passes_the_index(self):
        root, f = self.drafted()
        t = tomllib.loads((f / "device.toml").read_text())
        self.assertEqual(
            t["device"],
            {
                "vendor": "Bench & Co",
                "model": "BX-12 inductive sensor",
                "kind": "sensor",
                "family": "BX inductive",
                "vendor_url": "https://bench.example",
            },
        )
        self.assertNotIn("checked_on", t["device"])
        self.assertNotIn("protocols", t)
        self.assertEqual(t["identity"], {"iolink": {"vendor_id": 310, "device_id": 666}})
        self.assertEqual([v["product_id"] for v in t["variants"]], ["BX-12 PNP", "BX-12 cable"])
        self.assertIs(t["wired"]["sio"], True)
        # Nothing claims which signal the wire carries.
        self.assertNotIn("switching", t["wired"])
        self.assertEqual(t["wired"]["connections"][1]["wires"][1]["name"], "Q2 (second switching output)")
        sw1 = next(s for s in t["signals"] if s["name"] == "Switching signal 1")
        self.assertEqual(
            sw1,
            {
                "dir": "in",
                "name": "Switching signal 1",
                "type": "bool",
                "bits": "0",
                "description": "On while a target is inside the set distance",
                "off": "No target",
                "on": "Target present",
            },
        )
        self.assertEqual(next(s for s in t["signals"] if s["name"] == "Distance")["bits"], "16..31")
        self.assertEqual(
            next(s for s in t["signals"] if s["name"] == "Signal quality")["values"], {"255": "No echo"}
        )
        data = (root / "BX-12-IODD1.1.xml").read_bytes()
        self.assertEqual(
            t["iodd"]["file"],
            {
                "name": "BX-12-IODD1.1.xml",
                "size": len(data),
                "sha256": __import__("hashlib").sha256(data).hexdigest(),
                "url": URL,
            },
        )
        e = self.entry(root, f)
        self.assertEqual(e["identity"], {"iolink": {"vendor_id": 310, "device_id": 666}}, json.dumps(e))
        self.assertEqual((e["kind"], e["vendor"]), ("sensor", "Bench & Co"))
        readme = (f / "README.md").read_text()
        self.assertIn("Draft from documents", readme)
        self.assertIn(
            "| in | Switching signal 1 | bool | 0 | false = No target, true = Target present |", readme
        )
        self.assertIn("2: Other (WH)", readme)

    def test_names_and_kind_can_be_given(self):
        _, f = self.drafted(extra=("--vendor", "Bench", "--model", "BX-12", "--kind", "other"))
        t = tomllib.loads((f / "device.toml").read_text())
        self.assertEqual(
            (t["device"]["vendor"], t["device"]["model"], t["device"]["kind"]), ("Bench", "BX-12", "other")
        )

    def test_outputs_alone_make_an_actuator(self):
        text = IODD.replace(
            '<ProcessDataIn id="PI" bitLength="32"><DatatypeRef datatypeId="D_In"/><Name textId="T_In"/></ProcessDataIn>',
            "",
        )
        _, f = self.drafted(text)
        self.assertEqual(tomllib.loads((f / "device.toml").read_text())["device"]["kind"], "actuator")

    def test_hostile_texts_stay_texts(self):
        hostile = "x&quot;&#10;[device]&#10;vendor = &quot;pwned | &lt;script&gt; " + "y" * 400
        text = IODD.replace('value="Switching signal 1"', f'value="{hostile}"').replace(
            'vendorName="Bench &amp; Co"', 'vendorName="a\\b &quot;; rm -rf / é ☃"'
        )
        root, f = self.drafted(text)
        t = tomllib.loads((f / "device.toml").read_text())
        self.assertEqual(t["device"]["vendor"], 'a\\b "; rm -rf / é ☃')
        self.assertEqual(t["device"]["kind"], "sensor")
        name = next(s for s in t["signals"] if s["bits"] == "0" and s["dir"] == "in")["name"]
        self.assertTrue(name.startswith('x" [device] vendor = "pwned | <script> yyy'), name)
        self.assertEqual(len(name), 120)
        self.entry(root, f)
        for line in (f / "README.md").read_text().splitlines():
            if "pwned" in line:
                self.assertEqual(line.count("|"), 6, line)

    def test_what_draft_refuses(self):
        root = pathlib.Path(tempfile.mkdtemp())
        src = root / "x.xml"
        src.write_text(IODD)
        ok = ["draft", str(src), "devices/bench/bx-12", "--url", URL]
        for argv, why in [
            (ok[:3], "--url"),
            (ok[:3] + ["--url", "http://bench.example/x.zip"], "--url"),
            (ok[:3] + ["--url", 'https://bench.example/"x'], "--url"),
            (ok[:3] + ["--url"], "--url needs a value"),
            (ok + ["--kind", "robot"], "--kind"),
            (ok[:2] + ["devices/Bench/BX", "--url", URL], "FOLDER must be"),
            (ok[:2] + ["../devices/bench/x", "--url", URL], "FOLDER must be"),
            (["draft", str(root / "none.xml"), "devices/bench/bx-12", "--url", URL], "no such file"),
        ]:
            with self.assertRaises(SystemExit, msg=argv) as caught:
                self.run_main(argv, root)
            self.assertIn(why, str(caught.exception), argv)
        self.assertFalse((root / "devices").exists())
        bad = root / "bad.xml"
        bad.write_text(IODD.replace("IODevice", "Device"))
        with self.assertRaises(SystemExit) as caught:
            self.run_main(["draft", str(bad), "devices/bench/bx-12", "--url", URL], root)
        self.assertIn("bad.xml: ", str(caught.exception))
        self.assertFalse((root / "devices").exists())

    def test_an_existing_record_is_kept_without_force(self):
        root, f = self.drafted()
        (f / "device.toml").write_text("# checked by hand\n")
        (f / "README.md").write_text("# mine\n")
        src = str(root / "BX-12-IODD1.1.xml")
        with self.assertRaises(SystemExit) as caught:
            self.run_main(["draft", src, "devices/bench/bx-12", "--url", URL], root)
        self.assertIn("--force", str(caught.exception))
        self.assertEqual((f / "device.toml").read_text(), "# checked by hand\n")
        code, _ = self.run_main(["draft", src, "devices/bench/bx-12", "--url", URL, "--force"], root)
        self.assertEqual(code, 0)
        self.assertIn("[identity.iolink]", (f / "device.toml").read_text())
        self.assertIn("Draft from documents", (f / "README.md").read_text())

    def test_show_prints_what_was_read(self):
        root = pathlib.Path(tempfile.mkdtemp())
        src = root / "x.xml"
        src.write_text(IODD)
        code, said = self.run_main(["show", str(src)], root)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(said), iod.parse(IODD.encode()))
        code, said = self.run_main(["help"], root)
        self.assertEqual(code, 2)
        self.assertIn("iodd-draft.py draft IODD FOLDER", said)


class Index(unittest.TestCase):
    def entry(self, identity: str):
        root = pathlib.Path(tempfile.mkdtemp())
        f = root / "devices" / "v" / "m"
        f.mkdir(parents=True)
        (f / "device.toml").write_text(f'[device]\nvendor = "V"\nmodel = "M"\nkind = "sensor"\n{identity}')
        old = bi.ROOT
        bi.ROOT = root
        try:
            return bi.entry(f)
        finally:
            bi.ROOT = old

    def test_an_iolink_identity_is_indexed(self):
        e = self.entry("[identity.iolink]\nvendor_id = 310\ndevice_id = 16777215\n")
        self.assertEqual(e["identity"], {"iolink": {"vendor_id": 310, "device_id": 16777215}})
        self.assertNotIn("protocols", e)

    def test_a_wrong_iolink_identity_is_refused(self):
        for identity in (
            "[identity.iolink]\nvendor_id = 0\ndevice_id = 1\n",
            "[identity.iolink]\nvendor_id = 65536\ndevice_id = 1\n",
            "[identity.iolink]\nvendor_id = 1\ndevice_id = 16777216\n",
            '[identity.iolink]\nvendor_id = "310"\ndevice_id = 1\n',
            "[identity.iolink]\nvendor_id = true\ndevice_id = 1\n",
            "[identity.iolink]\nvendor_id = 310\n",
        ):
            with self.assertRaises(SystemExit, msg=identity) as caught:
                self.entry(identity)
            self.assertIn("identity.iolink needs", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
