"""scripts/modbus-read.py over real TCP, against a stub Modbus server on 127.0.0.1.

The stub answers from a small table of bits and registers and records the
function code of every request, so the tests can hold the script to reads
only. A test can also hand it a function that rewrites the reply, to play a
device that lies: the script must say so and stop, never hang or crash.
"""

import contextlib
import importlib.util
import io
import pathlib
import random
import socketserver
import struct
import threading
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "modbus-read.py"
spec = importlib.util.spec_from_file_location("modbus_read", SCRIPT)
mb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mb)

IDENT = {0: b"Moxa", 1: b"E1213", 2: b"V3.1"}


class Device:
    """What the stub serves, and what it saw."""

    def __init__(self):
        self.bits = {1: [0] * 4096, 2: [0] * 4096}  # function code -> values by address
        self.regs = {3: [0] * 4096, 4: [0] * 4096}
        self.ident = dict(IDENT)
        self.refuse = {}  # function code -> exception code
        self.mangle = None  # (request frame, reply frame) -> bytes to send instead
        self.seen = []  # function code of every request

    def pdu(self, req):
        fc = req[0]
        self.seen.append(fc)
        if fc in self.refuse:
            return bytes([fc | 0x80, self.refuse[fc]])
        if fc in (1, 2):
            start, n = struct.unpack(">HH", req[1:5])
            vals, out = self.bits[fc][start : start + n], bytearray((n + 7) // 8)
            for i, v in enumerate(vals):
                out[i >> 3] |= v << (i & 7)
            return bytes([fc, len(out)]) + bytes(out)
        if fc in (3, 4):
            start, n = struct.unpack(">HH", req[1:5])
            return bytes([fc, 2 * n]) + struct.pack(f">{n}H", *self.regs[fc][start : start + n])
        if fc == 0x2B:
            objs = b"".join(bytes([k, len(v)]) + v for k, v in sorted(self.ident.items()))
            return bytes([0x2B, 0x0E, 0x01, 0x01, 0x00, 0x00, len(self.ident)]) + objs
        return bytes([fc | 0x80, 1])


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        dev = self.server.dev
        while True:
            try:
                head = self.request.recv(7)
            except OSError:  # the script hung up on a reply it would not take
                return
            if len(head) < 7:
                return
            tid, _proto, length, unit = struct.unpack(">HHHB", head)
            req = self.request.recv(length - 1)
            pdu = dev.pdu(req)
            frame = struct.pack(">HHHB", tid, 0, len(pdu) + 1, unit) + pdu
            if dev.mangle:
                frame = dev.mangle(head + req, frame)
                if frame is None:
                    return
            self.request.sendall(frame)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


class Stubbed(unittest.TestCase):
    def setUp(self):
        self.dev = Device()
        self.server = Server(("127.0.0.1", 0), Handler)
        self.server.dev = self.dev
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.addr = f"127.0.0.1:{self.server.server_address[1]}"
        old = mb.TIMEOUT_S
        mb.TIMEOUT_S = 0.3
        self.addCleanup(setattr, mb, "TIMEOUT_S", old)

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = mb.main([self.addr, *args])
        return code, out.getvalue(), err.getvalue()


class Reads(Stubbed):
    def test_bits_registers_and_identity_print_as_documented(self):
        self.dev.bits[2][0] = self.dev.bits[2][11] = 1
        self.dev.bits[1][1] = 1
        self.dev.regs[4][16:20] = [0, 1, 0xBEEF, 0]
        self.dev.regs[3][300] = 0x0102
        code, out, err = self.run_main("di:0..di:11", "coil:0..7", "ir:16:u32..ir:18:u32", "hr:300")
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(
            out.splitlines(),
            [
                "# 127.0.0.1: Read Device Identification (function 43/14), unit 1",
                "[identity.modbus]",
                "vendor_name = 'Moxa'",
                "product_code = 'E1213'",
                "revision = 'V3.1'",
                "# di 0..11: 100000000001",
                "# coil 0..7: 01000000",
                "# ir 16..19: 0000 0001 beef 0000",
                "# hr 300: 0102",
            ],
        )

    def test_only_read_function_codes_are_ever_sent(self):
        self.run_main("di:0..di:11", "coil:0..7", "ir:0..ir:9", "hr:0..hr:9")
        self.assertEqual(set(self.dev.seen), {1, 2, 3, 4, 0x2B})

    def test_a_long_range_is_split_at_the_protocol_limits(self):
        self.dev.bits[2][2499] = 1
        self.dev.regs[4][129] = 7
        code, out, _ = self.run_main("di:0..2499", "ir:0..129")
        self.assertEqual(code, 0)
        self.assertEqual(self.dev.seen.count(2), 2)  # 2000 + 500
        self.assertEqual(self.dev.seen.count(4), 2)  # 125 + 5
        lines = out.splitlines()
        self.assertEqual(lines[-2], "# di 0..2499: " + "0" * 2499 + "1")
        self.assertTrue(lines[-1].endswith(" 0007"))
        self.assertEqual(len(lines[-1].split(": ")[1].split()), 130)

    def test_the_unit_id_is_sent_and_checked(self):
        code, out, _ = self.run_main("--unit", "17", "hr:0")
        self.assertEqual(code, 0)
        self.assertIn("unit 17", out)

    def test_a_refused_range_is_reported_and_the_rest_still_reads(self):
        self.dev.refuse = {2: 2, 0x2B: 1}
        code, out, err = self.run_main("di:0..3", "hr:0")
        self.assertEqual((code, err), (1, ""))
        self.assertIn("# device identification: refused (exception 1)", out)
        self.assertIn("# di 0..3: refused (exception 2)", out)
        self.assertIn("# hr 0: 0000", out)

    def test_a_device_without_identification_is_not_a_failure(self):
        # The bench ioLogik E1213 (firmware 3.1) answers function 43 with exception 1.
        self.dev.refuse = {0x2B: 1}
        self.dev.bits[2][2] = 1
        code, out, err = self.run_main("di:0..di:11")
        self.assertEqual((code, err), (0, ""))
        self.assertNotIn("[identity.modbus]", out)
        self.assertEqual(out.splitlines()[-1], "# di 0..11: 001000000000")

    def test_a_device_name_cannot_break_out_of_its_line(self):
        self.dev.ident[1] = b'E1\'\n[device]\nvendor = "x"\x00\xff'
        _, out, _ = self.run_main()
        line = [ln for ln in out.splitlines() if ln.startswith("product_code")]
        self.assertEqual(line, ["""product_code = 'E1\\'[device]vendor = "x"'"""])
        self.assertEqual(len(out.splitlines()), 5)

    def test_identification_that_never_ends_is_cut_off(self):
        calls = []

        def more(_req, frame):
            calls.append(1)
            return frame[:11] + bytes([0xFF, len(calls)]) + frame[13:]

        self.dev.mangle = more
        code, _, _ = self.run_main()
        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 8)


