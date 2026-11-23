> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation PowerFlex 755TS

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
85, device type 37 CIP Motion Drive,
revision 14.2; EDS file revision
1.1 (12-21-2023).

## What this folder stands for

Stands for the PowerFlex 755TS (cat. 20G1D/20G1E), a CIP Motion drive. The EDS drafted is the one in ODVA's `12346.06_EDS.zip` (DOC 12346). ODVA also has a second 755TS listing (product 2443) that was not drafted.Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | CIP Motion Safety Drive Exclusive Owner | 2 / 500 | 81 / 500 |  |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 755TS: ODVA Declaration of Conformity | `0721e8e87635607b…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2690/12346_DOC_031726.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 755TS: EDS (ODVA marketplace) | `29d448ab91ceea18…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2690/12346.06_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
