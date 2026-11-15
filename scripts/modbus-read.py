#!/usr/bin/env python3
"""Read a Modbus TCP device: who it says it is, and the bits and registers asked for. Read-only.

Sends read requests only: function codes 1 (coils), 2 (discrete inputs),
3 (holding registers), 4 (input registers) and 43/14 (Read Device
Identification). No write function code is ever sent, so nothing on the
device changes. A device that refuses a request says so in the output; the
rest still prints.

Usage: python3 -I scripts/modbus-read.py HOST[:PORT] [--unit N] [RANGE ...]
  RANGE is the library's point syntax, 0-based PDU addresses:
    di:0..di:11      discrete inputs 0 to 11        coil:0..7   coils 0 to 7
    ir:16..ir:39     input registers 16 to 39       hr:300      one holding register
    ir:16:u32..ir:38:u32   32-bit values: the last one's second word is read too
  e.g. scripts/modbus-read.py 192.168.3.60 di:0..di:11 ir:16:u32..ir:38:u32

Prints an [identity.modbus] fragment for device.toml, then one line a range:
  # di 0..11: 100000000000              one digit an address, in address order
  # ir 16..19: 0000 0001 0000 0000      one hex word a register, as sent

Exit 0 when every range was read, 1 when the device refused one or the
connection failed, 2 for a bad command line.

On macOS from an agent session, run it with Apple's /usr/bin/python3: the
Local Network privacy setting keeps other interpreters off the LAN.
Standard library only, Python 3.9 or later.
"""

import re
import socket
import struct
import sys

PORT = 502
TIMEOUT_S = 2.0
READ = {"coil": 1, "di": 2, "hr": 3, "ir": 4}
MAX_BITS = 2000  # a request's limit (Modbus Application Protocol V1.1b3, 6.1 and 6.2)
MAX_REGS = 125  # 6.3 and 6.4
MAX_TOTAL = 65536
WIDE = {"u32", "i32", "f32", "u32sw", "i32sw", "f32sw"}
NARROW = {"u16", "i16"}
OBJECTS = {0: "vendor_name", 1: "product_code", 2: "revision"}
RANGE = re.compile(
    r"(di|coil|ir|hr):(\d{1,5})(?::([a-z0-9]{1,5}))?"
    r"(?:\.\.(?:(di|coil|ir|hr):)?(\d{1,5})(?::([a-z0-9]{1,5}))?)?",
    re.ASCII,  # \d would otherwise take any script's digits
)


class Refused(Exception):
    """The device answered with a Modbus exception."""

    def __init__(self, code):
        super().__init__(f"exception {code}")
        self.code = code


def parse_range(text):
    """(table, first address, count) for one RANGE argument. Raises ValueError."""
    m = RANGE.fullmatch("".join(text.split()))
    if not m:
        raise ValueError(f"{text!r}: not a range (di:0..di:11, coil:0..7, ir:16..ir:39, hr:300)")
    table, first, fmt, table2, last, fmt2 = m.groups()
    for f in (fmt, fmt2):
        if f is not None and (f not in WIDE | NARROW or table in ("di", "coil")):
            raise ValueError(f"{text!r}: {f!r} is not a register format here")
    if table2 not in (None, table):
        raise ValueError(f"{text!r}: a range stays in one table")
    first = int(first)
    last = first if last is None else int(last)
    if (fmt2 if fmt2 is not None else fmt) in WIDE:
        last += 1  # the second word of the last 32-bit value
    if last < first:
        raise ValueError(f"{text!r}: the range ends before it starts")
    if last > 65535:
        raise ValueError(f"{text!r}: addresses stop at 65535")
    return table, first, last - first + 1


def recv_exact(s, n):
    buf = b""
    while len(buf) < n:
        part = s.recv(n - len(buf))
        if not part:
            raise ConnectionError("the device closed the connection")
        buf += part
    return buf


