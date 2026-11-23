> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Mitsubishi Electric FR-E800-SCE

EDS identity: vendor 161 Mitsubishi Electric, product code
63, device type 2 AC Drive Device,
revision 1.1; EDS file revision
1.0 (01-16-2020).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Basic Speed Control | 70 /  | 20 /  |  |
| Connection2 | Input Only - Basic Speed Control | 70 /  | 197 / 0 |  |
| Connection3 | Listen Only - Basic Speed Control | 70 /  | 198 / 0 |  |
| Connection4 | Extended Speed Control | 71 /  | 21 /  |  |
| Connection5 | Input Only - Extended Speed Control | 71 /  | 197 / 0 |  |
| Connection6 | Listen Only - Extended Speed Control | 71 /  | 198 / 0 |  |
| Connection7 | Speed and Torque Control | 72 /  | 22 /  |  |
| Connection8 | Input Only - Speed and Torque Control | 72 /  | 197 / 0 |  |
| Connection9 | Listen Only - Speed and Torque Control | 72 /  | 198 / 0 |  |
| Connection10 | Extended Speed and Torque Control | 73 /  | 23 /  |  |
| Connection11 | Input Only - Extended Speed and Torque Control | 73 /  | 197 / 0 |  |
| Connection12 | Listen Only - Extended Speed and Torque Control | 73 /  | 198 / 0 |  |
| Connection13 | Safety Output | 196 /  | 140 /  | 196 |
| Connection14 | Safety Input | 190 /  | 196 /  | 196 |

## Scope

FR-E800-SCE: the safety-function variant of the FR-E800 with Ethernet. Product code 63, next to the FR-E800-E's 62.

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Mitsubishi Electric FR-E800-SCE: declaration of conformity (ODVA), ODVA marketplace product 2231 | `75334048f965586f…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2231/11935_DOC_051320.pdf; retrieved 2026-11-23; not redistributed here |
| Mitsubishi Electric FR-E800-SCE: EDS, ODVA marketplace product 2231 | `60cd04c579446102…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2231/00A10002003F0100.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
