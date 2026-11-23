> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# TURCK TBEN-L5-8IOL

EDS identity: vendor 48 TURCK, product code
14017, device type 12 Communications Adapter,
revision 2.7; EDS file revision
2.7 (10-24-2016).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 103 /  | 104 /  | 106 |
| Connection2 | Input Only Connection | 103 /  | 254 / 0 | 1 |
| Connection3 | Listen Only Connection | 103 /  | 255 / 0 | 1 |
| Connection4 | Exclusive Owner - Omron | 101 / 0..346 (Param6) | 102 / 0..262 (Param7) | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| TBEN-L EDS files and catalog files (family package) | `91c35fe7408fc5f7…` | https://www.turck.us/attachment/TBEN-L_ETHERNETIP.zip; retrieved 2026-11-23; not redistributed here |
| TBEN-Lx-8IOL Instructions for Use | `5980862a24761391…` | https://www.turck.us/attachment/d301407.pdf; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
