> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Festo CPX-FB32

EDS identity: vendor 26 Festo Corporation, product code
13002, device type 12 Communications Adapter,
revision 1.1; EDS file revision
1.1 (03-09-2005).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Class1 Server | 101 / 13 | 100 / 11 | 102 |
| Connection2 | Input Only | 101 / 13 | 1 / 0 | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| CPX-FB32 EDS (ODVA marketplace, product 981) | `38fe88d6f2c17f77…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/981/CPX-FB32.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
