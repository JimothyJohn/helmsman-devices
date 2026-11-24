> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Emerson Numatics 580 Ethernet/IP

EDS identity: vendor 52 Numatics, Inc, product code
580, device type 12 Communications Adapter,
revision 2.1; EDS file revision
1.11 (04-11-2014).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 101 / 0..504 (Param2) | 150 / 0..504 (Param1) | 1 |
| Connection2 | Exclusive Owner - Status | 110 / 0..504 (Param2) | 193 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Numatics 580 EtherNet/IP EDS (ODVA marketplace, product 1165) | `29d313afae036aa9…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1165/NUMATICS-580.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
