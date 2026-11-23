> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# SMC Corporation EX600-SEN1

EDS identity: vendor 7 SMC Corporation, product code
126, device type 12 Communications Adapter,
revision 1.1; EDS file revision
1.1 (04-02-2009).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 100 / 0..64 (Param2) | 150 / 0..64 (Param1) | 5 |
| Connection2 | Input Only | 100 / 0..64 (Param2) | 103 / 0 | 5 |
| Connection3 | Listen Only | 100 / 0..64 (Param2) | 104 / 0 | 5 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| EX600-SEN1/SEN2 EDS (ODVA marketplace, product 1049) | `4d80cffe24e536c6…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1049/EX600_SEN_.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