class Client:
    def __init__(self, sock, unit):
        self.s = sock
        self.unit = unit
        self.tid = 0

    def request(self, pdu):
        """One request, one reply PDU. Raises Refused, or ValueError for a reply that is not one."""
        self.tid = self.tid % 65535 + 1
        self.s.sendall(struct.pack(">HHHB", self.tid, 0, len(pdu) + 1, self.unit) + pdu)
        tid, proto, length, unit = struct.unpack(">HHHB", recv_exact(self.s, 7))
        if proto != 0 or not 3 <= length <= 254:
            raise ValueError(f"not a Modbus reply (protocol {proto}, length {length})")
        reply = recv_exact(self.s, length - 1)
        if tid != self.tid or unit != self.unit:
            raise ValueError(f"a reply to another request (transaction {tid}, unit {unit})")
        if reply[0] == pdu[0] | 0x80:
            raise Refused(reply[1])
        if reply[0] != pdu[0]:
            raise ValueError(f"function {reply[0]} in reply to function {pdu[0]}")
        return reply

    def read(self, table, first, count):
        """count values from first: 0/1 for a bit table, 0..65535 for a register table."""
        fc, bits = READ[table], table in ("di", "coil")
        out = []
        while len(out) < count:
            n = min(count - len(out), MAX_BITS if bits else MAX_REGS)
            reply = self.request(struct.pack(">BHH", fc, first + len(out), n))
            want = (n + 7) // 8 if bits else 2 * n
            if len(reply) != 2 + want or reply[1] != want:
                raise ValueError(f"{len(reply) - 2} data bytes where {want} were due")
            data = reply[2:]
            if bits:
                out += [data[i >> 3] >> (i & 7) & 1 for i in range(n)]
            else:
                out += struct.unpack(f">{n}H", data)
        return out

    def identification(self):
        """{key: text} from Read Device Identification, basic objects. Raises Refused."""
        found, obj = {}, 0
        for _ in range(8):  # "more follows" is the device's word; eight rounds bound it
            reply = self.request(bytes([0x2B, 0x0E, 0x01, obj]))
            if len(reply) < 7 or reply[1] != 0x0E:
                raise ValueError("a short device identification reply")
            more, next_obj, n, off = reply[4], reply[5], reply[6], 7
            for _ in range(n):
                if off + 2 > len(reply) or off + 2 + reply[off + 1] > len(reply):
                    raise ValueError("a device identification object runs past the reply")
                oid, size = reply[off], reply[off + 1]
                if oid in OBJECTS:
                    found.setdefault(OBJECTS[oid], text(reply[off + 2 : off + 2 + size]))
                off += 2 + size
            if more != 0xFF or next_obj <= obj:
                break
            obj = next_obj
        return found


def text(raw):
    """A device's string, made safe to print on one line: printable ASCII, 120 characters."""
    return "".join(c for c in raw.decode("ascii", "replace") if " " <= c <= "~")[:120]


def target(arg):
    host, sep, port = arg.rpartition(":")
    if not sep or not (port.isascii() and port.isdigit()):
        return arg, PORT
    if not host or not 0 < int(port) < 65536:
        raise ValueError(f"{arg!r}: not HOST or HOST:PORT")
    return host, int(port)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    try:
        host, port = target(argv[0])
        rest, unit = argv[1:], 1
        if rest[:1] == ["--unit"]:
            if len(rest) < 2 or not (rest[1].isascii() and rest[1].isdigit()) or not 0 <= int(rest[1]) <= 255:
                raise ValueError("--unit takes a number 0..255")
            unit, rest = int(rest[1]), rest[2:]
        ranges = [parse_range(a) for a in rest]
        if sum(r[2] for r in ranges) > MAX_TOTAL:
            raise ValueError(f"more than {MAX_TOTAL} addresses in one run")
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
    failed = False
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT_S) as s:
            c = Client(s, unit)
            print(f"# {host}: Read Device Identification (function 43/14), unit {unit}")
            try:
                found = c.identification()
                if found:
                    print("[identity.modbus]")
                for key, value in found.items():
                    print(f"{key} = {value!r}")
            except Refused as e:
                print(f"# device identification: refused (exception {e.code})")
            for table, first, count in ranges:
                span = f"{table} {first}" + (f"..{first + count - 1}" if count > 1 else "")
                try:
                    values = c.read(table, first, count)
                except Refused as e:
                    print(f"# {span}: refused (exception {e.code})")
                    failed = True
                    continue
                if table in ("di", "coil"):
                    print(f"# {span}: {''.join(map(str, values))}")
                else:
                    print(f"# {span}: {' '.join(f'{v:04x}' for v in values)}")
    except (OSError, ValueError, struct.error) as e:
        print(f"{host}: {e}", file=sys.stderr)
        return 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
