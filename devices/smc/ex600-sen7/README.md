> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# SMC EX600-SEN7/SEN8

EDS identity: vendor 7 SMC Corporation, product code
258, device type 12 Communications Adapter,
revision 1.1; EDS file revision
1.0 (08-18-2021).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 100 / 0..1210 (Param2) | 150 / 0..1210 (Param1) | 105 |
| Connection2 | Input Only | 100 / 0..1210 (Param2) | 103 / 0 | 105 |
| Connection3 | Listen Only | 100 / 0..1210 (Param2) | 104 / 0 | 105 |
| Connection4 | Input Only Ext | 100 / 0..1210 (Param2) | 106 / 0 | 105 |
| Connection5 | Listen Only Ext | 100 / 0..1210 (Param2) | 107 / 0 | 105 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| EX600-SEN7/SEN8 EDS (ODVA marketplace, product 2421) | `ee69b338e86b2627…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2421/12174.01-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