class Lies(Stubbed):
    """A device, or something in its place, that does not answer as Modbus says."""

    def refused(self, mangle, *args):
        self.dev.mangle = mangle
        code, out, err = self.run_main(*(args or ("hr:0..3",)))
        self.assertEqual(code, 1, (out, err))
        self.assertTrue(err.startswith("127.0.0.1: "), err)
        self.assertNotIn("Traceback", err)
        return err

    def test_wrong_transaction(self):
        self.refused(lambda _q, f: struct.pack(">H", 999) + f[2:])

    def test_wrong_protocol_id(self):
        self.refused(lambda _q, f: f[:2] + b"\x00\x01" + f[4:])

    def test_wrong_unit(self):
        self.refused(lambda _q, f: f[:6] + b"\x09" + f[7:])

    def test_length_too_small_or_too_large(self):
        for length in (0, 1, 2, 255, 65535):
            with self.subTest(length=length):
                self.refused(lambda _q, f, n=length: f[:4] + struct.pack(">H", n) + f[6:])

    def test_another_function_in_the_reply(self):
        self.refused(lambda q, f: f[:7] + b"\x04" + f[8:] if q[7] == 3 else f)

    def test_byte_count_that_does_not_match(self):
        self.refused(lambda q, f: f[:8] + b"\x02" + f[9:] if q[7] == 3 else f)

    def test_fewer_data_bytes_than_asked_for(self):
        def short(q, f):
            if q[7] != 3:
                return f
            pdu = f[7:9] + f[9:-2]
            return f[:4] + struct.pack(">H", len(pdu) + 1) + f[6:7] + pdu

        self.refused(short)

    def test_closing_instead_of_answering(self):
        self.refused(lambda _q, _f: None)

    def test_half_a_header_then_silence(self):
        err = self.refused(lambda _q, f: f[:3])
        self.assertIn("timed out", err)

    def test_an_identification_object_longer_than_the_reply(self):
        self.refused(lambda q, f: f[:15] + b"\xf0" + f[16:] if q[7] == 0x2B else f)

    def test_random_bytes_never_crash_it(self):
        rnd = random.Random(20261115)
        for _ in range(60):
            junk = bytes(rnd.randrange(256) for _ in range(rnd.randrange(0, 40)))
            self.dev.mangle = lambda _q, _f, j=junk: j or None
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = mb.main([self.addr, "di:0..9", "ir:0..3"])
            self.assertIn(code, (0, 1), junk.hex())
            self.assertNotIn("Traceback", err.getvalue())

    def test_nothing_listening(self):
        self.server.shutdown()
        self.server.server_close()
        code, _, err = self.run_main("hr:0")
        self.assertEqual(code, 1)
        self.assertTrue(err.startswith("127.0.0.1: "))


