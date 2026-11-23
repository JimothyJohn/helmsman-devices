> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation 1738-AENT

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
132, device type 12 Communications Adapter,
revision 6.13; EDS file revision
6.013 (03-25-2023).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Assembly Exclusive Owner | 101 / 8..509 (Param3) | 100 / 0..505 (Param2) | 102 |
| Connection2 | Assembly Listen-Only | 101 / 8..509 (Param3) | 191 / 0..505 (Param2) | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ArmorPOINT EtherNet/IP adapters EDS package 10401.33 (1738-AENT, 1738-AENTR) | `385800c349a5560f…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/540/10401.33_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.

## What is not here

No manual: rockwellautomation.com and literature.rockwellautomation.com answer the fetcher with 403 (2026-11-22), so there are no `[[points]]` and no `[wiring]`. The EDS is the ODVA-conformance copy linked from the ODVA marketplace page named in `collect/rockwell-automation.toml`. A unit must settle every value above.
