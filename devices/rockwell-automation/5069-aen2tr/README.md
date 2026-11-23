> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation 5069-AEN2TR

EDS identity: vendor 1 Allen-Bradley, product code
252, device type 12 Communications Adapter,
revision 3.1; EDS file revision
1.7 (08-27-2015).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Ping |  / 0 |  / 0 |  |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Compact 5000 5069-AEN2TR EDS (uploaded from firmware 3.011.44) | `b40ea940a20752f6…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1185/0001000C00FC0300_as_uploaded_from_3.011.44.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.

## What is not here

No manual: rockwellautomation.com and literature.rockwellautomation.com answer the fetcher with 403 (2026-11-22), so there are no `[[points]]` and no `[wiring]`. The EDS is the ODVA-conformance copy linked from the ODVA marketplace page named in `collect/rockwell-automation.toml`. A unit must settle every value above.
