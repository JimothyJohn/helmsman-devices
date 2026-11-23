> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# SICK AG SIG350

EDS identity: vendor 808 SICK AG, product code
16642, device type 12 Communications Adapter,
revision 1.1; EDS file revision
1.1 (07-28-2021).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner - 32 bytes per IO-Link Port | 101 / 4..276 (Param151) | 100 / 4..276 (Param150) | 102 |
| Connection2 | Exclusive Owner - 32 bytes per IO-Link Port without Config | 101 / 4..276 (Param151) | 100 / 4..276 (Param150) | 1 |
| Connection3 | Listen only - 32 bytes per IO-Link Port | 101 / 4..276 (Param151) | 192 / 0 | 1 |
| Connection4 | Input Only - 32 bytes per IO-Link Port | 101 / 4..276 (Param151) | 193 / 0 | 102 |
| Connection5 | Exclusive Owner - 16 bytes per IO-Link Port | 105 / 4..148 (Param153) | 104 / 4..148 (Param152) | 102 |
| Connection6 | Exclusive Owner - 16 bytes per IO-Link Port without Config | 105 / 4..148 (Param153) | 104 / 4..148 (Param152) | 1 |
| Connection7 | Listen Only - 16 bytes per IO-Link Port | 105 / 4..148 (Param153) | 192 / 0 | 1 |
| Connection8 | Input Only - 16 bytes per IO-Link Port | 105 / 4..148 (Param153) | 193 / 0 | 102 |
| Connection9 | Exclusive Owner - 4 bytes per IO-Link Port | 109 / 4..52 (Param155) | 108 / 4..52 (Param154) | 102 |
| Connection10 | Exclusive Owner - 4 bytes per IO-Link Port without Config | 109 / 4..52 (Param155) | 108 / 4..52 (Param154) | 1 |
| Connection11 | Listen Only - 4 bytes per IO-Link Port | 109 / 4..52 (Param155) | 192 / 0 | 1 |
| Connection12 | Input Only - 4 bytes per IO-Link Port | 109 / 4..52 (Param155) | 193 / 0 | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| SICK SIG350-0005AP100, ODVA declaration of conformity (ODVA Marketplace) | `aa567cb43f3dd426…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2509/12265_DOC_062422.pdf; retrieved 2026-11-23; not redistributed here |
| SICK SIG350-0005AP100, EDS (ODVA Marketplace) | `7eda2e3e90f451cf…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2509/12265.01-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
