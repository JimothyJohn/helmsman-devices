> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation Armor PowerFlex 35E

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
3, device type 170 PowerFlex Variable Frequency Drive,
revision 2.1; EDS file revision
1.2 (07-13-2022).

## What this folder stands for

A substitute: Armor PowerFlex 35E, from ODVA listing 2432 (DOC 12191), one EDS in `12191.10.zip`.Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1025 / 76 | 769 / 28 | 1 |
| Connection2 | Input Only | 5121 / 76 | 238 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Armor PowerFlex 35E: ODVA Declaration of Conformity | `765503f461db5438…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2432/12191_DOC_090125.pdf; retrieved 2026-11-23; not redistributed here |
| Armor PowerFlex 35E: EDS (ODVA marketplace) | `2af95303f1d98eec…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2432/12191.10.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
