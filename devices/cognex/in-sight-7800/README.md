> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Cognex In-Sight 7900-7500 Series

EDS identity: vendor 678 Cognex, product code
276, device type 100 In-Sight Vision System,
revision 11.1; EDS file revision
11.3 (11-11-2016).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Consume Data From/Produce Data To | 13 / 2..500 (Param2) | 22 / 2..496 (Param3) | 1 |
| Connection2 | Consume Data From | 13 / 2..500 (Param2) | 254 / 0 | 1 |
| Connection3 | Produce Data To | 254 / 0 | 22 / 2..496 (Param3) | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Cognex In-Sight 7800, 7802, 780xC, 7500, 7502, 7900, 7902, ODVA declaration of conformity (ODVA Marketplace) | `aebb0affa29a3681…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2053/11713_DOC_102418.pdf; retrieved 2026-11-23; not redistributed here |
| Cognex In-Sight 7800, 7802, 780xC, 7500, 7502, 7900, 7902, EDS (ODVA Marketplace) | `8e4757e83acacc28…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2053/11713.01-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
