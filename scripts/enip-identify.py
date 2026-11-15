#!/usr/bin/env python3
"""Ask an EtherNet/IP device what a library folder needs, over explicit messages only.

Prints the Identity object (vendor, device type, product code, revision,
serial, product name) and the size of each assembly instance asked for, as
a device.toml fragment. Read-only: one session, Get_Attribute_Single
requests, no Forward_Open, nothing written. A device that refuses an
attribute says so in the output; the rest still prints.

Usage: python3 -I scripts/enip-identify.py HOST [ASSEMBLY ...]
  e.g. scripts/enip-identify.py 192.168.3.70 100 112 128

On macOS from an agent session, run it with Apple's /usr/bin/python3: the
Local Network privacy setting keeps other interpreters off the LAN.
Standard library only, Python 3.9 or later.
"""

import socket
import struct
import sys

PORT = 44818
TIMEOUT_S = 2.0
NAMES = {
    1: "vendor_id",
    2: "device_type",
    3: "product_code",
    4: "revision",
    5: "status",
    6: "serial",
    7: "product_name",
}


def encap(cmd, session, body):
    return struct.pack("<HHII8sI", cmd, len(body), session, 0, b"identify", 0) + body


def recv_exact(s, n):
    buf = b""
    while len(buf) < n:
        part = s.recv(n - len(buf))
        if not part:
            raise ConnectionError("the device closed the session")
        buf += part
    return buf


def reply(s):
    head = recv_exact(s, 24)
    length, status = struct.unpack_from("<H", head, 2)[0], struct.unpack_from("<I", head, 8)[0]
    if length > 65511:
        raise ValueError(f"encapsulation length {length}: not a reply")
    return head, status, recv_exact(s, length)


def get_attribute(s, session, cls, inst, attr):
    """Get_Attribute_Single over SendRRData. Returns (general status, data)."""
    path = (
        bytes([0x20, cls, 0x24, inst, 0x30, attr])
        if inst < 256
        else bytes([0x20, cls, 0x25, 0]) + struct.pack("<H", inst) + bytes([0x30, attr])
    )
    mr = bytes([0x0E, len(path) // 2]) + path
    body = struct.pack("<IHH", 0, 10, 2) + struct.pack("<HH", 0, 0) + struct.pack("<HH", 0xB2, len(mr)) + mr
    s.sendall(encap(0x6F, session, body))
    _, status, b = reply(s)
    if status:
        return f"encapsulation status {status:#x}", b""
    off = 8
    _, n0 = struct.unpack_from("<HH", b, off)
    off += 4 + n0
    _, n1 = struct.unpack_from("<HH", b, off)
    r = b[off + 4 : off + 4 + n1]
    if len(r) < 4:
        return "short reply", b""
    general, extra = r[2], r[3]
    return general, r[4 + 2 * extra :]


def decode(attr, data):
    if attr in (1, 2, 3) and len(data) >= 2:
        return struct.unpack_from("<H", data)[0]
    if attr == 4 and len(data) >= 2:
        return f"{data[0]}.{data[1]}"
    if attr == 5 and len(data) >= 2:
        return f"{struct.unpack_from('<H', data)[0]:#06x}"
    if attr == 6 and len(data) >= 4:
        return f"{struct.unpack_from('<I', data)[0]:#010x}"
    if attr == 7 and data:
        return data[1 : 1 + data[0]].decode("ascii", "replace")
    return data.hex()


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    host = argv[0]
    try:
        assemblies = [int(a, 0) for a in argv[1:]]
    except ValueError:
        print("assembly instances are numbers (100, 0x64)", file=sys.stderr)
        return 2
    with socket.create_connection((host, PORT), timeout=TIMEOUT_S) as s:
        s.sendall(encap(0x65, 0, struct.pack("<HH", 1, 0)))
        head, status, _ = reply(s)
        if status:
            print(f"RegisterSession refused: status {status:#x}", file=sys.stderr)
            return 1
        session = struct.unpack_from("<I", head, 4)[0]
        print(f"# {host}: Identity object (class 1, instance 1)")
        print("[identity.enip]")
        for attr, key in NAMES.items():
            general, data = get_attribute(s, session, 0x01, 1, attr)
            if general == 0:
                v = decode(attr, data)
                print(f"{key} = {v!r}" if isinstance(v, str) else f"{key} = {v}")
            else:
                print(f"# {key}: refused ({general})")
        for inst in assemblies:
            general, data = get_attribute(s, session, 0x04, inst, 3)
            if general == 0:
                print(f"# assembly {inst}: {len(data)} bytes, now {data.hex() or '(empty)'}")
            else:
                print(f"# assembly {inst}: data refused (general status {general})")
        s.sendall(encap(0x66, session, b""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
