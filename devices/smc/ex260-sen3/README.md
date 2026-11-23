> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# SMC EX260-SEN3

EDS identity: vendor 7 SMC Corporation, product code
158, device type 27 Pneumatic Valve(s),
revision 2.2; EDS file revision
2.1 (09-25-2015).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 100 / 2 | 150 / 2 | 105 |
| Connection2 | Listen Only | 100 / 2 | 151 / 0 | 105 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| EX260-SEN1/2/3/4 EDS (ODVA marketplace, product 1560) | `e54c0c294aa5d150…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1560/11007_EDS_file.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
