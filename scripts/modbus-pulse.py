#!/usr/bin/env python3
"""Switch one Modbus TCP coil for a moment and put it back, for a person at a terminal.

Proving what an output does means switching it, and whatever is wired to
that output will act. So this script runs only for a person: it asks on
the terminal itself (/dev/tty, never standard input), shows what it is
about to do, and goes ahead only when the word it shows is typed back.
With no terminal (an agent's shell, a pipe, CI) it refuses before it
connects. An agent asks the person to run it and to say what moved.

It switches one coil, to the state it is not in, for --seconds, and then
writes the first state back, also when it is interrupted or the device
stops answering halfway.

Usage: python3 -I scripts/modbus-pulse.py HOST[:PORT] [--unit N] [--seconds S] coil:N
  e.g. scripts/modbus-pulse.py 192.168.3.60 coil:3        (2 seconds)
  --seconds takes 0.2 to 10.

Prints one line for the pull request:
  # coil 3: was 0, set 1 for 2.0 s (read back 1), restored 0 (read back 0)

Exit 0 when the coil went there and came back, 1 when anything else
happened (the message says what, and whether the coil may still be
switched), 2 for a bad command line, 3 with no terminal to ask on.

Standard library only, Python 3.9 or later.
"""

import importlib.util
import math
import pathlib
import re
import secrets
import socket
import struct
import sys
import time

_spec = importlib.util.spec_from_file_location(
    "modbus_read", pathlib.Path(__file__).with_name("modbus-read.py")
)
mb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mb)

sleep = time.sleep
COIL = re.compile(r"coil:(\d{1,5})", re.ASCII)
LETTERS = "abcdefghjkmnpqrstuvwxyz"  # no i, l, o: nothing to misread


class Tty:
    """The controlling terminal, opened by name so a pipe on stdin cannot answer for a person."""

    def __init__(self):
        self.f = open("/dev/tty", "r+b", buffering=0)  # noqa: SIM115 - held for the run, closed in close()

    def write(self, text):
        self.f.write(text.encode("ascii", "replace"))

    def readline(self):
        return self.f.readline(256).decode("ascii", "replace")

    def close(self):
        self.f.close()


def open_tty():
    return Tty()


def arguments(argv):
    """(host, port, unit, seconds, coil). Raises ValueError."""
    host, port = mb.target(argv[0])
    rest, unit, seconds = argv[1:], 1, 2.0
    while rest and rest[0] in ("--unit", "--seconds"):
        if len(rest) < 2:
            raise ValueError(f"{rest[0]} takes a value")
        if rest[0] == "--unit":
            if not (rest[1].isascii() and rest[1].isdigit()) or not 0 <= int(rest[1]) <= 255:
                raise ValueError("--unit takes a number 0..255")
            unit = int(rest[1])
        else:
            try:
                seconds = float(rest[1])
            except ValueError:
                seconds = math.nan
            if not 0.2 <= seconds <= 10:  # also false for nan
                raise ValueError("--seconds takes 0.2 to 10")
        rest = rest[2:]
    if len(rest) != 1:
        raise ValueError("one coil a run: coil:N")
    m = COIL.fullmatch(rest[0])
    if not m or int(m.group(1)) > 65535:
        raise ValueError(
            f"{rest[0]!r}: not a coil (coil:0 to coil:65535); a range, an input or a register is not switched"
        )
    return host, port, unit, seconds, int(m.group(1))


def write_coil(c, coil, on):
    pdu = struct.pack(">BHH", 5, coil, 0xFF00 if on else 0)
    if c.request(pdu) != pdu:
        raise ValueError("the device's reply to the write is not an echo of it")


def restore(host, port, unit, coil, was, c):
    """Write the first state back: on the open connection, then on a new one. Returns the read-back or None."""
    for attempt in (c, None):
        try:
            if attempt is None:
                with socket.create_connection((host, port), timeout=mb.TIMEOUT_S) as s:
                    fresh = mb.Client(s, unit)
                    write_coil(fresh, coil, was)
                    return fresh.read("coil", coil, 1)[0]
            write_coil(attempt, coil, was)
            return attempt.read("coil", coil, 1)[0]
        except (OSError, ValueError, struct.error, mb.Refused):
            continue
    return None


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    try:
        host, port, unit, seconds, coil = arguments(argv)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
    try:
        tty = open_tty()
    except OSError:
        print(
            "modbus-pulse.py switches an output, so it only runs for a person at a terminal.\n"
            "There is no terminal here. Ask the person to run it themselves and to say what moved.",
            file=sys.stderr,
        )
        return 3
    try:
        try:
            with socket.create_connection((host, port), timeout=mb.TIMEOUT_S) as s:
                c = mb.Client(s, unit)
                was = c.read("coil", coil, 1)[0]
                word = "".join(secrets.choice(LETTERS) for _ in range(4))
                tty.write(
                    f"\n{host}, unit {unit}: coil {coil} is now {'ON' if was else 'OFF'}.\n"
                    f"This will switch it {'OFF' if was else 'ON'} for {seconds:g} s and then put it back.\n"
                    "Whatever is wired to that output will act. Make the machine safe first.\n"
                    f"Type {word} to switch it, anything else to stop: "
                )
                if tty.readline().strip() != word:
                    tty.write("Stopped. Nothing was switched.\n")
                    print("stopped: nothing was switched", file=sys.stderr)
                    return 1
                # From the moment the write is sent the coil may be switched, whatever comes
                # back: only the device's own refusal means it is not.
                seen, back, sent = None, None, True
                try:
                    try:
                        write_coil(c, coil, not was)
                    except mb.Refused:
                        sent = False
                        raise
                    seen = c.read("coil", coil, 1)[0]
                    sleep(seconds)
                finally:
                    back = restore(host, port, unit, coil, was, c) if sent else was
                    if back != was:
                        warning = (
                            f"COIL {coil} ON {host} MAY STILL BE {'OFF' if was else 'ON'}: writing "
                            f"{was} back {'failed' if back is None else 'was not taken'}. Check the device now."
                        )
                        tty.write(warning + "\n")
                        print(warning, file=sys.stderr)
                line = f"# coil {coil}: was {was}, set {1 - was} for {seconds:g} s (read back {seen}), "
                print(line + f"restored {was} (read back {back})")
                return 0 if seen == 1 - was and back == was else 1
        except mb.Refused as e:
            print(f"{host}: the device refused (exception {e.code})", file=sys.stderr)
        except (OSError, ValueError, struct.error) as e:
            print(f"{host}: {e}", file=sys.stderr)
        except KeyboardInterrupt:
            print("interrupted", file=sys.stderr)
        return 1
    finally:
        tty.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
