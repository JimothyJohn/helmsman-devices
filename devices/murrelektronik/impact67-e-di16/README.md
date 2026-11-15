# Murrelektronik IMPACT67 E DI16 (art. no. 55085)

IP67 EtherNet/IP I/O block: 16 DI (8 on pin 4, 8 on pin 2 of 8 M12 ports). Two Ethernet ports (M12 D-coded), power over 7/8".
EtherNet/IP adapter only: no Modbus.

**Not checked on a unit.** Everything here is from the handbook. What the five articles share is in
[impact67-e-series.md](../impact67-e-series.md).

## Source

*Manual for the Devices of the IMPACT67 E Series, art. no. 55368, edition 1.8 (2019-06)*, 9631751 bytes, SHA-256 `f01edb0ad41cc1aa12de4984c68e1384afc3e6a6df38694401623be58d77c77f`. "p. N" is the handbook's page number. Nick's
copy; Murrelektronik's terms ("Copyright", p. 104) do not allow redistributing it here.

## The connection (pp. 65, 93)

| | instance | bytes |
| --- | --- | --- |
| input (T->O) | 100 | 4 |
| output (O->T) | 112 | 2 |
| configuration | 128 | 0 |

The profile's `enip-io` line: `config=128 o2t=112:2 t2o=100:4`, RPI 10 ms.

**Two I/O length modes** (web server, "Selection of I/O Length Mode", p. 41): "True I/O Length"
(3 in, 1 out for this article, p. 64) or "Always Even I/O Length", which pads an odd
length with a 0x00 byte. The profile uses the even lengths: from software version 1.03 (1.04 for the
DO16) "the I/O length will be always even" (p. 64). A unit in the other mode refuses the
`Forward_Open` (wrong size), and `enip-io` names the reason.

## Input assembly 100

| byte | bits |
| --- | --- |
| 0 | input channel 00 (bit 0) .. 07 (bit 7) |
| 1 | input channel 10 (bit 0) .. 17 (bit 7) |
| 2 | group diagnosis: bit 0 module / sensor supply US below 18 V, bit 2 a sensor supply short-circuit on some M12 port |
| 3 | 0x00, the padding byte of the "Always Even I/O Length" mode |

## Output assembly 112

| byte | bits |
| --- | --- |
| 0 | reserved (the DI16 has no outputs; the connection still carries this byte) |
| 1 | 0x00, the padding byte of the "Always Even I/O Length" mode |

Channel numbers are Murrelektronik's: 00..07 are pin 4 of M12 ports 0..7, 10..17 pin 2 of the
same ports. Bit 0 of a byte is the lowest channel of that byte.

## Inferred

- The O->T data carries the 32-bit run/idle header and T->O none, as a "Generic EtherNet Module" connection does (the handbook's own example, p. 56-57), and as `enip-io`'s explicit mode assumes. The handbook does not say.
- What the outputs do when the controller is lost. The handbook shows the network LED flashing red when "at least one connection has timeout" (p. 83) and nothing about the outputs. Expect them off; the bench decides.
- The 1 s RPI ceiling in `cycle_ms`: the handbook gives no maximum.

## Files

- [`murrelektronik-impact67-e-di16.device`](murrelektronik-impact67-e-di16.device): the profile a controller copies into a project.
- [`enip.map`](enip.map): the same channels as `enip-io` map lines, `ADDR` to fill in.
- [`device.toml`](device.toml): the record a lookup matches.

## To make this entry a checked one

- `ListIdentity`: vendor 640, the product code and name this article answers with, its revision (`identity.enip` in `device.toml`).
- Murrelektronik's EDS for the article (p. 45): the connection's real-time formats and RPI range.
- The exclusive owner at 10 ms, every channel once, and a pulled cable to see what the outputs do.
