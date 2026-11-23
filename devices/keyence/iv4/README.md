> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Keyence Corporation IV4 Series

EDS identity: vendor 367 Keyence Corporation, product code
4607, device type 43 Generic Device,
revision 1.1; EDS file revision
1.0 (01-01-2024).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Default Monitor Data And External Input | 100 / 2..1400 (Param10100) | 110 / 2..104 (Param10110) | 1 |
| Connection2 | 4X Detailed Monitor Data And External Input | 101 / 2..1400 (Param10101) | 110 / 2..104 (Param10110) | 1 |
| Connection3 | 8X Detailed Monitor Data And External Input | 102 / 2..1400 (Param10102) | 110 / 2..104 (Param10110) | 1 |
| Connection4 | Simple Monitor Data And External Input | 103 / 2..1400 (Param10103) | 110 / 2..104 (Param10110) | 1 |
| Connection5 | Default Monitor Data (Input Only) | 100 / 2..1400 (Param10100) | 254 / 0 | 1 |
| Connection6 | 4X Detailed Monitor Data (Input Only) | 101 / 2..1400 (Param10101) | 254 / 0 | 1 |
| Connection7 | 8X Detailed Monitor Data (Input Only) | 102 / 2..1400 (Param10102) | 254 / 0 | 1 |
| Connection8 | Simple Monitor Data (Input Only) | 103 / 2..1400 (Param10103) | 254 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Keyence IV4 Series, ODVA declaration of conformity (ODVA Marketplace) | `f677a76cf2658bce…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2703/12434_DOC_012624.pdf; retrieved 2026-11-23; not redistributed here |
| Keyence IV4 Series, EDS (ODVA Marketplace) | `49b07f53bc105f3c…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2703/Keyence_4607_0101.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
