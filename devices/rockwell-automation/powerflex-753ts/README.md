> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation PowerFlex 753TS

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
7056, device type 143 PowerFlex TotalFORCE via Embedded EtherNet/IP,
revision 13.1; EDS file revision
1.1 (04-11-2023).

## What this folder stands for

A substitute candidate: the PowerFlex 753TS (cat. 20F1D/20F1E), from ODVA listing 2691 (DOC 12345).Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1 / 12..76 (Param1) | 2 / 8..72 (Param2) | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 753TS: ODVA Declaration of Conformity | `24c1238364e31545…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2691/12345_DOC_022724.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 753TS: EDS (ODVA marketplace) | `ffa875f571bd434a…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2691/EDS_753TS.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
