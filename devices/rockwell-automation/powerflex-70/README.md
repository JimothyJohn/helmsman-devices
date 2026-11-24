> **Draft from documents.** No unit has been checked. The identity and sizes are the
> EDS's, read by `scripts/eds-draft.py`; the 26 points were read by hand from the 20-COMM-E EtherNet/IP Adapter User Manual (20COMM-UM010H-EN-P), PDF pp. 92-99 (I/O image, Table 5.A, scaling, datalinks), 113 (datalink parameter numbers), 227 (adapter parameter 23), 271-272 (Logic Command and Status bits). Each point's `source` names the table and page. Nothing here was seen on a device.

# Rockwell Automation PowerFlex 70 (EtherNet/IP adapter)

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
48, device type 123 DPI to EtherNet/IP,
revision 2.9; EDS file revision
1.12 (10-20-2008).

## What this folder stands for

Stands for the PowerFlex 70 (cat. 20A) on an EtherNet/IP adapter. The EDS drafted is the `PowerFlex 70` member (`0001007B00300200.eds`) of ODVA's family package 1639; the package also holds a PowerFlex 755 file, not drafted. Which adapter (20-COMM-E or 20-COMM-ER) the file belongs to is not stated in it.Points: read from the 20-COMM-E EtherNet/IP Adapter User Manual (20COMM-UM010H-EN-P), PDF pp. 92-99 (I/O image, Table 5.A, scaling, datalinks), 113 (datalink parameter numbers), 227 (adapter parameter 23), 271-272 (Logic Command and Status bits). No unit has confirmed any of them. Sizes: the manual's Table 5.A gives 10 words out (20 bytes) and 12 words in (24 bytes) with all four datalink sets on, which is the EDS's maximum (0..20 out, 4..24 in). The default of 4 out is the Logic Command and Reference; the default of 8 in is two pad words, Logic Status and Feedback. The input image starts with two pad words (4 bytes) that the manual's ControlLogix table shows and the EDS size range implies; the points start after them. The EDS minimums (0 out, 4 in) are not stated in the manual.

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
| PowerFlex 20-COMM-E EtherNet/IP Adapter User Manual, 20COMM-UM010 (publication 20COMM-UM010H-EN-P) | `e707376542b3a411…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/um/20comm-um010_-en-p.pdf; fetched in a browser 2026-11-23 (the site answers a plain fetch with 403); not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