class Ranges(unittest.TestCase):
    def test_the_forms_the_library_writes(self):
        for text, want in {
            "di:0..di:11": ("di", 0, 12),
            "coil:0..7": ("coil", 0, 8),
            "hr:300": ("hr", 300, 1),
            "ir:16:u32..ir:38:u32": ("ir", 16, 24),
            "ir:16:u32 .. ir:38:u32": ("ir", 16, 24),
            "ir:1536:i16..ir:1541:i16": ("ir", 1536, 6),
            "hr:0:f32": ("hr", 0, 2),
            "ir:65535": ("ir", 65535, 1),
            "hr:0..65535": ("hr", 0, 65536),
        }.items():
            with self.subTest(text=text):
                self.assertEqual(mb.parse_range(text), want)

    def test_what_is_not_a_range(self):
        for text in (
            "",
            "di",
            "di:",
            "di:-1",
            "di:0..",
            "di:5..2",
            "di:0..coil:3",
            "di:0:u32",
            "coil:0..3:u16",
            "ir:0:u64",
            "ir:65535:u32",
            "ir:65536",
            "ir:0..65536",
            "ir:999999",
            "xx:0",
            "ir:0;hr:0",
            "ir:0..1..2",
            "ir:0x10",
            "ir:١",
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                mb.parse_range(text)

    def test_a_bad_command_line_is_refused_before_any_connection(self):
        for args in (
            ["127.0.0.1:1", "nonsense"],
            ["127.0.0.1:1", "--unit"],
            ["127.0.0.1:1", "--unit", "256", "hr:0"],
            ["127.0.0.1:1", "--unit", "x", "hr:0"],
            ["127.0.0.1:1", "--unit", "²", "hr:0"],
            ["127.0.0.1:٥٠٢", "--unit", "x"],
            [":502", "hr:0"],
            ["127.0.0.1:0", "hr:0"],
            ["127.0.0.1:65536", "hr:0"],
            ["127.0.0.1:1", "hr:0..65535", "ir:0"],
        ):
            with self.subTest(args=args):
                err = io.StringIO()
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                    self.assertEqual(mb.main(args), 2)
                self.assertTrue(err.getvalue().strip())

    def test_no_arguments_prints_the_usage(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(mb.main([]), 2)
        self.assertIn("Usage:", out.getvalue())


if __name__ == "__main__":
    unittest.main()
