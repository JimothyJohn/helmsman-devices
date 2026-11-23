> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation 1719-AENTR

EDS identity: vendor 1 Rockwell Automation, product code
315, device type 12 Communications Adapter,
revision 3.12; EDS file revision
1.9 (11-14-2024).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Adapter Status | 101 / 48 | 198 / 0 | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| 1719-AENTR EtherNet/IP adapter EDS package 11554.05 | `d0264b0694e66323…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1813/11554.05_EDS_Files.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.

## What is not here

No manual: rockwellautomation.com and literature.rockwellautomation.com answer the fetcher with 403 (2026-11-22), so there are no `[[points]]` and no `[wiring]`. The EDS is the ODVA-conformance copy linked from the ODVA marketplace page named in `collect/rockwell-automation.toml`. A unit must settle every value above.
