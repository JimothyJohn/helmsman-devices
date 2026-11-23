> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Festo CMMT-AS-EP

EDS identity: vendor 26 Festo, product code
65282, device type 43 Generic Device,
revision 1.1; EDS file revision
1.4 (03-16-2023).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | DriveProfile - Exclusive Owner | 101 / 24..24 (Param6) | 100 / 24..24 (Param5) | 102 |
| Connection2 | DriveProfile - Input Only | 101 / 24..24 (Param6) | 254 / 0 | 102 |
| Connection3 | DriveProfile - Listen Only | 101 / 24..24 (Param6) | 255 / 0 | 102 |
| Connection4 | Extended Process Data - Exclusive Owner | 111 / 32..32 (Param8) | 110 / 32..32 (Param7) | 102 |
| Connection5 | Extended Process Data - Listen Only | 111 / 32..32 (Param8) | 255 / 0 | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| CMMT-AS / CMMT-ST EtherNet/IP EDS (ODVA marketplace, product 2342) | `49a30233e0d5ee3c…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2342/11965.03-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
