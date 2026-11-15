> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# WAGO 750-363

EDS identity: vendor 40 WAGO Kontakttechnik GmbH & Co. KG, product code
363, device type 12 Communications Adapter,
revision 1.4; EDS file revision
1.5 (04-26-2021).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | class1 - exclusive owner | 104 /  | 101 /  | 1 |
| Connection2 | class1 - input only | 104 /  | 198 / 0 | 1 |
| Connection3 | class1 - listen only | 104 /  | 199 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| WAGO EDS for EtherNet/IP: 750-363, 750-823, 750-893 (ODVA marketplace, product 2172) | `24eabd21e0728694…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2172/11921.02-EDS.zip; retrieved 2026-11-14; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
