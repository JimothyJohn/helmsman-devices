> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation 1794-AENTR

EDS identity: vendor 1 Allen-Bradley, product code
261, device type 12 Communications Adapter,
revision 2.12; EDS file revision
2.12 (08-04-2022).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| none read | | | | |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| FLEX I/O 1794-AENTR EDS package 10989.14 | `4a95df7cee1fec8d…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/552/10989.14.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.

## What is not here

No manual: rockwellautomation.com and literature.rockwellautomation.com answer the fetcher with 403 (2026-11-22), so there are no `[[points]]` and no `[wiring]`. The EDS is the ODVA-conformance copy linked from the ODVA marketplace page named in `collect/rockwell-automation.toml`. A unit must settle every value above.
