> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Parker Hannifin Corporation P2M Lite Node 24DO ETHERNET/IP

EDS identity: vendor 4 Parker Hannifin Corporation, product code
53505, device type 43 Generic Device,
revision 1.1; EDS file revision
1.00 (11-16-2020).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive owner | 100 / 7 | 150 / 4 | 0 |
| Connection2 | Listen only | 100 / 7 | 4 / 0 | 0 |
| Connection3 | Input only | 100 / 7 | 3 / 0 | 0 |
| Connection4 | Listen only extended | 100 / 7 | 7 / 0 | 0 |
| Connection5 | Input only extended | 100 / 7 | 6 / 0 | 0 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| P2M Lite node EtherNet/IP EDS (ODVA marketplace, product 2292) | `1edc8c8bc60c5b2c…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2292/Parker_Lite.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
