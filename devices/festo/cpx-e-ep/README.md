> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Festo CPX-E-EP

EDS identity: vendor 26 Festo AG & Co. KG, product code
14040, device type 12 Communications Adapter,
revision 1.1; EDS file revision
1.1 (02-17-2017).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | I/O Connection (SINT-Format) | 101 / 0..64 (Param1) | 100 / 0..64 (Param2) | 1 |
| Connection2 | Input Only (SINT-Format) | 101 / 0..64 (Param1) | 254 / 0 | 1 |
| Connection3 | Listen Only (SINT-Format) | 101 / 0..64 (Param1) | 255 / 0 | 1 |
| Connection4 | I/O Connection (INT-Format) | 111 / 0..64 (Param1) | 110 / 0..64 (Param2) | 1 |
| Connection5 | Input Only (INT-Format) | 111 / 0..64 (Param1) | 254 / 0 | 1 |
| Connection6 | Listen Only (INT-Format) | 111 / 0..64 (Param1) | 255 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| CPX-E-EP EDS (ODVA marketplace, product 1883) | `6f8a0156a2f41f70…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1883/11634.01-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
