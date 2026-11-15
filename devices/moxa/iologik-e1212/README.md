# Moxa ioLogik E1212

Remote Ethernet I/O: 8 DI and 8 DIO, two switched Ethernet ports, Modbus/TCP server and EtherNet/IP
adapter (manual p. 1-2). The E1212-T is the same unit for -40 to 75 °C.

**Not checked on a unit.** Everything here is read from Moxa's documents. What the
family's one benched member showed is in [the E1213's folder](../iologik-e1213/README.md),
and what the series shares, firmware history included, in
[iologik-e1200-series.md](../iologik-e1200-series.md).

## Sources

| | what | where |
| --- | --- | --- |
| **Manual** | *ioLogik E1200 Series User's Manual*, Version 15.10, May 2021, 10 137 362 bytes, SHA-256 `f8788816b2e0062a68f9b7f1ef9850a2d57f92946ac8b64077c4e77097744454`. "p. X-N" is the manual's own page number. | `pct.wiki.uib.no/images/2/29/Moxa-iologik-e1200-series-manual-v15.10.pdf` (a university mirror; fetched 2026-11-12, the hash is the one the E1213's folder gives). Not in this repository. |
| **Release notes** | *Firmware for ioLogik E1200 Series (ioLogik E1212/E1212-T) Release Notes*, to v4.0 (Build24071616, Aug 29, 2025), 64698 bytes, SHA-256 `d5eed5bd230dc012d4d47305f5ea22d7b81270bdc03baa71d99b212cc7610dba`. "RN" below. | Fetched 2026-11-12 from `moxa.com/Moxa/media/PDIM/S100000327/` (the "firmware v4.0.1kp Software Release History" PDF for the E1212). Not in this repository. |
| **EDS** | `ioLogik_E1212_EtherNetIP_V1.1_170207.eds`, 42491 bytes, CRLF, SHA-256 `4ab4e542774c833fabb5e145f72bc59b2559dbac32f62463e553fdeb248aa0e8`. EZ-EDS 3.11.1 generated; `[File]` Revision 1.1, ModDate 02-07-2017; `[Device]` revision 2.6. "l.N" is a line of it. | Fetched 2026-11-12 from ODVA's marketplace, the E1212's page (`marketplace.odva.org/products/1870-iologik-e1212`, "Download the EDS File", a zip of this one file). **Not in this repository**: the file states no terms. Moxa's own download for the E1212 may be newer (the E1213's is v2.0 of 2026, for firmware 4.0); it has not been read. |

## Channels

8 digital inputs and 8 hybrid DIO channels, each DIO a DI or a DO by a jumper inside the unit
(p. 2-4; DO by default, Appendix E). The tables carry 16 DI (DI-00..DI-15) and 8 DO
(DO-00..DO-07), so a DIO channel has a number on both sides and answers on the one its jumper
selects.

## Modbus/TCP (manual p. A-5)

Port 502 (Appendix D), unit id 1 by default (p. A-2). Addresses are the manual's 0-based "Start
Address" (the `modbus-tcp` driver's address); its "Start Register" column is the same plus the
1-based table prefix.

| name | table | address | count | `modbus-tcp` point |
| --- | --- | --- | --- | --- |
| DI_status | discrete input | 0 | 16 | `di:0`..`di:15` |
| DI_counterValue, "high/low word" | input register | 16 | 32 (2 a channel) | `ir:16:u32` (DI-00) .. `ir:46:u32` |
| DI-all_statusFromDI-00 | input register | 48 | 1 | `ir:48` |
| DI_counterStatus / Reset / OverflowFlagClear | coil 256, 272, 288 |  | 16 | (counter control; not in the profile) |
| DI_counterOverflowFlag | discrete input | 1000 | 16 | (not in the profile) |
| DO_status | coil | 0 | 8 | `coil:0`..`coil:7` |
| DO-all_statusFromDO-00 | holding register | 32 | 1 | `hr:32` |
| DO_pulseStatus / pulseCount / OnWidth / OffWidth | coil 16, hr 36, 52, 68 |  | 8 | (pulse mode; not in the profile) |
| DO_p2pStatus / p2pSafeModeFlag / FlagClear | di 4096, 4112, coil 4128 |  | 8 | (peer-to-peer and safe mode; not in the profile) |

"High/low word" is high word first, the driver's default for `u32` (no `sw`). The system registers
(model name, firmware version and build date, MAC, uptime) are the same on every E1200 and are in the
series page.

