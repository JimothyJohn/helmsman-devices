# Moxa ioLogik E1241

Remote Ethernet I/O: 4 AO, two switched Ethernet ports, Modbus/TCP server and EtherNet/IP adapter
(manual p. 1-2). The E1241-T is the same unit for -40 to 75 °C.

**Not checked on a unit.** Everything here is read from Moxa's documents. What the
family's one benched member showed is in [the E1213's folder](../iologik-e1213/README.md),
and what the series shares, firmware history included, in
[iologik-e1200-series.md](../iologik-e1200-series.md).

## Sources

| | what | where |
| --- | --- | --- |
| **Manual** | *ioLogik E1200 Series User's Manual*, Version 15.10, May 2021, 10 137 362 bytes, SHA-256 `f8788816b2e0062a68f9b7f1ef9850a2d57f92946ac8b64077c4e77097744454`. "p. X-N" is the manual's own page number. | `pct.wiki.uib.no/images/2/29/Moxa-iologik-e1200-series-manual-v15.10.pdf` (a university mirror; fetched 2026-11-12, the hash is the one the E1213's folder gives). Not in this repository. |
| **Release notes** | *Firmware for ioLogik E1200 Series (ioLogik E1241/E1241-T) Release Notes*, to v4.0 (Build24071616, Aug 29, 2025), 63630 bytes, SHA-256 `28c70f0d56345d3617c4c19cd468f49465d31ffad1b9349fcc0e1002f91802da`. "RN" below. | Fetched 2026-11-12 from `moxa.com/Moxa/media/PDIM/S100000327/` (the "firmware v4.0.1kp Software Release History" PDF for the E1241). Not in this repository. |

## Channels

4 analog outputs, AO-00..AO-03, each in a mode (0: 0-10 V, 1: 4-20 mA, 2: 0-20 mA; voltage by
default, Appendix E). The profile's safe value is raw 0, the bottom of the range in every mode.

## Modbus/TCP (manual p. A-12)

Port 502 (Appendix D), unit id 1 by default (p. A-2). Addresses are the manual's 0-based "Start
Address" (the `modbus-tcp` driver's address); its "Start Register" column is the same plus the
1-based table prefix.

| name | table | address | count | `modbus-tcp` point |
| --- | --- | --- | --- | --- |
| AO_rawValue | holding register | 1024 | 4 | `hr:1024`..`hr:1027` |
| AO_scaledValue, "high/low word" | input register 0 to firmware 3.2, holding register 0 from 3.3 | 0 | 8 (2 a channel) | (not in the profile: see "What depends on the firmware") |
| AO_p2pStatus / p2pSafeModeFlag / FlagClear | di 4096, 4112, coil 4128 |  | 4 | (peer-to-peer and safe mode; not in the profile) |

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

Input assembly 101 (0x65), 8 bytes by the manual's table:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0-7 | aoValueRaw, "AO raw value" | UINT | AO-00..AO-03 |

Output assembly 102 (0x66), 8 bytes:

| bytes | name | type | channels |
| --- | --- | --- | --- |
| 0-7 | aoValueRaw | UINT | AO-00..AO-03 |

## What depends on the firmware

The ten E1200 models share one firmware line (the same builds on the same dates in every model's
release notes). What moves with it, from this model's notes:

| firmware | what changed for a controller |
| --- | --- |
| before 2.5 | no EtherNet/IP (manual p. 5-1) |
| 3.0 | "Update only the next or the previous released firmware version": updates go one release at a time |
| 3.1 | EtherNet/IP needs no licence registration any more; `Set_Attribute_Single` works |
| 3.2 | "Ethernet/IP implicit messages are sent to port 2222 by default": before it the unit names another UDP port for O->T data in its `Forward_Open` reply (5222 on the E1213 at 3.1) and ignores data sent to 2222; Safe Mode covers EtherNet/IP |
| 3.3 | "Ethernet/IP cannot establish second input-only session" fixed; a default password ("moxa") and a login policy; **AO_scaledValue moves** (below) |
| 4.0 | SNMP, EtherNet/IP and RESTful are **off by default**: a unit updated or shipped at 4.0 does not answer `ListIdentity` until EtherNet/IP is switched on in its web console; Modbus/TCP stays on |

**The scaled value's register moved at 3.3.** The release notes for v3.3 (Aug 03, 2022), under Changes:
"AO Scaled Value Modbus address changes from 30001 to 40001", "Function code changes from 04:input
register to 03:holding register", and the value becomes read-write in SNMP and AOPC. The manual at
hand (v15.10, May 2021) is older and shows input register 0, read-only. So the same request reads the
scaled value on a unit at 3.2 and fails on one at 3.3, and the reverse. The raw value at holding
register 1024 is the same on both, which is why the profile uses it and nothing else.

## Inferred

- Channel *n*'s raw value is holding register `1024 + n` and, over EtherNet/IP, the UINT at byte `2n`.
- The raw range 0..4095 is the Safe Mode value's range (p. 3-21); the register's own range is not given.
- What the outputs do when the controller is lost: each channel's Safe Mode value or hold-last, once the communication watchdog (off by default) trips (pp. 3-4, 3-21).

## Left out of the profile, and why

- **AO_scaledValue**: which table it is in depends on the firmware (above), and its format is not stated ("high/low word"; a REAL on EtherNet/IP's AO Channel Object, p. B-4). A profile cannot yet say "this point on firmware 3.3 and later", so it is left out rather than right for half the units.

## Files

- [`moxa-iologik-e1241.device`](moxa-iologik-e1241.device): the profile a controller copies into a project; the channels above by name.
- [`modbus.map`](modbus.map): the same channels as map lines for `modbus-tcp`, `ADDR` to fill in.
- [`device.toml`](device.toml): the record a lookup matches.

## To make this entry a checked one

- Read this model's EDS (Moxa's product page, Resources, "EDS file"; the site refuses scripted downloads): its product code gives `identity.enip`, its `[Connection Manager]` the connection, and the profile gains its `enip-io` line.
- Put a unit on the bench, note its firmware (the web console's overview, or input registers 5029 and 5031) and drive every channel once: `checked_on`, `firmware` and `checked_by` in `device.toml`.
- On that unit: the scaled value at input register 0 and at holding register 0, with the unit's firmware noted, to confirm the move at 3.3.
