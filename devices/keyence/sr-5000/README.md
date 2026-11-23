> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Keyence SR-5000 Series

EDS identity: vendor 367 Keyence Corporation, product code
1008, device type 43 Generic Device,
revision 1.1; EDS file revision
1.1 (08-02-2019).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Class1 | 100 / 40..1400 (Param1) | 101 / 4..1400 (Param2) | 1 |
| Connection2 | Class1 (Input-Only) | 100 / 40..1400 (Param1) | 254 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Keyence SR-5000 Series, ODVA declaration of conformity (ODVA Marketplace) | `e9ed9e83dd3c23f0…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2207/11937_DOC_030420.pdf; retrieved 2026-11-23; not redistributed here |
| Keyence SR-5000 Series, EDS (ODVA Marketplace) | `82d9945e1b3f7896…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2207/11937.01-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
