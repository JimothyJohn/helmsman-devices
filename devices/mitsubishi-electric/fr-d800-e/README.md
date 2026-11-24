> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Mitsubishi Electric FR-D800-E

EDS identity: vendor 161 Mitsubishi Electric Corporation, product code
112, device type 2 AC Drive,
revision 1.1; EDS file revision
1.0 (10-03-2024).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Basic Speed Control | 70 / 4 | 20 / 4 |  |
| Connection2 | Input Only - Basic Speed Control | 70 / 4 | 197 / 0 |  |
| Connection3 | Listen Only - Basic Speed Control | 70 /  | 198 / 0 |  |
| Connection4 | Extended Speed Control | 71 / 4 | 21 / 4 |  |
| Connection5 | Input Only - Extended Speed Control | 71 / 4 | 197 / 0 |  |
| Connection6 | Listen Only - Extended Speed Control | 71 /  | 198 / 0 |  |
| Connection7 | Speed and Torque Control | 72 / 6 | 22 / 6 |  |
| Connection8 | Input Only - Speed and Torque Control | 72 / 6 | 197 / 0 |  |
| Connection9 | Listen Only - Speed and Torque Control | 72 /  | 198 / 0 |  |
| Connection10 | Extended Speed and Torque Control | 73 / 6 | 23 / 6 |  |
| Connection11 | Input Only - Extended Speed and Torque Control | 73 / 6 | 197 / 0 |  |
| Connection12 | Listen Only - Extended Speed and Torque Control | 73 /  | 198 / 0 |  |
| Connection13 | Configurable | 150 / 0..62 (Param3002) | 100 / 0..46 (Param3001) |  |
| Connection14 | Input Only - Configurable | 150 / 0..62 (Param3002) | 197 / 0 |  |
| Connection15 | Listen Only - Configurable | 150 / 0..62 (Param3002) | 198 / 0 |  |

## Scope

FR-D800-E, a candidate substituted for the FR-A800-E: no EDS for the FR-A800-E was found.

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Mitsubishi Electric FR-D800-E: declaration of conformity (ODVA), ODVA marketplace product 2787 | `0a5fd017960cf765…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2787/12552_DOC_110624.pdf; retrieved 2026-11-23; not redistributed here |
| Mitsubishi Electric FR-D800-E: EDS, ODVA marketplace product 2787 | `c90227479e640e11…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2787/12552.01.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
