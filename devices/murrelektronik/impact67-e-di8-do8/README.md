# Murrelektronik IMPACT67 E DI8 DO8 (art. no. 55086)

IP67 EtherNet/IP I/O block: 8 DI, 8 DO (2 A each). Two Ethernet ports (M12 D-coded), power over 7/8".
EtherNet/IP adapter only: no Modbus. **The bench block is this article** (its EDS, from Nick, 2026-11-12).

**Not checked on a unit.** Everything here is from the handbook and the EDS. What the five articles
share is in [impact67-e-series.md](../impact67-e-series.md).

## Sources

| | what | where |
| --- | --- | --- |
| **Handbook** | *Manual for the Devices of the IMPACT67 E Series, art. no. 55368, edition 1.8 (2019-06)*, 9631751 bytes, SHA-256 `f01edb0ad41cc1aa12de4984c68e1384afc3e6a6df38694401623be58d77c77f`. "p. N" is the handbook's page number. | Nick's copy. Murrelektronik's terms ("Copyright", p. 104) do not allow redistributing it here. |
| **EDS** | `55086_Impact67_EIP_DI8DO8.eds`, 11427 bytes, SHA-256 `fd900040a8f59ea7c67b8908dae152639cd45516855a8299cdd5bf3654ed745e`. EZ-EDS 3.11 generated; `[File]` Revision 1.1, CreateDate 09-24-2009, ModDate 04-29-2015. "l.N" is a line of it. | Nick's download, `55086_IMPACT67_KF5_x_11.zip` (6e6748dc…cb69, one file), from Murrelektronik's configuration-file downloads. **Not in this repository**: the file states no terms. |

## Identity (EDS `[Device]`, l.13-23)

| attribute | value |
| --- | --- |
| vendor | 640 "Murrelektronik GmbH" |
| device type | 7 "General Purpose Discrete I/O" |
| product code | **55086**, the article number |
| revision | 1.1 |
| product name | "IMPACT67 DI8 DO8", catalog "55086" |

## The connection (EDS `[Connection Manager]` l.151-196; handbook pp. 66, 95)

One connection, "I/O Connection": trigger and transport `0x04010002` (class 1, cyclic, exclusive owner),
connection word `0x4464040F`, path `20 04 24 80 2C 70 2C 64`: configuration 128, O->T 112, T->O 100.

| | instance | bytes in the EDS (min, max, default) | the profile |
| --- | --- | --- | --- |
| input (T->O) | 100 | `Param1` "Input Size" 3, 4, **3** (l.76-88) | 4 |
| output (O->T) | 112 | `Param2` "Output Size" 1, 2, **1** (l.89-101) | 2 |
| configuration | 128 | `Param3` 0, 0, 0, "Always Zero" (l.102-114) | 0 |
| RPI | | `Param4` 5 000 to 3 200 000 µs, default 10 000 (l.115-127) | 10 ms, `cycle_ms=10..3200` |

The connection word, by the generator's own bit legend beside it: bits 0-3 (O->T and T->O, fixed **and
variable** size), O->T real-time format 4 (the 32-bit run/idle header), T->O format 0 (modeless),
point-to-point both ways, T->O multicast allowed, scheduled priority.

The profile's `enip-io` line: `config=128 o2t=112:2 t2o=100:4`, RPI 10 ms.

**Two I/O length modes** (web server, "Selection of I/O Length Mode", p. 41): "True I/O Length"
(3 in, 1 out, p. 64) or "Always Even I/O Length", which pads an odd length with a 0x00 byte. The EDS
accepts both (3..4 and 1..2) and defaults to the true lengths; the handbook says that from software
version 1.03 "the I/O length will be always even" (p. 64). The profile uses the even lengths. Which
mode the bench unit is in is one read away: `scripts/enip-identify.py IP 100 112` prints each
assembly's size. If it says 3 and 1, the profile's line becomes `o2t=112:1 t2o=100:3` and byte 3 and
the output padding byte go.

## Input assembly 100

| byte | bits |
| --- | --- |
| 0 | input channel 00 (bit 0) .. 07 (bit 7) |
| 1 | group diagnosis: bit 0 module / sensor supply US below 18 V, bit 1 actuator supply UA below 18 V, bit 2 a sensor supply short-circuit on some M12 port, bit 3 an output overloaded or short-circuited (group) |
| 2 | actuator overload, channel 00 (bit 0) .. 07 (bit 7) |
| 3 | 0x00, the padding byte of the "Always Even I/O Length" mode |

## Output assembly 112

| byte | bits |
| --- | --- |
| 0 | output channel 00 (bit 0) .. 07 (bit 7) |
| 1 | 0x00, the padding byte of the "Always Even I/O Length" mode |

Channel numbers are Murrelektronik's: 00..07 are pin 4 of M12 ports 0..7. Bit 0 of a byte is the
lowest channel of that byte. The EDS describes the assemblies' data as one opaque block
(`Assem100`/`Assem112`, l.129-141) and says nothing about the bits; the bits are the handbook's.

## Inferred

- What the outputs do when the controller is lost. The handbook shows the network LED flashing red when "at least one connection has timeout" (p. 83) and nothing about the outputs; the EDS has no parameter for it. Expect them off; the bench decides.

## Files

- [`murrelektronik-impact67-e-di8-do8.device`](murrelektronik-impact67-e-di8-do8.device): the profile a controller copies into a project.
- [`enip.map`](enip.map): the same channels as `enip-io` map lines, `ADDR` to fill in.
- [`device.toml`](device.toml): the record a lookup matches.

## To make this entry a checked one

- `ListIdentity` and `scripts/enip-identify.py IP 100 112 128`: does the unit answer 640 / 55086 / 1.1 and "IMPACT67 DI8 DO8", and which length mode is it in.
- The exclusive owner at 10 ms, every channel once, and a pulled cable to see what the outputs do.
- An output into a short: it stays off until written 0 then 1 (pp. 33, 91).
