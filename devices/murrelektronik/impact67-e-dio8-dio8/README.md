# Murrelektronik IMPACT67 E DIO8 (DIO8) (art. no. 55089)

IP67 EtherNet/IP I/O block: 16 DIO (pin 4 and pin 2 of 8 M12 ports, each an input or an output, 1.6 A). Two Ethernet ports (M12 D-coded), power over 7/8".
EtherNet/IP adapter only: no Modbus.

**Not checked on a unit.** Everything here is from the handbook. What the five articles share is in
[impact67-e-series.md](../impact67-e-series.md).

## Source

*Manual for the Devices of the IMPACT67 E Series, art. no. 55368, edition 1.8 (2019-06)*, 9631751 bytes, SHA-256 `f01edb0ad41cc1aa12de4984c68e1384afc3e6a6df38694401623be58d77c77f`. "p. N" is the handbook's page number. Nick's
copy; Murrelektronik's terms ("Copyright", p. 104) do not allow redistributing it here.

## The connection (pp. 73-75, 101)

| | instance | bytes |
| --- | --- | --- |
| input (T->O) | 117 | 8 |
| output (O->T) | 35 | 2 |
| configuration | 110 | 0 |

The profile's `enip-io` line: `config=110 o2t=35:2 t2o=117:8`, RPI 10 ms.

## Input assembly 117

| byte | bits |
| --- | --- |
| 0 | input channel 00 (port 0, pin 4, bit 0) .. 07 (port 7, pin 4, bit 7) |
| 1 | input channel 10 (port 0, pin 2, bit 0) .. 17 (port 7, pin 2, bit 7) |
| 2 | bit 1 no actuator voltage, bit 2 sensor supply undervoltage, bit 3 actuator supply undervoltage |
| 3 | sensor short-circuit, port 0 (bit 0) .. port 7 (bit 7) |
| 4 | actuator overload, channel 00 .. 07 |
| 5 | actuator overload, channel 10 .. 17 |
| 6 | actuator warning, channel 00 .. 07 |
| 7 | actuator warning, channel 10 .. 17 |

## Output assembly 35

| byte | bits |
| --- | --- |
| 0 | output channel 00 (port 0, pin 4, bit 0) .. 07 (port 7, pin 4, bit 7) |
| 1 | output channel 10 (port 0, pin 2, bit 0) .. 17 (port 7, pin 2, bit 7) |

Channel numbers are Murrelektronik's: 00..07 are pin 4 of M12 ports 0..7, 10..17 pin 2 of the
same ports. Bit 0 of a byte is the lowest channel of that byte.

## Notes

- **Four connections** (p. 69): 1 "Exclusive Owner w/o Diags" (input 5, 2 bytes), 2 "Exclusive Owner w/ Diags" (input 117, 8 bytes), 3 "Listen Only w/o Diags" (input 105, 2 bytes), 4 "Listen Only w/ Diags" (input 118, 8 bytes). Output 35 (2 bytes) for the owners, 135 (2 reserved bytes) for the listeners. A listen-only connection "may only be established if the Connection1 or Connection2 have already been established". The profile uses connection 2: the diagnosis costs six bytes a cycle.
- **Two parameterization modes** (web server, "Properties", p. 43). "Over Web Server": each channel's function is set and saved to flash in the web server (pp. 48-51), and the configuration instance is 110 of 0 bytes. "Over EDS File": the controller sends the functions in configuration instance 109 (3 bytes: pin/port mode, pin 4 functions, pin 2 functions, pp. 62-63, 70). helmsman's `enip-io` sends no configuration data, so the profile needs **Over Web Server**.
- **Pin mode or port mode** changes the bit layout (pp. 71-75): pin mode puts pin 4's eight channels in byte 0 and pin 2's in byte 1; port mode interleaves them by port (byte 0: 00, 10, 01, 11, ...). The profile is written for **pin mode**. Set it in the web server, "Port/Pin Configuration" (p. 49).
- Device Level Ring from software version 1.01 (p. 81).

## Inferred

- The product code 55089 (0xD731) and device type 7 come from the EDS file's name, `02800007D7310101.eds` (p. 45): 0x0280 is vendor 640, 0x0007 the type, 0xD731 the product code, 0101 revision 1.1. That is the usual naming of EZ-EDS files, not a statement in the handbook; `ListIdentity` settles it.
- The O->T data carries the 32-bit run/idle header and T->O none, as a "Generic EtherNet Module" connection does (the handbook's own example, p. 56-57), and as `enip-io`'s explicit mode assumes. The handbook does not say.
- What the outputs do when the controller is lost. The handbook shows the network LED flashing red when "at least one connection has timeout" (p. 83) and nothing about the outputs. Expect them off; the bench decides.
- The 1 s RPI ceiling in `cycle_ms`: the handbook gives no maximum.

## Files

- [`murrelektronik-impact67-e-dio8-dio8.device`](murrelektronik-impact67-e-dio8-dio8.device): the profile a controller copies into a project.
- [`enip.map`](enip.map): the same channels as `enip-io` map lines, `ADDR` to fill in.
- [`device.toml`](device.toml): the record a lookup matches.

## To make this entry a checked one

- `ListIdentity`: vendor 640, the product code and name this article answers with, its revision (`identity.enip` in `device.toml`).
- Murrelektronik's EDS for the article (p. 45): the connection's real-time formats and RPI range.
- The exclusive owner at 10 ms, every channel once, and a pulled cable to see what the outputs do.
