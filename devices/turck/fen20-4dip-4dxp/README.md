> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Turck FEN20-4DIP-4DXP

EDS identity: vendor 48 Turck, product code
31090, device type 12 Communications Adapter,
revision 2.7; EDS file revision
2.7 (10-11-2016).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 103 /  | 104 /  | 106 |
| Connection2 | Input Only Connection | 103 /  | 254 / 0 | 1 |
| Connection3 | Listen Only Connection | 103 /  | 255 / 0 | 1 |
| Connection4 | Exclusive Owner - Omron | 101 / 0..8 (Param6) | 102 / 0..4 (Param7) | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| FEN20 EDS files and catalog files (family package) | `4eff4b49616d269e…` | https://www.turck.us/attachment/FEN20_ETHERNETIP.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
