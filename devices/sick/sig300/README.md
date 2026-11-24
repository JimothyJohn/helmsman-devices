> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# SICK SIG300

EDS identity: vendor 808 SICK AG, product code
16641, device type 12 Communications Adapter,
revision 1.1; EDS file revision
1.3 (04-24-2024).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 101 / 4..404 (Param151) | 100 / 4..404 (Param150) | 153 |
| Connection2 | Input Only | 101 / 4..404 (Param151) | 254 / 0 | 1 |
| Connection3 | Listen Only | 101 / 4..404 (Param151) | 255 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| SICK SIG300, ODVA declaration of conformity (ODVA Marketplace) | `fd899e883f552348…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2796/12525_DOC_091124.pdf; retrieved 2026-11-23; not redistributed here |
| SICK SIG300, EDS (ODVA Marketplace) | `9631245f5d0981b5…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2796/SICK_SIG300_V1.3.1.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
