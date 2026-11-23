> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Pepperl+Fuchs ICE2-8IOL-G65L-V1D

EDS identity: vendor 57 Pepperl+Fuchs, product code
374, device type 43 Generic Device,
revision 1.40; EDS file revision
1.03 (02-05-2021).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Read/Write All Ports | 101 / 2..499 (Param4) | 117 / 2..499 (Param6) | 1 |
| Connection2 | Read Only - All Ports | 101 / 2..499 (Param4) | 254 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Pepperl+Fuchs ICE2-8IOL-G65L-V1D, ICE2-8IOL-K45S-RJ45, ICE2-8IOL-K45P-RJ45, ICE2-8IOL1-G65L-V1D, ODVA declaration of conformity (ODVA Marketplace) | `1dd8d71989e4c108…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2379/11916_DOC_022221.pdf; retrieved 2026-11-23; not redistributed here |
| Pepperl+Fuchs ICE2-8IOL-G65L-V1D, ICE2-8IOL-K45S-RJ45, ICE2-8IOL-K45P-RJ45, ICE2-8IOL1-G65L-V1D, EDS (ODVA Marketplace) | `66168bbed45bf332…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2379/11916.02-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
