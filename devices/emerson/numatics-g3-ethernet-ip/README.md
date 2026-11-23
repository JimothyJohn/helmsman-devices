> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Numatics, Inc Numatics G3 EtherNet/IP

EDS identity: vendor 52 Numatics, Inc, product code
101, device type 12 Communications Adapter,
revision 2.1; EDS file revision
1.08 (02-15-2013).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 101 / 0..504 (Param2) | 150 / 0..504 (Param1) | 1 |
| Connection2 | Status Only | 110 / 0..504 (Param2) | 193 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Numatics G3 EtherNet/IP node EDS (ODVA marketplace, product 516) | `f85af8493cc6105a…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/516/G3EP0102s-2013-03-01.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
