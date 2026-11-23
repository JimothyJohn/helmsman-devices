> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Parker Hannifin Corporation P2H Node 32DO EtherNet/IP

EDS identity: vendor 4 Parker Hannifin Corporation, product code
53296, device type 43 Generic Device,
revision 1.1; EDS file revision
1.00 (12-11-2020).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive owner | 100 / 8 | 150 / 5 | 0 |
| Connection2 | Listen only | 100 / 8 | 4 / 0 | 0 |
| Connection3 | Input only | 100 / 8 | 3 / 0 | 0 |
| Connection4 | Listen only extended | 100 / 8 | 7 / 0 | 0 |
| Connection5 | Input only extended | 100 / 8 | 6 / 0 | 0 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| P2H node EtherNet/IP EDS (ODVA marketplace, product 2381) | `9cd3f5dd84b67825…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2381/P2H_Ethernet_IP.EDS; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
