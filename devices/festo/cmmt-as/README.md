> **Draft from documents.** No unit has been checked. Identity and connections
> are the EDS's, read by `scripts/eds-draft.py`; the points are read from the
> CMMT-AS-...-S1 manual, with the page for each. No unit has confirmed any of them.

# Festo CMMT-AS-EP

EDS identity: vendor 26 Festo, product code
65282, device type 43 Generic Device,
revision 1.1; EDS file revision
1.4 (03-16-2023).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | DriveProfile - Exclusive Owner | 101 / 24..24 (Param6) | 100 / 24..24 (Param5) | 102 |
| Connection2 | DriveProfile - Input Only | 101 / 24..24 (Param6) | 254 / 0 | 102 |
| Connection3 | DriveProfile - Listen Only | 101 / 24..24 (Param6) | 255 / 0 | 102 |
| Connection4 | Extended Process Data - Exclusive Owner | 111 / 32..32 (Param8) | 110 / 32..32 (Param7) | 102 |
| Connection5 | Extended Process Data - Listen Only | 111 / 32..32 (Param8) | 255 / 0 | 102 |

## Points

26 points from the CMMT-AS-...-S1 manual (2026-06p), chapter 14, PDF p. 880 to
921. The EDS names the 12 words of the DriveProfile image and the 16 words of
Extended Process Data only as anonymous 16-bit members. What a word is depends
on the telegram chosen with `Telegram selection` (P0.3030101): the manual's
Tab. 1159 and 1160 (PDF p. 881) list the process data words (PZD) of
telegrams 1, 9, 102 and 111. The points are for **telegram 111** (single
positioning with record selection and MDI: the one that fills all 12 words)
and, for the two speed words, **telegram 1**; their names start `T111` and
`T1`, and they overlap, since only one telegram is active. Telegrams 9 and 102
are not written out. Extended Process Data (assemblies 110/111, 32 bytes) is
up to 8 parameters mapped with the plug-in, so it is one point each way.

Every point lists its bits or scaling and the table column read. Byte offsets
are inferred: the manual numbers PZD1 to PZD12 and gives no byte offsets or
byte order, so PZD n is taken as bytes 2(n-1) and 2(n-1)+1 (see the open
questions). Where the table merges two PZD for a 32-bit value (the position
and velocity words) that is read from the image of the table, since the text
extraction loses it. Speed is standardised to 0x4000 (16 bit) or 0x40000000
(32 bit) = 100 %; positions and MDI velocity are in user units set by the
factor group. The manual's POS_STW1 bit table marks bit 12 reserved while its
PNU table lists "POS_STW1.12 Setpoint transfer": left out of the points.

No unit has confirmed any of this.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| CMMT-AS / CMMT-ST EtherNet/IP EDS (ODVA marketplace, product 2342) | `49a30233e0d5ee3c…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2342/11965.03-EDS.zip; retrieved 2026-11-23; not redistributed here |
| Manual CMMT-AS-...-S1 (2026-06p), 924 pages | `7688e16ae76d2756…` | https://www.festo.com/assets/attachment/en/665942, downloaded in a browser 2026-11-23; private store |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