## EtherNet/IP (manual pp. B-1, B-2)

From firmware 2.5 (p. 5-1; off by default from 4.0). The connection is from the EDS, the meaning of the
bytes from the manual; the two agree on the sizes (the manual's input table ends at byte 66, the EDS's
`Assem101` is 67 bytes, l.463-469).

| | value | EDS |
| --- | --- | --- |
| identity | vendor 991 "Moxa", device type 12 "Communications Adapter", product code **514**, revision 2.6, product name "E1212" | `[Device]`, l.18-27 |
| input assembly | 101, 67 bytes (`Param2` "Input Size" 67) | l.463-469, l.425-437 |
| output assembly | 102, 1 byte (`Param1` "Output Size" 1) | l.470-476, l.412-424 |
| RPI | 100 000 to 3 000 000 µs, default 100 000 (`Param3` "RPI Range") | l.438-450 |
| Connection1 "Exclusive Owner" | trigger and transport `0x04010002`, connection word `0x44640405` (O->T with the 32-bit run/idle header, T->O without), path `20 04 24 64 2C 66 2C 65`: configuration 100, O->T 102, T->O 101 | l.485-529 |
| Connection2 "Input Only" | `0x02010002`, the same connection word, O->T size 0, path `20 04 2C 6F 20 04 2C 65` | l.530-574 |

The exclusive owner is word for word the E1213's, which runs on the bench, so the profile's `enip-io`
line restates it (`config=100 o2t=102:1 t2o=101:67`) and no vendor file is needed on the box. The Input
Only connection is **not** the E1213's: this EDS's path names no configuration instance and repeats the
class segment, and its connection word claims the exclusive owner's real-time format. The E1213's EDS
v2.0 has `20 04 24 64 2C 6F 2C 65` and `0x44640305` there. Which of the two an E1212 accepts is unchecked,
so the profile does not offer input only.

Input assembly 101 (0x65), 67 bytes by the manual's table:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0-1 | diStatus, "DI mode status (0: OFF, 1: ON)" | BOOL | DI-00..DI-15 |
| 2-65 | diCounterValue, "Counter mode value" | UDINT | DI-00..DI-15 |
| 66 | doStatus, "status (0: OFF, 1: ON)" | BOOL | DO-00..DO-07 |

Output assembly 102 (0x66), 1 byte:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0 | doStatus | BOOL | DO-00..DO-07 |

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

The EDS at hand is revision 2.6 (2017); a unit at 3.x or 4.0 reports another revision, so an electronic
key of `key=exact` against it would be refused, as on the E1213. The profile sets no key.

## Inferred

- Counter *n* is the two input registers at `16 + 2n` and, over EtherNet/IP, the UDINT at byte `2 + 4n`, little-endian. The manual gives only the ranges.
- Bit *n* of the input word is channel *n*. The manual gives byte and channel ranges, not bit positions; the E1213 on the bench has it this way.
- DI-08..DI-15 are the eight DIO channels read as inputs, and DO-00..DO-07 the same eight as outputs. The manual does not say which numbers the DIO take; on the E1213 the console says "DO4-7 Channel Equal DIO0-3 Channel", the DIO being its last DI and last DO.
- What the outputs do when the owner goes idle or the connection times out. From firmware 3.2 Safe Mode covers EtherNet/IP (RN); it needs the communication watchdog, which is off by default (p. 3-4).
- Before firmware 3.2 the unit names a UDP port of its own for O->T data in its `Forward_Open` reply, as the E1213 at 3.1 does (5222). The release notes list the same fix for this model; the port was seen on the E1213 only. Helmsman's scanner sends where the reply says.

## Files

- [`moxa-iologik-e1212.device`](moxa-iologik-e1212.device): the profile a controller copies into a project; the channels above by name.
- [`modbus.map`](modbus.map): the same channels as map lines for `modbus-tcp`, `ADDR` to fill in.
- [`enip.map`](enip.map): the same channels for `enip-io`.
- [`device.toml`](device.toml): the record a lookup matches.

## To make this entry a checked one

- Read Moxa's current EDS for the E1212 (the one here is from ODVA's marketplace and dated 2017) and compare its Input Only connection and revision.
- Put a unit on the bench, note its firmware (the web console's overview, or input registers 5029 and 5031) and drive every channel once: `checked_on`, `firmware` and `checked_by` in `device.toml`.
- On that unit: `ListIdentity` (does it answer product code 514, and which product name), then the exclusive owner at 100 ms.
