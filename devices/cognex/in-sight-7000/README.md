> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Cognex In-Sight 7000 Series

EDS identity: vendor 678 Cognex, product code
265, device type 100 In-Sight 7000 Series,
revision 10.1; EDS file revision
10.1 (04-10-2014).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Consume Data From | 12 / 2..500 (Param2) | 254 / 0 | 1 |
| Connection2 | Produce Data To | 254 / 0 | 21 / 2..496 (Param3) | 1 |
| Connection3 | Consume Data From/Produce Data To | 12 / 2..500 (Param2) | 21 / 2..496 (Param3) | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Cognex In-Sight 7000 Series, ODVA declaration of conformity (ODVA Marketplace) | `287c288c42b51e09…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1669/11273_DOC_060414.pdf; retrieved 2026-11-23; not redistributed here |
| Cognex In-Sight 7000 Series, EDS (ODVA Marketplace) | `ef13ffda43b6dbc6…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1669/02A6006401090A00.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
