> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation 1734-AENT

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
108, device type 12 Communications Adapter,
revision 7.15; EDS file revision
7.015 (07-29-2024).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Assembly Exclusive Owner | 101 / 8..509 (Param3) | 100 / 0..505 (Param2) | 102 |
| Connection2 | Assembly Listen-Only | 101 / 8..509 (Param3) | 191 / 0..505 (Param2) | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| POINT I/O 1734-AENT/C and 1734-AENTR/C EDS package 11808.09 | `f31fab6a86bfd8f0…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2050/11808.09-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.

## What is not here

No manual: rockwellautomation.com and literature.rockwellautomation.com answer the fetcher with 403 (2026-11-22), so there are no `[[points]]` and no `[wiring]`. The EDS is the ODVA-conformance copy linked from the ODVA marketplace page named in `collect/rockwell-automation.toml`. A unit must settle every value above.
