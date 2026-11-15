# Moxa ioLogik E1260

Remote Ethernet I/O: 6 RTD inputs, two switched Ethernet ports, Modbus/TCP server and EtherNet/IP
adapter (manual p. 1-2). The E1260-T is the same unit for -40 to 75 °C.

**Not checked on a unit.** Everything here is read from Moxa's documents. What the
family's one benched member showed is in [the E1213's folder](../iologik-e1213/README.md),
and what the series shares, firmware history included, in
[iologik-e1200-series.md](../iologik-e1200-series.md).

## Sources

| | what | where |
| --- | --- | --- |
| **Manual** | *ioLogik E1200 Series User's Manual*, Version 15.10, May 2021, 10 137 362 bytes, SHA-256 `f8788816b2e0062a68f9b7f1ef9850a2d57f92946ac8b64077c4e77097744454`. "p. X-N" is the manual's own page number. | `pct.wiki.uib.no/images/2/29/Moxa-iologik-e1200-series-manual-v15.10.pdf` (a university mirror; fetched 2026-11-12, the hash is the one the E1213's folder gives). Not in this repository. |
| **Release notes** | *Firmware for ioLogik E1200 Series (ioLogik E1260/E1260-T) Release Notes*, to v4.0 (Build24071616, Aug 29, 2025), 63474 bytes, SHA-256 `c175dd5e616c0fd4c4182be34067ff84b418870ff7b194ffde0b4da9cd964ae8`. "RN" below. | Fetched 2026-11-12 from `moxa.com/Moxa/media/PDIM/S100000327/` (the "firmware v4.0.1kp Software Release History" PDF for the E1260). Not in this repository. |

## Channels

6 RTD inputs, RTD-00..RTD-05. Each channel has a sensor type and a unit set in the web console;
the "multiplied engineering value" is the measurement times ten in that unit, as one word.

## Modbus/TCP (manual p. A-16)

Port 502 (Appendix D), unit id 1 by default (p. A-2). Addresses are the manual's 0-based "Start
Address" (the `modbus-tcp` driver's address); its "Start Register" column is the same plus the
1-based table prefix.

| name | table | address | count | `modbus-tcp` point |
| --- | --- | --- | --- | --- |
| RTD_multipliedEngineeringValue, "Unit: 0.1" | input register | 1536 | 6 | `ir:1536:i16`..`ir:1541:i16` |
| RTD_scaledValue, "high/low word" | input register | 1548 | 12 (2 a channel) | (not in the profile: see below) |
| RTD_multipliedEngineeringValueMin / Max | input register 1560, 1572 |  | 6 | (not in the profile) |
| RTD_resetMinValue / resetMaxValue | coil 4161, 4169 |  | 6 | (not in the profile) |

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

Input assembly 101 (0x65), 12 bytes by the manual's table:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0-11 | rtdValueEngineeringMultiplied, "RTD Engineering Multiplied value" | UINT | RTD-00..RTD-05 |

The manual lists no output data for this model (p. B-2): there is nothing to own, so a
controller would hold an Input Only connection.

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

v3.1 also fixed "the offset scaling value will reset after changing the Alias name (E1260)".

## Inferred

- Channel *n* is input register `1536 + n` and, over EtherNet/IP, the UINT at byte `2n`.
- **The sign.** The manual types the value as a word (UINT on EtherNet/IP) and an RTD reads below zero. The profile reads it as `i16`, two's complement: the same as the manual's unsigned word for every value from 0 up, and the usual encoding below. Not seen on a unit.

## Left out of the profile, and why

- **RTD_scaledValue** (input registers from 1548, two words a channel): "high/low word" with no format; a REAL on EtherNet/IP's RTD Channel Object (p. B-4), so probably `f32`, high word first. Unread on a unit, so not in the profile.

## Files

- [`moxa-iologik-e1260.device`](moxa-iologik-e1260.device): the profile a controller copies into a project; the channels above by name.
- [`modbus.map`](modbus.map): the same channels as map lines for `modbus-tcp`, `ADDR` to fill in.
- [`device.toml`](device.toml): the record a lookup matches.

## To make this entry a checked one

- Read this model's EDS (Moxa's product page, Resources, "EDS file"; the site refuses scripted downloads): its product code gives `identity.enip`, its `[Connection Manager]` the connection, and the profile gains its `enip-io` line.
- Put a unit on the bench, note its firmware (the web console's overview, or input registers 5029 and 5031) and drive every channel once: `checked_on`, `firmware` and `checked_by` in `device.toml`.
- On that unit: a sensor below 0 °C (or a decade box), to settle the sign of the x10 word.
