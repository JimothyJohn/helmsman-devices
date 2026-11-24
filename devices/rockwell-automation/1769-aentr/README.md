> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation 1769-AENTR

EDS identity: vendor 1 Allen-Bradley, product code
298, device type 12 Communications Adapter,
revision 1.3; EDS file revision
1.3 (09-22-2021).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| none read | | | | |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| CompactLogix 1769-AENTR EDS package 11237.04 | `5d0a1249479d0e23…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1162/11237.04-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.

## What is not here

No manual: rockwellautomation.com and literature.rockwellautomation.com answer the fetcher with 403 (2026-11-22), so there are no `[[points]]` and no `[wiring]`. The EDS is the ODVA-conformance copy linked from the ODVA marketplace page named in `collect/rockwell-automation.toml`. A unit must settle every value above.
