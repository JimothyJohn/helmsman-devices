> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Norgren Manufacturing Co., Ltd. VR1X-EP

EDS identity: vendor 1609 Norgren Manufacturing Co., Ltd., product code
1, device type 43 Generic Device,
revision 1.1; EDS file revision
1.0 (25-10-2023).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 100 /  | 150 /  | 151 |
| Connection2 | Input Only | 100 /  | 152 / 0 | 0 |
| Connection3 | Listen Only | 100 /  | 153 / 0 | 0 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| VR1X-EP EtherNet/IP EDS (ODVA marketplace, product 2241) | `87df5947b8369b60…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2241/NORGREN-VR1X-EP-24-V1.2.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
