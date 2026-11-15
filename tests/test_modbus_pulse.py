"""scripts/modbus-pulse.py against a stub Modbus server on 127.0.0.1.

The script switches a real output, so what is held here is what it must
never do: write without a person's word on a terminal, write more than
the one coil, or leave the coil switched when anything goes wrong on the
way. The stub records every request and every coil write.
"""

import contextlib
import importlib.util
import io
import os
import pathlib
import re
import socketserver
import struct
import subprocess
import sys
import threading
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "modbus-pulse.py"
spec = importlib.util.spec_from_file_location("modbus_pulse", SCRIPT)
mp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mp)


class Device:
    def __init__(self):
        self.coils = [0] * 64
        self.seen = []  # function code of every request
        self.writes = []  # (coil, value) of every write the device took
        self.refuse_writes_after = None  # take this many writes, then answer exception 4
        self.stuck = False  # acknowledge writes without changing the coil
        self.drop_after_writes = None  # close the connection once, after this many writes
        self.wrong_echo = False

    def pdu(self, req):
        fc = req[0]
        self.seen.append(fc)
        if fc == 1:
            start, n = struct.unpack(">HH", req[1:5])
            out = bytearray((n + 7) // 8)
            for i, v in enumerate(self.coils[start : start + n]):
                out[i >> 3] |= v << (i & 7)
            return bytes([1, len(out)]) + bytes(out)
        if fc == 5:
            addr, value = struct.unpack(">HH", req[1:5])
            if self.refuse_writes_after is not None and len(self.writes) >= self.refuse_writes_after:
                return bytes([0x85, 4])
            self.writes.append((addr, 1 if value == 0xFF00 else 0))
            if not self.stuck:
                self.coils[addr] = 1 if value == 0xFF00 else 0
            return struct.pack(">BHH", 5, addr + 1, value) if self.wrong_echo else req
        return bytes([fc | 0x80, 1])


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        dev = self.server.dev
        while True:
            try:
                head = self.request.recv(7)
            except OSError:
                return
            if len(head) < 7:
                return
            tid, _proto, length, unit = struct.unpack(">HHHB", head)
            pdu = dev.pdu(self.request.recv(length - 1))
            if dev.drop_after_writes is not None and len(dev.writes) >= dev.drop_after_writes:
                dev.drop_after_writes = None
                return
            self.request.sendall(struct.pack(">HHHB", tid, 0, len(pdu) + 1, unit) + pdu)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


class Terminal:
    """A person at the terminal: types back the word the prompt shows, or what the test says."""

    def __init__(self, answer=None):
        self.answer = answer
        self.shown = ""
        self.closed = False

    def write(self, text):
        self.shown += text

    def readline(self):
        if self.answer is not None:
            return self.answer
        return re.search(r"Type ([a-z]{4}) to switch it", self.shown).group(1) + "\n"

    def close(self):
        self.closed = True


class Stubbed(unittest.TestCase):
    def setUp(self):
        self.dev = Device()
        self.server = Server(("127.0.0.1", 0), Handler)
        self.server.dev = self.dev
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.addr = f"127.0.0.1:{self.server.server_address[1]}"
        for name, value in (("TIMEOUT_S", 0.3),):
            old = getattr(mp.mb, name)
            setattr(mp.mb, name, value)
            self.addCleanup(setattr, mp.mb, name, old)
        self.slept = []
        self.patch("sleep", self.slept.append)
        self.term = Terminal()
        self.patch("open_tty", lambda: self.term)

    def patch(self, name, value):
        old = getattr(mp, name)
        setattr(mp, name, value)
        self.addCleanup(setattr, mp, name, old)

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = mp.main([self.addr, *args])
        return code, out.getvalue(), err.getvalue()


class Pulses(Stubbed):
    def test_an_off_coil_goes_on_and_comes_back(self):
        code, out, err = self.run_main("coil:3")
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, "# coil 3: was 0, set 1 for 2 s (read back 1), restored 0 (read back 0)\n")
        self.assertEqual(self.dev.writes, [(3, 1), (3, 0)])
        self.assertEqual(self.slept, [2.0])
        self.assertEqual(self.dev.coils[3], 0)
        self.assertTrue(self.term.closed)

    def test_an_on_coil_goes_off_and_comes_back(self):
        self.dev.coils[5] = 1
        code, out, _ = self.run_main("--seconds", "0.5", "coil:5")
        self.assertEqual(code, 0)
        self.assertEqual(self.dev.writes, [(5, 0), (5, 1)])
        self.assertIn("was 1, set 0 for 0.5 s", out)
        self.assertEqual(self.dev.coils[5], 1)

    def test_the_person_is_told_what_will_happen_before_anything_is_written(self):
        self.term.answer = "\n"
        self.run_main("--unit", "9", "coil:3")
        self.assertIn("unit 9: coil 3 is now OFF", self.term.shown)
        self.assertIn("switch it ON for 2 s", self.term.shown)
        self.assertIn("Whatever is wired to that output will act", self.term.shown)
        self.assertEqual(self.dev.writes, [])

    def test_only_a_read_and_the_one_coil_write_are_ever_sent(self):
        self.run_main("coil:3")
        self.assertEqual(set(self.dev.seen), {1, 5})
        self.assertEqual({addr for addr, _ in self.dev.writes}, {3})


