#!/usr/bin/env python3
"""ListIdentity broadcast: every EtherNet/IP device that answers, one line each. Read-only.

Usage: python3 -I scripts/enip-list.py [BROADCAST ...]   (default: the bench subnets and 255.255.255.255)

On macOS from an agent session, run it with Apple's /usr/bin/python3 (Local
Network privacy). Standard library only, Python 3.9 or later.
"""

import socket
import struct
import sys
import time

TARGETS = sys.argv[1:] or ["192.168.3.255", "10.0.0.255", "192.168.127.255", "255.255.255.255"]
REQ = struct.pack("<HHII8sI", 0x63, 0, 0, 0, b"lid\0\0\0\0\0", 0)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(("", 0))
for t in TARGETS:
    try:
        s.sendto(REQ, (t, 44818))
    except OSError as e:
        print(f"{t}: {e}")
s.settimeout(0.3)
seen = {}
end = time.monotonic() + 3
while time.monotonic() < end:
    try:
        data, (ip, _) = s.recvfrom(1500)
    except OSError:  # a timeout; socket.timeout on 3.9, TimeoutError later
        continue
    if ip in seen or len(data) < 24 + 2 + 4:
        continue
    off = 24 + 2
    _typ, length = struct.unpack_from("<HH", data, off)
    item = data[off + 4 : off + 4 + length]
    # version(2) sockaddr(16) vendor device product rev_major rev_minor status serial name_len name state
    vendor, dtype, product = struct.unpack_from("<HHH", item, 18)
    major, minor = item[24], item[25]
    status, serial = struct.unpack_from("<HI", item, 26)
    n = item[32]
    name = item[33 : 33 + n].decode("ascii", "replace")
    seen[ip] = True
    print(
        f"{ip:15} vendor {vendor:5} type {dtype:#06x} product {product:5} ({product:#06x}) "
        f"rev {major}.{minor} status {status:#06x} serial {serial:#010x} {name!r}"
    )
print(f"{len(seen)} answered")
