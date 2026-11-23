> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation 5094-AEN2TR

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
322, device type 12 Communications Adapter,
revision 6.12; EDS file revision
6.4 (08-27-2025).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Ping |  / 0 |  / 0 |  |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| FLEX 5000 EtherNet/IP adapters EDS package 11693.11 (5094-AENTR, 5094-AEN2TR and variants) | `a0e6e823abf84140…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1968/11693.11_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.

## What is not here

No manual: rockwellautomation.com and literature.rockwellautomation.com answer the fetcher with 403 (2026-11-22), so there are no `[[points]]` and no `[wiring]`. The EDS is the ODVA-conformance copy linked from the ODVA marketplace page named in `collect/rockwell-automation.toml`. A unit must settle every value above.
