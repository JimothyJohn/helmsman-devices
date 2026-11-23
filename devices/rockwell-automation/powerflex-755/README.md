> **Draft from documents.** No unit has been checked. The identity and sizes are the
> EDS's, read by `scripts/eds-draft.py`; the 44 points were read by hand from the PowerFlex 755 Drive Embedded EtherNet/IP Adapter User Manual (750COM-UM001G-EN-P, August 2018), PDF pp. 94-95 (sizes), 99-103 (I/O image, Reference and Feedback, datalinks) and 195-198 (Logic Command and Status bits). Each point's `source` names the table and page. Nothing here was seen on a device.

# Rockwell Automation PowerFlex 755 (embedded EtherNet/IP)

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
2192, device type 143 PowerFlex 750-Series via Embedded EtherNet/IP,
revision 16.1; EDS file revision
1.1 (07-25-2016).

## What this folder stands for

Stands for the PowerFlex 755 (cat. 20G) with its embedded EtherNet/IP port, device type 143, member `0001008F08901000.eds` of ODVA's `10875.04.zip` (PF755 V16). The package holds one EDS per host/adapter variant and a 755HiP set; the others were not drafted.Points: read from the PowerFlex 755 Drive Embedded EtherNet/IP Adapter User Manual (750COM-UM001G-EN-P, August 2018), PDF pp. 94-95 (sizes), 99-103 (I/O image, Reference and Feedback, datalinks) and 195-198 (Logic Command and Status bits). No unit has confirmed any of them. Sizes: the manual's Generic Profile image is a pad word, Logic Status and Feedback (3 words, 12 bytes in at least) and Logic Command and Reference (2 words, 8 bytes out at least), plus one 32-bit word per datalink, 16 each way: 76 bytes in and 72 out, the EDS's ranges exactly, in 4-byte steps.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1 / 12..76 (Param2) | 2 / 8..72 (Param1) | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 755, 755HiP: ODVA Declaration of Conformity | `58bf5c53762a6e4e…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1644/10875_DOC_042225.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 755, 755HiP: EDS (ODVA marketplace) | `58ffcda61a8f3c1f…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1644/10875.04.zip; retrieved 2026-11-23; not redistributed here |
| PowerFlex 755 Drive Embedded EtherNet/IP Adapter User Manual, 750COM-UM001 (publication 750COM-UM001G-EN-P, August 2018) | `1d3e5cf16d24abfd…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/um/750com-um001_-en-p.pdf; fetched in a browser 2026-11-23 (the site answers a plain fetch with 403); not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
