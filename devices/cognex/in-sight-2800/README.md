> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Cognex In-Sight 2800 Series

EDS identity: vendor 678 Cognex Corporation, product code
3585, device type 782 In-Sight Vision System,
revision 1.1; EDS file revision
1.1 (03-19-2024).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Consume Data From/Produce Data To | 13 / 2..500 (Param2) | 22 / 2..496 (Param3) | 1 |
| Connection2 | Consume Data From | 13 / 2..500 (Param2) | 254 / 0 | 1 |
| Connection3 | Produce Data To | 254 / 0 | 22 / 2..496 (Param3) | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Cognex In-Sight 2800 (IS2802M, IS2802C, IS2805X, IS2801X, IS2800M), ODVA declaration of conformity (ODVA Marketplace) | `e5ea3420499b0ebf…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2468/12213_DOC_071524.pdf; retrieved 2026-11-23; not redistributed here |
| Cognex In-Sight 2800 (IS2802M, IS2802C, IS2805X, IS2801X, IS2800M), EDS (ODVA Marketplace) | `2d70feeaaf8d0432…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2468/12213.03_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
