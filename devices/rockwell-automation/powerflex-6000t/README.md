> **Draft from documents.** No unit has been checked. The identity and sizes are the
> EDS's, read by `scripts/eds-draft.py`; the 44 points were read by hand from the PowerFlex 750-Series Drives with TotalFORCE Control Built-in EtherNet/IP Adapter User Manual (750COM-UM009B-EN-P, April 2021), PDF pp. 55-57 (I/O image, Reference and Feedback, datalinks) and 121-123 (Logic Command and Status bits, drive products). Each point's `source` names the table and page. Nothing here was seen on a device.

# Rockwell Automation PowerFlex 6000T

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
10640, device type 143 Vendor Specific,
revision 11.1; EDS file revision
1.3 (05-20-2026).

## What this folder stands for

Stands for the PowerFlex 6000T medium-voltage drive (6000T...), from ODVA listing 2255 (DOC 12040). The EDS file is named `12040.08_EDS` with no extension on ODVA's server.Points: read from the PowerFlex 750-Series Drives with TotalFORCE Control Built-in EtherNet/IP Adapter User Manual (750COM-UM009B-EN-P, April 2021), PDF pp. 55-57 (I/O image, Reference and Feedback, datalinks) and 121-123 (Logic Command and Status bits, drive products). No unit has confirmed any of them. Sizes: the manual's Table 6 is Logic Command and Reference (8 bytes) plus up to 16 datalinks out (72), Logic Status and Feedback (8 bytes) plus up to 16 in (72), and says the interface also allocates a memory word for the generic module profile. The EDS lists that word as "Reserved", first in the input assembly, which makes the 12..76 input range; the points put Logic Status at byte 4 on that basis (inferred). The manual's catalog numbers are 20G, 20J and 6000T; its bus supply tables (PowerFlex 755TM) are left out.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1 / 12..76 (Param1) | 2 / 8..72 (Param2) | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 6000T MV AC drive: ODVA Declaration of Conformity | `66cbf2811650eb12…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2255/12040_DOC_082126.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 6000T MV AC drive: EDS (ODVA marketplace) | `42d2fad7e8521edb…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2255/12040.08_EDS; retrieved 2026-11-23; not redistributed here |
| PowerFlex 750-Series Drives with TotalFORCE Control Built-in EtherNet/IP Adapter User Manual, 750COM-UM009 (publication 750COM-UM009B-EN-P, April 2021) | `3df2899e8f852582…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/um/750com-um009_-en-p.pdf; fetched in a browser 2026-11-23 (the site answers a plain fetch with 403); not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
