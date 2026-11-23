> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Balluff BNI EIP-508-105-Z015

EDS identity: vendor 43 BALLUFF GmbH, product code
20618, device type 43 Generic Device,
revision 3.1; EDS file revision
1.1 (01-15-2013).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Input Only | 100 / 392 | 128 / 0 | 102 |
| Connection2 | Exclusive Owner | 100 / 392 | 101 / 262 | 102 |
| Connection3 | Listen only | 100 / 392 | 129 / 0 | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Balluff EtherNet/IP EDS files (ODVA marketplace 448): BNI EIP-302-105-Z015, BNI EIP-508-105-Z015 | `4056224315d1afb5…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/448/10943.03-EDSFiles.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
