> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Yaskawa America, Inc. Yaskawa GA501

EDS identity: vendor 44 Yaskawa America, Inc., product code
24063, device type 2 AC Drive Device,
revision 1.5; EDS file revision
1.005 (02-01-2024).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Basic Speed Control | 70 / 4 | 20 / 4 | 6 |
| Connection2 | Extended Speed Control | 71 / 4 | 21 / 4 | 6 |
| Connection3 | Basic Speed & Torque Control | 72 / 6 | 22 / 6 | 6 |
| Connection4 | Extended Speed & Torque Control | 73 / 6 | 23 / 6 | 6 |
| Connection5 | Memobus Message | 150 / 5 | 100 / 5 | 6 |
| Connection6 | Standard Speed & Torque Control | 151 / 8 | 101 / 8 | 6 |
| Connection7 | High Speed & Torque Control | 155 / 40 | 115 / 40 | 6 |
| Connection8 | Dynamic Control | 166 / 44 | 116 / 44 | 6 |
| Connection9 | Dynamic 2 Control | 167 / 8 | 117 / 8 | 6 |
| Connection10 | Dynamic 4 Control | 168 / 12 | 118 / 12 | 6 |
| Connection11 | Dynamic 7 Control | 169 / 18 | 119 / 18 | 6 |
| Connection12 | Dynamic 10 Control | 170 / 24 | 120 / 24 | 6 |
| Connection13 | Input Only | 70 / 4 | 128 / 0 | 1 |
| Connection14 | Listen Only | 70 / 4 | 129 / 0 | 1 |

## Scope

The EDS names the GA501 (the GA500 series with the EtherNet/IP option). Yaskawa's EDS page for the SI-EN3 also lists the GA500; its zip holds 2816 members and `docs-fetch.py` refuses it (over 2000), so the SI-EN3 EDS is not in the library.

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Yaskawa GA500 / GA501 EtherNet/IP: declaration of conformity (ODVA), ODVA marketplace product 2770 | `0b341fd56f7767f8…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2770/12536_DOC_091124.pdf; retrieved 2026-11-23; not redistributed here |
| Yaskawa GA500 / GA501 EtherNet/IP: EDS, ODVA marketplace product 2770 | `9196ed40cfb7ddda…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2770/GA501_v1.005.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
