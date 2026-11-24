> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Keyence IV3 Series

EDS identity: vendor 367 Keyence Corporation, product code
4606, device type 43 Generic Device,
revision 1.1; EDS file revision
1.0 (12-20-2020).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Monitor Data And External Input | 100 / 2..1400 (Param10100) | 101 / 2..104 (Param10101) | 1 |
| Connection2 | Monitor Data (Input Only) | 100 / 2..1400 (Param10100) | 254 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Keyence IV3 Series, ODVA declaration of conformity (ODVA Marketplace) | `75377788cd081cc9…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2406/12099_DOC_072721.pdf; retrieved 2026-11-23; not redistributed here |
| Keyence IV3 Series, EDS (ODVA Marketplace) | `301244a528dc409b…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2406/Keyence_4606_0101.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
