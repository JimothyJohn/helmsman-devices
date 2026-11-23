> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation 1732E-16CFGM12R

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
357, device type 7 General Purpose Discrete I/O,
revision 3.12; EDS file revision
3.12 (07-17-2022).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Logix - Exclusive Owner | 105 /  | 35 /  | 102 |
| Connection2 | Open - Exclusive Owner | 5 /  | 35 /  | 102 |
| Connection3 | Logix - Listen Only | 105 /  | 191 / 0 | 102 |
| Connection4 | Open - Listen Only | 5 /  | 191 / 0 | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ArmorBlock 1732E 16-point M12 EDS package 11894.05 | `6d733a423323020a…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2159/11894.05-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.

## What is not here

No manual: rockwellautomation.com and literature.rockwellautomation.com answer the fetcher with 403 (2026-11-22), so there are no `[[points]]` and no `[wiring]`. The EDS is the ODVA-conformance copy linked from the ODVA marketplace page named in `collect/rockwell-automation.toml`. A unit must settle every value above.
