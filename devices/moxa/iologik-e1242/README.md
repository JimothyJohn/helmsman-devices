# Moxa ioLogik E1242

Remote Ethernet I/O: 4 AI, 4 DI and 4 DIO, two switched Ethernet ports, Modbus/TCP server and
EtherNet/IP adapter (manual p. 1-2). The E1242-T is the same unit for -40 to 75 °C.

**Not checked on a unit.** Everything here is read from Moxa's documents. What the
family's one benched member showed is in [the E1213's folder](../iologik-e1213/README.md),
and what the series shares, firmware history included, in
[iologik-e1200-series.md](../iologik-e1200-series.md).

## Sources

| | what | where |
| --- | --- | --- |
| **Manual** | *ioLogik E1200 Series User's Manual*, Version 15.10, May 2021, 10 137 362 bytes, SHA-256 `f8788816b2e0062a68f9b7f1ef9850a2d57f92946ac8b64077c4e77097744454`. "p. X-N" is the manual's own page number. | `pct.wiki.uib.no/images/2/29/Moxa-iologik-e1200-series-manual-v15.10.pdf` (a university mirror; fetched 2026-11-12, the hash is the one the E1213's folder gives). Not in this repository. |
| **Release notes** | *Firmware for ioLogik E1200 Series (ioLogik E1242/E1242-T) Release Notes*, to v4.0 (Build24071616, Aug 29, 2025), 64970 bytes, SHA-256 `f024674669f92317a8346cec0a8adbf3b1dd72b9e74205b62885e5f422da9253`. "RN" below. | Fetched 2026-11-12 from `moxa.com/Moxa/media/PDIM/S100000327/` (the "firmware v4.0.1kp Software Release History" PDF for the E1242). Not in this repository. |

## Channels

4 analog inputs, AI-00..AI-03 (voltage or current by jumper, p. 2-4), 4 digital inputs and 4
hybrid DIO channels, each a DI or a DO by jumper (DO by default, Appendix E). The tables carry
8 DI (DI-00..DI-07) and 4 DO (DO-00..DO-03), so a DIO channel has a number on both sides.

## Modbus/TCP (manual p. A-14, A-15)

Port 502 (Appendix D), unit id 1 by default (p. A-2). Addresses are the manual's 0-based "Start
Address" (the `modbus-tcp` driver's address); its "Start Register" column is the same plus the
1-based table prefix.

| name | table | address | count | `modbus-tcp` point |
| --- | --- | --- | --- | --- |
| DI_status | discrete input | 0 | 8 | `di:0`..`di:7` |
| DI_counterValue, "high/low word" | input register | 16 | 16 (2 a channel) | `ir:16:u32` (DI-00) .. `ir:30:u32` |
| DI-all_statusFromDI-00 | input register | 48 | 1 | `ir:48` |
| DI_counterStatus / Reset / OverflowFlagClear | coil 256, 272, 288 |  | 8 | (counter control; not in the profile) |
| DI_counterOverflowFlag | discrete input | 1000 | 8 | (not in the profile) |
| DO_status | coil | 0 | 4 | `coil:0`..`coil:3` |
| DO-all_statusFromDO-00 | holding register | 32 | 1 | `hr:32` |
| DO_pulseStatus / pulseCount / OnWidth / OffWidth | coil 16, hr 36, 52, 68 |  | 4 | (pulse mode; not in the profile) |
| DO_p2pStatus / p2pSafeModeFlag / FlagClear | di 4096, 4112, coil 4128 |  | 4 | (peer-to-peer and safe mode; not in the profile) |
| AI_rawValue | input register | 512 | 4 | `ir:512`..`ir:515` |
| AI_scaledValue, "high/low word" | input register | 520 | 8 (2 a channel) | (not in the profile: see below) |
| AI_status | input register | 576 | 4 | `ir:576`..`ir:579` |
| AI_mode | holding register | 544 | 4 | (0: 0-10 V, 1: 4-20 mA, 2: 0-20 mA, 4: 4-20 mA burnout; not in the profile) |

"High/low word" is high word first, the driver's default for `u32` (no `sw`). The system registers
(model name, firmware version and build date, MAC, uptime) are the same on every E1200 and are in the
series page.

## EtherNet/IP (manual pp. B-1, B-2)

The unit is an EtherNet/IP adapter from firmware 2.5 (p. 5-1; off by default from 4.0). The manual gives the
assembly instances and what the bytes mean; it does not give the product code, the configuration
instance, the RPI range or the connection's real-time format. Those are in the model's EDS, which has not
been read, so `device.toml` has no `identity.enip` and the profile reaches this model over Modbus/TCP only.
On the two siblings whose EDS has been read (E1212, E1213) the connection is the same: configuration
instance 100, exclusive owner on 102 and 101, input only on heartbeat 111, RPI 100 ms to 3 s.

Input assembly 101 (0x65), 42 bytes by the manual's table:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0 | diStatus, "DI mode status (0: OFF, 1: ON)" | BOOL | DI-00..DI-07 |
| 1-32 | diCounterValue, "Counter mode value" | UDINT | DI-00..DI-07 |
| 33 | doStatus, "status (0: OFF, 1: ON)" | BOOL | DO-00..DO-03 |
| 34-41 | aiValueRaw, "AI raw value" | UINT | AI-00..AI-03 |

Output assembly 102 (0x66), 1 byte:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0 | doStatus | BOOL | DO-00..DO-03 |

## What depends on the firmware

The ten E1200 models share one firmware line (the same builds on the same dates in every model's
release notes). What moves with it, from this model's notes:

| firmware | what changed for a controller |
| --- | --- |
| before 2.5 | no EtherNet/IP (manual p. 5-1) |
| 3.0 | "Update only the next or the previous released firmware version": updates go one release at a time |
| 3.1 | EtherNet/IP needs no licence registration any more; `Set_Attribute_Single` works |
| 3.2 | "Ethernet/IP implicit messages are sent to port 2222 by default": before it the unit names another UDP port for O->T data in its `Forward_Open` reply (5222 on the E1213 at 3.1) and ignores data sent to 2222; Safe Mode covers EtherNet/IP |
| 3.3 | "Ethernet/IP cannot establish second input-only session" fixed; a default password ("moxa") and a login policy |
| 4.0 | SNMP, EtherNet/IP and RESTful are **off by default**: a unit updated or shipped at 4.0 does not answer `ListIdentity` until EtherNet/IP is switched on in its web console; Modbus/TCP stays on |

v3.2 also lists "Discrepancy in the Modbus address at viewed on the web console" as fixed, and an
earlier release "Web User-Define Modbus address is incorrect": on old firmware the console's address
page is not to be trusted over the manual's table.

## Inferred

- Counter *n* is the two input registers at `16 + 2n` and, over EtherNet/IP, the UDINT at byte `1 + 4n`, little-endian. The manual gives only the ranges.
- Bit *n* of the input word is channel *n*. The manual gives byte and channel ranges, not bit positions; the E1213 on the bench has it this way.
- Channel *n*'s raw value is input register `512 + n` and, over EtherNet/IP, the UINT at byte `34 + 2n`.
- DI-04..DI-07 are the four DIO channels read as inputs, and DO-00..DO-03 the same four as outputs, by the E1213's pattern (its DIO are its last DI and last DO). The manual does not say.
- What the outputs do when the controller is lost: Safe Mode needs the communication watchdog, off by default (pp. 3-4, 3-21).

## Left out of the profile, and why

- **AI_scaledValue** (input registers from 520, two words a channel). The manual says "high/low word" and nothing about the number's format; the same value is a REAL on EtherNet/IP's AI Channel Object (p. B-3), so it is probably an IEEE float, high word first (`f32`). Nobody has read one from a unit, and a wrong format reads as a plausible wrong number, so the profile carries the raw value only.

## Files

- [`moxa-iologik-e1242.device`](moxa-iologik-e1242.device): the profile a controller copies into a project; the channels above by name.
- [`modbus.map`](modbus.map): the same channels as map lines for `modbus-tcp`, `ADDR` to fill in.
- [`device.toml`](device.toml): the record a lookup matches.

## To make this entry a checked one

- Read this model's EDS (Moxa's product page, Resources, "EDS file"; the site refuses scripted downloads): its product code gives `identity.enip`, its `[Connection Manager]` the connection, and the profile gains its `enip-io` line.
- Put a unit on the bench, note its firmware (the web console's overview, or input registers 5029 and 5031) and drive every channel once: `checked_on`, `firmware` and `checked_by` in `device.toml`.
