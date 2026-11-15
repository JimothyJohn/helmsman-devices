# Moxa ioLogik E1262

Remote Ethernet I/O: 8 thermocouple inputs, two switched Ethernet ports, Modbus/TCP server and
EtherNet/IP adapter (manual p. 1-2). The E1262-T is the same unit for -40 to 75 °C.

**Not checked on a unit.** Everything here is read from Moxa's documents. What the
family's one benched member showed is in [the E1213's folder](../iologik-e1213/README.md),
and what the series shares, firmware history included, in
[iologik-e1200-series.md](../iologik-e1200-series.md).

## Sources

| | what | where |
| --- | --- | --- |
| **Manual** | *ioLogik E1200 Series User's Manual*, Version 15.10, May 2021, 10 137 362 bytes, SHA-256 `f8788816b2e0062a68f9b7f1ef9850a2d57f92946ac8b64077c4e77097744454`. "p. X-N" is the manual's own page number. | `pct.wiki.uib.no/images/2/29/Moxa-iologik-e1200-series-manual-v15.10.pdf` (a university mirror; fetched 2026-11-12, the hash is the one the E1213's folder gives). Not in this repository. |
| **Release notes** | *Firmware for ioLogik E1200 Series (ioLogik E1262/E1262-T) Release Notes*, to v4.0 (Build24071616, Aug 29, 2025), 63549 bytes, SHA-256 `f9999a03690521f52eb5df1b654d9ea41a0de3aba9291986a8d8eec437b92427`. "RN" below. | Fetched 2026-11-12 from `moxa.com/Moxa/media/PDIM/S100000327/` (the "firmware v4.0.1kp Software Release History" PDF for the E1262). Not in this repository. |

## Channels

8 thermocouple inputs, TC-00..TC-07. Each channel has a sensor type and a unit set in the web
console; the "multiplied engineering value" is the measurement times ten in Celsius or
Fahrenheit, or in units of 0.0001 mV when the channel is in a millivolt mode, as two words.

## Modbus/TCP (manual p. A-18)

Port 502 (Appendix D), unit id 1 by default (p. A-2). Addresses are the manual's 0-based "Start
Address" (the `modbus-tcp` driver's address); its "Start Register" column is the same plus the
1-based table prefix.

| name | table | address | count | `modbus-tcp` point |
| --- | --- | --- | --- | --- |
| TC_multipliedEngineeringValue, "high/low word, Unit: 0.1 (Celsius, Fahrenheit) or 0.0001 (mV)" | input register | 2048 | 16 (2 a channel) | `ir:2048:i32` (TC-00) .. `ir:2062:i32` |
| TC_scaledValue, "high/low word" | input register | 2064 | 16 (2 a channel) | (not in the profile: see below) |
| TC_multipliedEngineeringValueMin / Max | input register 2080, 2096 |  | 16 | (not in the profile) |
| TC_resetMinValue / resetMaxValue, TC CJC calibration start | coil 4177, 4185, 4193 |  | 8 | (not in the profile) |

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

Input assembly 101 (0x65), 32 bytes by the manual's table:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0-31 | tcValueEngineeringMultiplied, "TC Engineering Multiplied value" | UDINT | TC-00..TC-07 |

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

## Inferred

- Channel *n* is the two input registers at `2048 + 2n` and, over EtherNet/IP, the UDINT at byte `4n`.
- **The sign.** The manual types the value as two words (UDINT on EtherNet/IP) and a thermocouple reads below zero. The profile reads it as `i32`, two's complement, high word first. Not seen on a unit.

## Left out of the profile, and why

- **TC_scaledValue** (input registers from 2064, two words a channel): "high/low word" with no format; a REAL on EtherNet/IP's TC Channel Object (p. B-4), so probably `f32`, high word first. Unread on a unit, so not in the profile.

## Files

- [`moxa-iologik-e1262.device`](moxa-iologik-e1262.device): the profile a controller copies into a project; the channels above by name.
- [`modbus.map`](modbus.map): the same channels as map lines for `modbus-tcp`, `ADDR` to fill in.
- [`device.toml`](device.toml): the record a lookup matches.

## To make this entry a checked one

- Read this model's EDS (Moxa's product page, Resources, "EDS file"; the site refuses scripted downloads): its product code gives `identity.enip`, its `[Connection Manager]` the connection, and the profile gains its `enip-io` line.
- Put a unit on the bench, note its firmware (the web console's overview, or input registers 5029 and 5031) and drive every channel once: `checked_on`, `firmware` and `checked_by` in `device.toml`.
- On that unit: a junction below 0 °C (or a millivolt source), to settle the sign of the x10 value.
