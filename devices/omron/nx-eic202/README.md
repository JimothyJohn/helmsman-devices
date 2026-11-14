> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Omron NX-EIC202

EDS identity: vendor 47 OMRON Corporation, product code
1660, device type 12 Communications Adapter,
revision 1.3; EDS file revision
1.2 (12-26-2016).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Input / Output | 100 /  | 148 /  | 199 |
| Connection2 | Input Only | 100 /  | 197 / 0 | 199 |
| Connection3 | Listen Only | 100 /  | 198 / 0 | 199 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| NX-EIC202 EDS (ODVA marketplace, product 1170) | `c38718b4d004a93c…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1170/NX-EIC202.eds; retrieved 2026-11-14; not redistributed here |
| NX-series EtherNet/IP Coupler Unit User's Manual W536-E1-01 (Omron knowledge base attachment) | `7534c445d65d1cbb…` | https://automation-knowledge-base.omron.eu/helpdesk/attachments/103252089414; retrieved 2026-11-14; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