class NoWord(Stubbed):
    """Without the word typed back on a terminal, nothing is written."""

    def test_no_terminal_refuses_before_connecting(self):
        def none():
            raise OSError("no tty")

        self.patch("open_tty", none)
        code, out, err = self.run_main("coil:3")
        self.assertEqual((code, out), (3, ""))
        self.assertIn("only runs for a person at a terminal", err)
        self.assertEqual(self.dev.seen, [])

    def test_anything_but_the_word_stops_it(self):
        for answer in ("", "\n", "yes\n", "y\n", "coil:3\n", "3\n", "ABCD\n", "\x00\n", "a" * 300):
            with self.subTest(answer=answer[:8]):
                self.term = Terminal(answer)
                code, out, err = self.run_main("coil:3")
                self.assertEqual((code, out), (1, ""))
                self.assertIn("nothing was switched", err)
                self.assertEqual(self.dev.writes, [])

    def test_the_word_is_not_the_same_twice(self):
        words = set()
        for _ in range(6):
            self.term = Terminal("\n")
            self.run_main("coil:3")
            words.add(re.search(r"Type ([a-z]{4}) to switch it", self.term.shown).group(1))
        self.assertGreater(len(words), 1)

    def test_last_runs_word_does_not_work(self):
        self.term = Terminal("\n")
        self.run_main("coil:3")
        old = re.search(r"Type ([a-z]{4}) to switch it", self.term.shown).group(1)
        for _ in range(4):  # a fresh word each run; a replayed one must not pass
            self.term = Terminal(old + "\n")
            self.run_main("coil:3")
            if old not in self.term.shown.rsplit("Type ", 1)[1]:
                self.assertEqual(self.dev.writes, [])
                return
        self.fail("the same word came up five runs in a row")

    def test_a_pipe_on_stdin_cannot_answer_for_a_person(self):
        # The real script, with no controlling terminal and the word-shaped text on stdin.
        r = subprocess.run(
            [sys.executable, "-I", str(SCRIPT), self.addr, "coil:3"],
            input="abcd\nyes\n",
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
            start_new_session=True,
            env={k: v for k, v in os.environ.items() if k in ("PATH", "SYSTEMROOT")},
        )
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertIn("only runs for a person at a terminal", r.stderr)
        self.assertEqual(self.dev.seen, [])


