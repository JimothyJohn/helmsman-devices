> **Not yet held against a robot.** Modbus TCP has been read and written on UR's simulators
> (URSim e-Series 5.26.0 and PolyScope X 10.13.0, 2026-11-20); EtherNet/IP has answered nowhere.
> The open questions are in `device.toml`.

# Universal Robots e-Series (and PolyScope X)

A collaborative robot arm whose control box is a Modbus TCP server on port 502, always on,
and an EtherNet/IP adapter (input assembly 100, 480 bytes; output 112, 224 bytes, from the
EDS) once it is switched on in PolyScope. The profile covers Modbus TCP.

## The map has holes

Only these addresses exist. A request that touches any other is refused whole with exception 2
(Illegal Data Address), so a read of 256..260 fails because of 259, and a 16-bit read of the
input bits fails because of bits 10..15.

| | addresses |
| --- | --- |
| registers (FC 3, 4) | 0..11, 16..22, 24..33, 128..258, 260..266, 270..275, 280..285, 290..295, 300..305, 310..315, 320..325, 400..405, 410..415, 420..428, 450..451, 768..770 |
| bits (FC 1, 2) | 0..9, 16..25, 64..143, 260..265, 300..427, 500..627 |

Every address `x` also answers at 10000 + x up to 40000 + x (UR's page, for Siemens clients).

## Values

- **Signed values** come as 16-bit two's complement: `65535` is -1. UR's page converts with
  `val - 65535`, which is one off; use `val - 65536` for `val >= 32768`.
- **A joint's angle is two registers.** 270..275 hold the angle inside one turn (0..6283 mrad)
  and 320..325 the turns, signed. On the simulators the base at -1.6007 rad read 4682 and -1:
  -1 x 6283 + 4682 = -1601 mrad. Read alone, 270 says +4.682 rad.
- **TCP pose** (400..405): x, y, z in tenths of a mm, rx, ry, rz in mrad.

## Simulators

`universalrobots/ursim_e-series:5.26.0` and `universalrobots/ursim_polyscopex:10.13.0` in
Docker answered the same, register for register. Register writes (FC 6, FC 16) read back as
written, which is not what the forum reports about older simulators. Neither simulator gave
EtherNet/IP: the first could not start PolyScope to switch it on (on Apple silicon), and the
second does not ship the `ur-ethernetip` URCap. The arm was never powered on or moved, so speeds
and currents were never seen nonzero with the arm moving.
