> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# TURCK TBEN-S2-4IOL

EDS identity: vendor 48 TURCK, product code
14024, device type 12 Communications Adapter,
revision 2.7; EDS file revision
2.8 (03-03-2017).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 103 /  | 104 /  | 106 |
| Connection2 | Input Only Connection | 103 /  | 254 / 0 | 1 |
| Connection3 | Listen Only Connection | 103 /  | 255 / 0 | 1 |
| Connection4 | Exclusive Owner - Omron | 101 / 0..208 (Param6) | 102 / 0..132 (Param7) | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| TBEN-S EDS files and catalog files (family package) | `69f84dc3eee7ea3f…` | https://www.turck.us/attachment/TBEN-S_ETHERNETIP.zip; retrieved 2026-11-23; not redistributed here |
| TBEN-S GSDML files (family package) | `6db8486032894fee…` | https://www.turck.us/attachment/TBEN-S_PROFINET.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