class GoesWrong(Stubbed):
    """Whatever happens after the coil is switched, the first state is written back, or the person is told."""

    def test_the_device_refuses_the_write(self):
        self.dev.refuse_writes_after = 0
        code, out, err = self.run_main("coil:3")
        self.assertEqual((code, out), (1, ""))
        self.assertIn("refused (exception 4)", err)
        self.assertNotIn("MAY STILL BE", err)
        self.assertEqual(self.dev.coils[3], 0)

    def test_an_interrupt_during_the_wait_still_restores(self):
        def interrupted(_s):
            raise KeyboardInterrupt

        self.patch("sleep", interrupted)
        code, _, err = self.run_main("coil:3")
        self.assertEqual(code, 1)
        self.assertIn("interrupted", err)
        self.assertEqual(self.dev.writes, [(3, 1), (3, 0)])
        self.assertEqual(self.dev.coils[3], 0)

    def test_a_dropped_connection_is_restored_on_a_new_one(self):
        self.dev.drop_after_writes = 1
        code, _, err = self.run_main("coil:3")
        self.assertEqual(code, 1)
        self.assertEqual(self.dev.writes, [(3, 1), (3, 0)])
        self.assertEqual(self.dev.coils[3], 0)
        self.assertNotIn("MAY STILL BE", err)

    def test_a_restore_the_device_refuses_is_shouted(self):
        self.dev.refuse_writes_after = 1
        code, out, err = self.run_main("coil:3")
        self.assertEqual(code, 1)
        self.assertIn("COIL 3 ON 127.0.0.1 MAY STILL BE ON", err)
        self.assertIn("MAY STILL BE ON", self.term.shown)
        self.assertIn("restored 0 (read back None)", out)
        self.assertEqual(self.dev.coils[3], 1)  # the stub really is left on: the warning is true

    def test_a_device_gone_for_good_is_shouted(self):
        def gone(_s):
            self.server.shutdown()
            self.server.server_close()
            self.dev.drop_after_writes = 0

        self.patch("sleep", gone)
        code, _, err = self.run_main("coil:3")
        self.assertEqual(code, 1)
        self.assertIn("MAY STILL BE ON", err)

    def test_a_coil_that_does_not_move_is_reported_not_passed(self):
        self.dev.stuck = True
        code, out, _ = self.run_main("coil:3")
        self.assertEqual(code, 1)
        self.assertIn("(read back 0), restored 0 (read back 0)", out)

    def test_a_reply_that_is_not_an_echo_is_treated_as_switched(self):
        # The device took the write and answered wrongly: the first state is written
        # back anyway, and since no reply can be trusted the person is told to look.
        self.dev.wrong_echo = True
        code, out, err = self.run_main("coil:3")
        self.assertEqual((code, out), (1, ""))
        self.assertIn("not an echo", err)
        self.assertIn("MAY STILL BE ON", err)
        self.assertEqual(self.dev.writes[:2], [(3, 1), (3, 0)])
        self.assertEqual(self.dev.coils[3], 0)

    def test_a_write_whose_reply_never_comes_is_treated_as_switched(self):
        self.dev.drop_after_writes = 1
        self.run_main("coil:3")
        self.assertEqual(self.dev.coils[3], 0)


class CommandLine(Stubbed):
    def test_what_it_will_not_take(self):
        for args in (
            [],
            ["coil:0..3"],
            ["coil:0", "coil:1"],
            ["di:0"],
            ["hr:0"],
            ["ir:0"],
            ["coil:65536"],
            ["coil:-1"],
            ["coil:٣"],
            ["coil"],
            ["--seconds", "0.1", "coil:0"],
            ["--seconds", "11", "coil:0"],
            ["--seconds", "nan", "coil:0"],
            ["--seconds", "inf", "coil:0"],
            ["--seconds", "-2", "coil:0"],
            ["--seconds", "x", "coil:0"],
            ["--seconds"],
            ["--unit", "256", "coil:0"],
            ["--unit", "²", "coil:0"],
            ["--all", "coil:0"],
        ):
            with self.subTest(args=args):
                code, out, err = self.run_main(*args)
                self.assertEqual((code, out), (2, ""))
                self.assertTrue(err.strip())
                self.assertEqual(self.dev.seen, [])
                self.assertEqual(self.term.shown, "")

    def test_no_arguments_prints_the_usage(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(mp.main([]), 2)
        self.assertIn("Usage:", out.getvalue())


if __name__ == "__main__":
    unittest.main()
