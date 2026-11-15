# Moxa ioLogik E1214

Remote Ethernet I/O: 6 DI and 6 relays, two switched Ethernet ports, Modbus/TCP server and EtherNet/IP
adapter (manual p. 1-2). The E1214-T is the same unit for -40 to 75 °C.

**Not checked on a unit.** Everything here is read from Moxa's documents. What the
family's one benched member showed is in [the E1213's folder](../iologik-e1213/README.md),
and what the series shares, firmware history included, in
[iologik-e1200-series.md](../iologik-e1200-series.md).

## Sources

| | what | where |
| --- | --- | --- |
| **Manual** | *ioLogik E1200 Series User's Manual*, Version 15.10, May 2021, 10 137 362 bytes, SHA-256 `f8788816b2e0062a68f9b7f1ef9850a2d57f92946ac8b64077c4e77097744454`. "p. X-N" is the manual's own page number. | `pct.wiki.uib.no/images/2/29/Moxa-iologik-e1200-series-manual-v15.10.pdf` (a university mirror; fetched 2026-11-12, the hash is the one the E1213's folder gives). Not in this repository. |
| **Release notes** | *Firmware for ioLogik E1200 Series (ioLogik E1214/E1214-T) Release Notes*, to v4.0 (Build24071616, Aug 29, 2025), 64858 bytes, SHA-256 `f50af21903ef61310eac623d887ce080110e361d3076ec5de7c2c92b77f27c72`. "RN" below. | Fetched 2026-11-12 from `moxa.com/Moxa/media/PDIM/S100000327/` (the "firmware v4.0.1kp Software Release History" PDF for the E1214). Not in this repository. |

## Channels

6 digital inputs, DI-00..DI-05 (DI or counter), and 6 relays, RLY-00..RLY-05 (relay or pulse
output; in pulse mode the widths are in units of 1.5 s, p. A-9). The unit counts each relay's
switching (total and current count).

## Modbus/TCP (manual p. A-9)

Port 502 (Appendix D), unit id 1 by default (p. A-2). Addresses are the manual's 0-based "Start
Address" (the `modbus-tcp` driver's address); its "Start Register" column is the same plus the
1-based table prefix.

| name | table | address | count | `modbus-tcp` point |
| --- | --- | --- | --- | --- |
| DI_status | discrete input | 0 | 6 | `di:0`..`di:5` |
| DI_counterValue, "high/low word" | input register | 16 | 12 (2 a channel) | `ir:16:u32` (DI-00) .. `ir:26:u32` |
| DI-all_statusFromDI-00 | input register | 48 | 1 | `ir:48` |
| DI_counterStatus / Reset / OverflowFlagClear | coil 256, 272, 288 |  | 6 | (counter control; not in the profile) |
| DI_counterOverflowFlag | discrete input | 1000 | 6 | (not in the profile) |
| RLY_status | coil | 0 | 6 | `coil:0`..`coil:5` |
| RLY-all_statusFromRLY-00 | holding register | 32 | 1 | `hr:32` |
| RLY_TotalCount, "high/low word" | input register | 64 | 12 (2 a relay) | `ir:64:u32` (RLY-00) .. `ir:74:u32` |
| RLY_currentCount, "high/low word" | input register | 96 | 12 (2 a relay) | (not in the profile) |
| RLY_pulseStatus / pulseCount / OnWidth / OffWidth | coil 16, hr 36, 52, 68 |  | 6 | (pulse mode; not in the profile) |
| RLY_p2pStatus / p2pSafeModeFlag / FlagClear | di 4096, 4112, coil 4128 |  | 6 | (peer-to-peer and safe mode; not in the profile) |

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

Input assembly 101 (0x65), 26 bytes by the manual's table:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0 | diStatus, "DI mode status (0: OFF, 1: ON)" | BOOL | DI-00..DI-05 |
| 1-24 | diCounterValue, "Counter mode value" | UDINT | DI-00..DI-05 |
| 25 | relayStatus, "status (0: OFF, 1: ON)" | BOOL | RLY-00..RLY-05 |

Output assembly 102 (0x66), 1 byte:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0 | relayStatus | BOOL | RLY-00..RLY-05 |

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

## Inferred

- Counter *n* is the two input registers at `16 + 2n` and, over EtherNet/IP, the UDINT at byte `1 + 4n`, little-endian. The manual gives only the ranges.
- Bit *n* of the input word is channel *n*. The manual gives byte and channel ranges, not bit positions; the E1213 on the bench has it this way.
- Relay *n*'s total count is the two input registers at `64 + 2n`.
- What the relays do when the controller is lost: Safe Mode needs the communication watchdog, off by default (pp. 3-4, 3-21).

## Left out of the profile, and why

- **RLY_currentCountReset**: the manual's row gives start address 0048 and start register 00048, which disagree by its own rule (the register is the address plus one). Not used until read on a unit.

## Files

- [`moxa-iologik-e1214.device`](moxa-iologik-e1214.device): the profile a controller copies into a project; the channels above by name.
- [`modbus.map`](modbus.map): the same channels as map lines for `modbus-tcp`, `ADDR` to fill in.
- [`device.toml`](device.toml): the record a lookup matches.

## To make this entry a checked one

- Read this model's EDS (Moxa's product page, Resources, "EDS file"; the site refuses scripted downloads): its product code gives `identity.enip`, its `[Connection Manager]` the connection, and the profile gains its `enip-io` line.
- Put a unit on the bench, note its firmware (the web console's overview, or input registers 5029 and 5031) and drive every channel once: `checked_on`, `firmware` and `checked_by` in `device.toml`.
