> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation PowerFlex 70EC

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
50, device type 152 DPI to DLR EtherNet/IP,
revision 5.1; EDS file revision
1.1 (03-25-2013).

## What this folder stands for

A substitute candidate: the PowerFlex 70EC (cat. 20A, Enhanced Control), from ODVA listing 1659 (DOC 11084).Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1 / 4..24 (Param2) | 2 / 0..20 (Param1) | 6 |
| Connection2 | Discrete Input Only | 1 / 4..24 (Param2) | 191 / 0 | 6 |
| Connection3 | Discrete Listen Only | 1 / 4..24 (Param2) | 192 / 0 | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 70EC: ODVA Declaration of Conformity | `30fbc80109947ec2…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1659/11084_DOC_071713.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 70EC: EDS (ODVA marketplace) | `a3f828cbce6c5bc9…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1659/0001009800320500.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
