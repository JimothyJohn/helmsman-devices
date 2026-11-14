> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and wiring in device.toml are read
> from the user's guide, with the page for each.

# Balluff BNI EIP-302-105-Z015

EDS identity: vendor 43 BALLUFF GmbH, product code
12330, device type 43 Generic Device,
revision 2.6; EDS file revision
1.1 (10-25-2011).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Input Only | 100 / 8 | 128 / 0 | 1 |
| Connection2 | Exclusive Owner | 100 / 8 | 101 / 6 | 1 |
| Connection3 | Listen only | 100 / 8 | 129 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Balluff EtherNet/IP EDS files (ODVA marketplace 448): BNI EIP-302-105-Z015, BNI EIP-508-105-Z015 | `4056224315d1afb5…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/448/10943.03-EDSFiles.zip; retrieved 2026-11-14; not redistributed here |
| BNI EIP-104/202/302-105-Z015 Bedienungsanleitung (German user's guide) | `9824630941285c98…` | https://assets.balluff.com/WebBinary1/MAN_BNI_EIP_XXX_105_Z015_D_B17_DOK_886816_04_000.pdf; retrieved 2026-11-14; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
