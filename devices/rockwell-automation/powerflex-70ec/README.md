> **Draft from documents.** No unit has been checked. The identity and sizes are the
> EDS's, read by `scripts/eds-draft.py`; the 26 points were read by hand from the 20-COMM-E EtherNet/IP Adapter User Manual (20COMM-UM010H-EN-P), PDF pp. 92-99, 113, 227 and 271-272, the same pages as the PowerFlex 70 folder. Each point's `source` names the table and page. Nothing here was seen on a device.

# Rockwell Automation PowerFlex 70EC

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
50, device type 152 DPI to DLR EtherNet/IP,
revision 5.1; EDS file revision
1.1 (03-25-2013).

## What this folder stands for

A substitute candidate: the PowerFlex 70EC (cat. 20A, Enhanced Control), from ODVA listing 1659 (DOC 11084).Points: read from the 20-COMM-E EtherNet/IP Adapter User Manual (20COMM-UM010H-EN-P), PDF pp. 92-99, 113, 227 and 271-272, the same pages as the PowerFlex 70 folder. No unit has confirmed any of them. The manual treats the PowerFlex 70 with standard or enhanced control alike (Table 5.A, Appendix D), so the 70 points apply as read. But the manual covers the 20-COMM-E, whose Identity Object reports device type 123, and this entry's EDS is device type 152, "DPI to DLR EtherNet/IP": a different adapter. Every point here is marked inferred for that reason, and a `[[questions]]` entry asks. Same size check as the PowerFlex 70: 20 bytes out and 24 in at most, per the manual's table.

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
| PowerFlex 20-COMM-E EtherNet/IP Adapter User Manual, 20COMM-UM010 (publication 20COMM-UM010H-EN-P) | `e707376542b3a411…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/um/20comm-um010_-en-p.pdf; fetched in a browser 2026-11-23 (the site answers a plain fetch with 403); not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
