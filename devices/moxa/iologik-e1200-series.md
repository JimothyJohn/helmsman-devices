# Moxa ioLogik E1200 series

The ten models share one manual, one firmware line and one set of system
registers. This page holds what they share; each model's folder holds its
channels. Only the E1213 has been on the bench
([its folder](iologik-e1213/README.md), "On the bench"). Every other
folder is read from documents and says so.

| model | channels | EtherNet/IP in the profile | folder |
| --- | --- | --- | --- |
| E1210 | 16 DI | no (EDS not read) | [iologik-e1210](iologik-e1210/README.md) |
| E1211 | 16 DO | no (EDS not read) | [iologik-e1211](iologik-e1211/README.md) |
| E1212 | 8 DI, 8 DIO | yes, from ODVA's EDS v1.1 | [iologik-e1212](iologik-e1212/README.md) |
| E1213 | 8 DI, 4 DO, 4 DIO (source) | yes, **benched** | [iologik-e1213](iologik-e1213/README.md) |
| E1214 | 6 DI, 6 relays | no (EDS not read) | [iologik-e1214](iologik-e1214/README.md) |
| E1240 | 8 AI | no (EDS not read) | [iologik-e1240](iologik-e1240/README.md) |
| E1241 | 4 AO | no (EDS not read) | [iologik-e1241](iologik-e1241/README.md) |
| E1242 | 4 AI, 4 DI, 4 DIO | no (EDS not read) | [iologik-e1242](iologik-e1242/README.md) |
| E1260 | 6 RTD | no (EDS not read) | [iologik-e1260](iologik-e1260/README.md) |
| E1262 | 8 TC | no (EDS not read) | [iologik-e1262](iologik-e1262/README.md) |

The `-T` variants (-40 to 75 °C) are the same units (manual p. 1-2) and
share their folders.

## Sources

- *ioLogik E1200 Series User's Manual*, Version 15.10, May 2021, SHA-256
  `f8788816b2e0062a68f9b7f1ef9850a2d57f92946ac8b64077c4e77097744454`
  (`pct.wiki.uib.no/images/2/29/Moxa-iologik-e1200-series-manual-v15.10.pdf`).
  Appendix A is the Modbus map per model, Appendix B the EtherNet/IP map.
- One release-notes PDF per model, v1.x to v4.0 (Aug 29, 2025), from
  `moxa.com/Moxa/media/PDIM/S100000327/`. Each folder's `device.toml`
  gives its hash.
- EDS files: the E1213's v2.0 (Moxa) and the E1212's v1.1 (ODVA's
  marketplace, the only ioLogik there). Moxa's site refuses scripted
  downloads, so the other eight models' EDS files have not been read.

## The same on every model

- **Modbus/TCP** on 502, unit id 1 (p. A-2); FC 1, 2, 3, 4, 5, 6, 15, 16.
  The addresses are 0-based PDU addresses (the manual's "Start Address").
- **System registers** (input registers, every model's table):
  `modelName` 5000 (10 words, ASCII), `deviceUpTime` 5020 (2, s),
  `lanMac` 5024 (3), `lanIp` 5027 (2), `firmwareVersion` 5029 (2:
  "V1.2.3 -> 1st byte 1, 2nd byte 2, 3rd byte 3"), `firmwareBuildDate` 5031
  (2: "Build16051718 -> 16051718"), `deviceName` 5040 (30). This is how a
  controller reads a unit's model and firmware over Modbus without the web
  console.
- **EtherNet/IP**: Assembly 101 (0x65) in, 102 (0x66) out (p. B-1); 44818/tcp
  explicit, 2222/udp implicit (Appendix D). Off until enabled in the web
  console (p. 5-1), and from firmware 4.0 off by default again.
- **Factory defaults** (Appendix E): 192.168.127.254/24, communication
  watchdog **off**, DI mode DI, counters stopped, DO mode DO, DO safe status
  disabled, DIO mode DO, AI and AO voltage mode.
- **Safe Mode** (pp. 3-4, 3-21): each output's Hold Last, ON or OFF (an AO's
  value) once the communication watchdog trips. Off by default, so a unit
  out of the box holds its outputs when its controller vanishes. From
  firmware 3.2 Safe Mode covers EtherNet/IP too.
- **Configuration** export and import as a text file, from the web console
  (pp. 3-29) or ioSearch, in bulk for units of one model (pp. 4-6, 4-10).

## Firmware (the release notes, the same builds on every model)

| version | build | date | what a controller sees |
| --- | --- | --- | --- |
| 2.4-2.6 | | | EtherNet/IP arrives (E1211 and E1240 at 2.4, E1213 at 2.6, the rest 2.5; manual p. 5-1), licence registration needed |
| 3.0 | Build17111512 | Jan 16, 2018 | "Update only the next or the previous released firmware version" |
| 3.1 | Build19110615 | Nov 2019 | no registration; `Set_Attribute_Single` works. **The bench E1213 runs this.** |
| 3.2 | Build20111915 | Dec 25, 2020 | implicit messages to UDP 2222 "by default" (before it: another O->T port, 5222 on the bench unit); Safe Mode for EtherNet/IP |
| 3.3 | Build 22072210 | Aug 03, 2022 | "cannot establish second input-only session" fixed; default password "moxa"; **E1241: AO scaled value moves from input register 0 to holding register 0** |
| 3.4 | Build24072310 | Sep 20, 2024 | a login page fix |
| 4.0 | Build24071616 | Aug 29, 2025 | SNMP, EtherNet/IP and RESTful **off by default**; new switch IC for hardware rev. 2.0; RESTful headers change |

Updating a 3.1 unit to 4.0 is four updates (3.2, 3.3, 3.4, 4.0), and after
the last one the unit no longer answers `ListIdentity` until EtherNet/IP is
switched back on. What this means for the library and the box is in
[docs/firmware-and-resilience.md](../../docs/firmware-and-resilience.md).
