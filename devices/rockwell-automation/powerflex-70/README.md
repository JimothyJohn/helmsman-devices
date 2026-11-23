> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation PowerFlex 70 (EtherNet/IP adapter)

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
48, device type 123 DPI to EtherNet/IP,
revision 2.9; EDS file revision
1.12 (10-20-2008).

## What this folder stands for

Stands for the PowerFlex 70 (cat. 20A) on an EtherNet/IP adapter. The EDS drafted is the `PowerFlex 70` member (`0001007B00300200.eds`) of ODVA's family package 1639; the package also holds a PowerFlex 755 file, not drafted. Which adapter (20-COMM-E or 20-COMM-ER) the file belongs to is not stated in it.Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1 / 4..24 (Param2) | 2 / 0..20 (Param1) | 6 |
| Connection2 | Discrete Input Only | 1 / 4..24 (Param2) | 2 / 0 | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 70 family (ODVA listing 1639): ODVA Declaration of Conformity | `b5629f7a3d40358e…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1639/10702_DOC_110308.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 70 family (ODVA listing 1639): EDS (ODVA marketplace) | `c76a77ae3a5b2759…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1639/10702-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
