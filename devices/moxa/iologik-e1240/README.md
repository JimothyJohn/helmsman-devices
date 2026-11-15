# Moxa ioLogik E1240

Remote Ethernet I/O: 8 AI, two switched Ethernet ports, Modbus/TCP server and EtherNet/IP adapter
(manual p. 1-2). The E1240-T is the same unit for -40 to 75 °C.

**Not checked on a unit.** Everything here is read from Moxa's documents. What the
family's one benched member showed is in [the E1213's folder](../iologik-e1213/README.md),
and what the series shares, firmware history included, in
[iologik-e1200-series.md](../iologik-e1200-series.md).

## Sources

| | what | where |
| --- | --- | --- |
| **Manual** | *ioLogik E1200 Series User's Manual*, Version 15.10, May 2021, 10 137 362 bytes, SHA-256 `f8788816b2e0062a68f9b7f1ef9850a2d57f92946ac8b64077c4e77097744454`. "p. X-N" is the manual's own page number. | `pct.wiki.uib.no/images/2/29/Moxa-iologik-e1200-series-manual-v15.10.pdf` (a university mirror; fetched 2026-11-12, the hash is the one the E1213's folder gives). Not in this repository. |
| **Release notes** | *Firmware for ioLogik E1200 Series (ioLogik E1240/E1240-T) Release Notes*, to v4.0 (Build24071616, Aug 29, 2025), 64702 bytes, SHA-256 `8362136b310a248420c6282ed7bb8a1740b295c2c6a59003d328b40f26152fce`. "RN" below. | Fetched 2026-11-12 from `moxa.com/Moxa/media/PDIM/S100000327/` (the "firmware v4.0.1kp Software Release History" PDF for the E1240). Not in this repository. |

## Channels

8 analog inputs, AI-00..AI-07, each voltage or current by a jumper inside the unit (p. 2-4;
voltage by default, Appendix E) and a mode (0: 0-10 V, 1: 4-20 mA, 2: 0-20 mA, 4: 4-20 mA with
burnout detection). The more channels are enabled the slower each is sampled: 12 Hz with one,
1.5 Hz with all eight (chapter 3, "AI Channels").

## Modbus/TCP (manual p. A-11)

Port 502 (Appendix D), unit id 1 by default (p. A-2). Addresses are the manual's 0-based "Start
Address" (the `modbus-tcp` driver's address); its "Start Register" column is the same plus the
1-based table prefix.

| name | table | address | count | `modbus-tcp` point |
| --- | --- | --- | --- | --- |
| AI_rawValue | input register | 0 | 8 | `ir:0`..`ir:7` |
| AI_scaledValue, "high/low word" | input register | 8 | 16 (2 a channel) | (not in the profile: see below) |
| AI_status | input register | 60 | 8 | `ir:60`..`ir:67` |
| AI_mode | holding register | 24 | 8 | (0: 0-10 V, 1: 4-20 mA, 2: 0-20 mA, 4: 4-20 mA burnout; not in the profile) |

"High/low word" is high word first, the driver's default for `u32` (no `sw`). The system registers
(model name, firmware version and build date, MAC, uptime) are the same on every E1200 and are in the
series page.

## EtherNet/IP (manual pp. B-1, B-2)

The unit is an EtherNet/IP adapter from firmware 2.4 (p. 5-1; off by default from 4.0). The manual gives the
assembly instances and what the bytes mean; it does not give the product code, the configuration
instance, the RPI range or the connection's real-time format. Those are in the model's EDS, which has not
been read, so `device.toml` has no `identity.enip` and the profile reaches this model over Modbus/TCP only.
On the two siblings whose EDS has been read (E1212, E1213) the connection is the same: configuration
instance 100, exclusive owner on 102 and 101, input only on heartbeat 111, RPI 100 ms to 3 s.

Input assembly 101 (0x65), 16 bytes by the manual's table:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0-15 | aiValueRaw, "AI raw value" | UINT | AI-00..AI-07 |

The manual lists no output data for this model (p. B-2): there is nothing to own, so a
controller would hold an Input Only connection.

## What depends on the firmware

The ten E1200 models share one firmware line (the same builds on the same dates in every model's
release notes). What moves with it, from this model's notes:

| firmware | what changed for a controller |
| --- | --- |
| before 2.4 | no EtherNet/IP (manual p. 5-1) |
| 3.0 | "Update only the next or the previous released firmware version": updates go one release at a time |
| 3.1 | EtherNet/IP needs no licence registration any more; `Set_Attribute_Single` works |
| 3.2 | "Ethernet/IP implicit messages are sent to port 2222 by default": before it the unit names another UDP port for O->T data in its `Forward_Open` reply (5222 on the E1213 at 3.1) and ignores data sent to 2222; Safe Mode covers EtherNet/IP |
| 3.3 | "Ethernet/IP cannot establish second input-only session" fixed; a default password ("moxa") and a login policy |
| 4.0 | SNMP, EtherNet/IP and RESTful are **off by default**: a unit updated or shipped at 4.0 does not answer `ListIdentity` until EtherNet/IP is switched on in its web console; Modbus/TCP stays on |

## Inferred

- Channel *n*'s raw value is input register `0 + n` and, over EtherNet/IP, the UINT at byte `0 + 2n`.

## Left out of the profile, and why

- **AI_scaledValue** (input registers from 8, two words a channel). The manual says "high/low word" and nothing about the number's format; the same value is a REAL on EtherNet/IP's AI Channel Object (p. B-3), so it is probably an IEEE float, high word first (`f32`). Nobody has read one from a unit, and a wrong format reads as a plausible wrong number, so the profile carries the raw value only.

## Files

- [`moxa-iologik-e1240.device`](moxa-iologik-e1240.device): the profile a controller copies into a project; the channels above by name.
- [`modbus.map`](modbus.map): the same channels as map lines for `modbus-tcp`, `ADDR` to fill in.
- [`device.toml`](device.toml): the record a lookup matches.

## To make this entry a checked one

- Read this model's EDS (Moxa's product page, Resources, "EDS file"; the site refuses scripted downloads): its product code gives `identity.enip`, its `[Connection Manager]` the connection, and the profile gains its `enip-io` line.
- Put a unit on the bench, note its firmware (the web console's overview, or input registers 5029 and 5031) and drive every channel once: `checked_on`, `firmware` and `checked_by` in `device.toml`.
- On that unit: a known voltage on one channel, read as the raw word and as the scaled value in both word orders, so the profile can carry a `real` channel with its unit.
