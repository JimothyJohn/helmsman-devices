> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation PowerFlex 755 (embedded EtherNet/IP)

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
2192, device type 143 PowerFlex 750-Series via Embedded EtherNet/IP,
revision 16.1; EDS file revision
1.1 (07-25-2016).

## What this folder stands for

Stands for the PowerFlex 755 (cat. 20G) with its embedded EtherNet/IP port, device type 143, member `0001008F08901000.eds` of ODVA's `10875.04.zip` (PF755 V16). The package holds one EDS per host/adapter variant and a 755HiP set; the others were not drafted.Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1 / 12..76 (Param2) | 2 / 8..72 (Param1) | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 755, 755HiP: ODVA Declaration of Conformity | `58bf5c53762a6e4e…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1644/10875_DOC_042225.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 755, 755HiP: EDS (ODVA marketplace) | `58ffcda61a8f3c1f…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1644/10875.04.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
