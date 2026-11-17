> **Held against one unit on 2026-11-16** for its identity and its connection. Its output
> assembly did not follow the documents' layout, and a lost connection did not stop a move:
> read "On the bench" before sending this drive anything.

# Novanta IMS Liberty / Lexium MDrive Ethernet (LMD), EtherNet/IP

An integrated stepper motor, drive and controller (formerly Schneider Electric Motion USA,
Lexium MDrive). One Ethernet interface that speaks Modbus TCP (as delivered), EtherNet/IP,
PROFINET IO or MCode/TCP, chosen with the vendor's TCP/IP Configuration Utility; this entry is the
EtherNet/IP mode. There is no map and no profile in this folder yet: the output layout is an open
question (`device.toml`), and a map that moves a motor is not published on a guess.

EDS identity: vendor 243 Schneider Electric, product code 15362, device type 43 Generic Device,
revision 2.22; EDS file revision 1.2 (01-17-2012). The unit answered revision 2.36.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 100 / 16 | 112 / 36 | 1 |
| Connection2 | Listen Only | 100 / 16 | 129 / 0 | 1 |
| Connection3 | Input Only | 100 / 16 | 128 / 0 | 1 |

The EDS gives the assemblies no size; 16 and 36 are their members' bits, and what the unit
reports. It gives no RPI, and declares every direction modeless or heartbeat.

## The documents' layout (Fieldbus manual p. 20, EDS)

| assembly | bytes | |
| --- | --- | --- |
| 100 | 0 | bit 0 EF error flag, bit 1 MV moving flag |
| | 1 | IN, the inputs as a group |
| | 4..7 | C1 position counter |
| | 8..11 | C2 encoder counter |
| | 12..15 | LL lead/lag (manual) or V velocity (EDS) |
| 112 | 0..3, 4..7 | A acceleration, D deceleration |
| | 8..11, 12..15 | MA move absolute, MR move relative |
| | 16, 17, 18 | RC run current, HC hold current, OT outputs |
| | 20..23 | SL slew |
| | 24..27, 28..31 | VI, VM initial and maximum velocity |
| | 32.. | TQ and EF (manual, 34 bytes in all) or TE (EDS, 36) |

The manual adds that this mapping "may be changed to any MCode mnemonic of the same data type
using the TCP/IP Configuration Utility".

## On the bench (2026-11-16)

One LMDCE853C at its default address 192.168.33.1, shaft free, set to EtherNet/IP beforehand.
`scripts/enip-identify.py`, a Class 1 connection from Helmsman's `enip-io` and from a stand-alone
originator, and the drive's own MCode/TCP port (503, which answers beside EtherNet/IP) to read
registers back.

```toml
[identity.enip]
vendor_id = 243
device_type = 43
product_code = 15362
revision = '2.36'
status = '0x0000'
product_name = 'MDrive'
```

`PR VR` answers `LMDCM 6.013, Hw: 2.10`.

**The connection**

- Assemblies that answer: 100 (16 bytes) and 112 (36 bytes), no others.
- **O->T takes a 32-bit run/idle header that the EDS does not declare.** A `Forward_Open` at the
  EDS's size is refused, 0x0127 with the size wanted (42). T->O is 16 bytes with no header.
  Helmsman's `enip-io` corrects the header from that refusal, so the vendor's EDS connects.
- Any configuration instance was taken (1, 100, 112, 128). The EDS's input-only and listen-only
  points were refused, 0x012A.
- **It sends more slowly than it grants.** The reply grants the RPI asked for; packets came every
  26 ms at 20, 72 ms at 50, 147 ms at 100, 750 ms at 500, and every 2 ms at 1.
- **It resets the TCP session 2 to 3 s after the `Forward_Open`** and goes on exchanging I/O. A
  `Forward_Close` over a new session is accepted.
- Inputs go to UDP 2222 only: a T->O socket-address item is ignored.
- Twenty minutes at 20 ms, outputs at zero: the first 13 s lost the link over and over (191 connections opened that brought no data, after 40 minutes in which nothing had talked to the drive), then one connection held for the remaining 19 minutes with no loss. Starts after a short pause were clean three times; what the first seconds were is open.

**The bytes**

- Input 100: bit 1 of byte 0 is MV; bit 0 followed the drive enable while `PR EF` read 0; byte 1
  is IN; bytes 4..7 are the position; bytes 8..9 held the error code (`PR ER`), not an encoder
  count.
- Output 112 did not follow the table above. One field changed at a time, drive disabled, read
  back over MCode: bytes 0..3 set the position counter; byte 17 non-zero enabled the drive and
  zero disabled it; byte 18 set the run current; bytes 20..23 are SL (5000 gave exactly 5000
  steps/s, 0 stopped). Bytes 4..7 started a move once the drive was enabled.
- **A field acts when it changes** from the last image the drive saw, across connections: the
  same image sent again on a new connection does nothing.
- **The first image built from the manual's table started a move at the `Forward_Open`** that
  reached about 1.1 million steps/s (some 1300 rpm) before SL brought it down. Do not send this
  drive an image from the table until its mapping has been read from the Configuration Utility.

**When the controller goes away** (slewing at 5000 steps/s, RPI 20 ms)

| the controller | the drive |
| --- | --- |
| sends `Forward_Close` | stops |
| sets the run/idle header to idle | stops |
| goes silent | keeps slewing: still 5000 steps/s after 10 s, until `SL 0` over MCode |

A pulled cable or a dead controller does not stop this drive. That stop has to be the drive's own.

Not run: MA and MR as position moves, the digital inputs and outputs, the closed-loop (hMT)
registers, explicit messages to the vendor objects beyond reads, any RPI above 500 ms.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| LMD Ethernet TCP/IP Application 2.4.0.9 (firmware package; carries the EDS) | `1bb0038ceae46daf…` | https://www.novantaims.com/download/lmd-ethernet-tcp-ip-application-2-4-0-9/?wpdmdl=33950&refresh=6afbcc0d386a61794886669; retrieved 2026-11-17; not redistributed here |
| Lexium MDrive Ethernet, LMDxE57C and LMDxE85C product manual (03.2015) | `1c90c18f9a1c4b09…` | https://novanta.com/robotics-automation/wp-content/uploads/sites/3/2015/04/LMDxE57-85C.pdf; retrieved 2026-11-17; not redistributed here |
| LM57/LM85 Ethernet TCP/IP with M12 circular connectors (LMDE57-85IP hardware manual) | `750e8e1baf96fa67…` | https://www.novantaims.com/download/liberty-mdrive-ethernet-nema-2334-ip65/?wpdmdl=6719&refresh=6afbcc022b7b31794886658; retrieved 2026-11-17; not redistributed here |
| LM57/LM85 Ethernet TCP/IP with pluggable connectors (LMDE57-85 hardware manual) | `dc3bb12d1b298678…` | https://www.novantaims.com/download/liberty-mdrive-ethernet-nema-2334/?wpdmdl=6713&refresh=6afbcc028ff621794886658; retrieved 2026-11-17; not redistributed here |
| LMD EtherNet/IP Protocol Implementation | `2a5a6f726b2a5b2f…` | https://www.novantaims.com/download/liberty-mdrive-ethernetip/?wpdmdl=6728&refresh=6afbcc0fb6ea01794886671; retrieved 2026-11-17; not redistributed here |
| LMD MCode OS Programming and Reference | `3945e47f63d49752…` | https://www.novantaims.com/download/lmd-mcode-os-programming-and-reference/?wpdmdl=29637&refresh=6afbcc01dcbd91794886657; retrieved 2026-11-17; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
