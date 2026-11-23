> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation PowerFlex 753 with 20-750-ENETR

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
1168, device type 140 PowerFlex 750-Series via ControlNet,
revision 1.1; EDS file revision
1.1 (02-12-2009).

## What this folder stands for

Stands for the PowerFlex 753 (cat. 20F) with the 20-750-ENETR dual-port option module. The EDS drafted is the `PowerFlex 753` member (`0001008C04900100.eds`) of ODVA's family package 854; the 20-750-ENETR module's own EDS (ODVA product 581) is listed under sources, not drafted. The 753's other variants in the package (CIP Motion, CIP Motion with CIP Safety) were not drafted.Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 1 / 4..76 (Param2) | 2 / 8..72 (Param1) | 6 |
| Connection2 | Input Only | 1 / 4..76 (Param2) | 4 / 0 | 6 |
| Connection3 | Redundant Owner | 1 / 4..76 (Param2) | 5 / 8..72 (Param1) | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 750-Series dual-port EtherNet/IP option module (20-750-ENETR): ODVA Declaration of Conformity | `b5307d5e9b429751…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/581/11061_DOC_061812.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 753 and 755 family (ODVA listing 854): ODVA Declaration of Conformity | `98c533cad64c8980…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/854/10788_DOC_082409.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 750-Series dual-port EtherNet/IP option module (20-750-ENETR): EDS (ODVA marketplace) | `fe78ee688ac471b6…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/581/11061-EDS.zip; retrieved 2026-11-23; not redistributed here |
| PowerFlex 753 and 755 family (ODVA listing 854): EDS (ODVA marketplace) | `1aeef508465e71ac…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/854/10788_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
