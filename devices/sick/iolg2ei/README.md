> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# SICK IOLG2EI-03208R01

EDS identity: vendor 808 SICK AG, product code
20618, device type 43 Generic Device,
revision 3.4; EDS file revision
1.1 (28-08-2014).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Input Only | 100 / 392 | 128 / 0 | 102 |
| Connection2 | Exclusive Owner | 100 / 392 | 101 / 262 | 102 |
| Connection3 | Listen only | 100 / 392 | 129 / 0 | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| SICK IO-Link Master (IOLG2EI), ODVA declaration of conformity (ODVA Marketplace) | `5bb0a95703f69cd1…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1455/11372_DOC_031615.pdf; retrieved 2026-11-23; not redistributed here |
| SICK IO-Link Master (IOLG2EI), EDS (ODVA Marketplace) | `a14956e637a09957…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1455/IOLG2EI-03208R01.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
