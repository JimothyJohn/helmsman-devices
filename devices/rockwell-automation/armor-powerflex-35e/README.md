> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. The manual was read and gives no
> byte layout for the assemblies, so there are no `[[points]]` (see below).

# Rockwell Automation Armor PowerFlex 35E

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
3, device type 170 PowerFlex Variable Frequency Drive,
revision 2.1; EDS file revision
1.2 (07-13-2022).

## What this folder stands for

A substitute: Armor PowerFlex 35E, from ODVA listing 2432 (DOC 12191), one EDS in `12191.10.zip`.Manual: Armor PowerFlex 350 AC Drives User Manual 35-UM001J-EN-P (March 2026), fetched in a browser and read; it covers the 35E. It has no `[[points]]` here, on purpose: the manual gives no logic command, logic status, command velocity or feedback bit or byte layout for the EDS's assemblies 769 (28 bytes out) and 1025 (76 bytes in). It configures the drive through the Studio 5000 add-on profile and sends the reader to the CIP Objects and Attributes Reference Data, publication 35-RD001 (PDF p. 155), which is a separate document (a spreadsheet) and was not collected. Its datalinks (Table 59, PDF pp. 161-162, 8 boolean and 4 real each way, drive firmware 2.000 or later) are named by what they carry, not placed in the assembly. The sizes in the EDS are neither confirmed nor contradicted. No unit has been checked.

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
| Armor PowerFlex 350 AC Drives User Manual, 35-UM001J-EN-P | `b04946e12a4da0ab…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/um/35-um001_-en-p.pdf; retrieved 2026-11-23, fetched in a browser; not redistributed here |


Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
