> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Yaskawa Yaskawa SI-EN3D for CIPR-GA80U2004

EDS identity: vendor 44 Yaskawa America, Inc., product code
24192, device type 2 AC Drive Device,
revision 2.8; EDS file revision
2.8 (04-01-2022).

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

The EDS is the SI-EN3D (dual-port option) file for the CIPR-GA80U2004, a GA800 model, from the ODVA marketplace listing 1740. The listing's zip carries one EDS per drive model; this folder uses the GA800 one. Yaskawa's own page lists the SI-EN3D EDS v2.008, but that zip is refused by `docs-fetch.py` (member count).

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Yaskawa 1740 listing: declaration of conformity (ODVA), ODVA marketplace product 1740 | `f22fff86a4ab1ca4…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1740/11453_DOC_082222.pdf; retrieved 2026-11-23; not redistributed here |
| Yaskawa 1740 listing: EDS, ODVA marketplace product 1740 | `c5a10ca71a76cbd1…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1740/11453.04-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
