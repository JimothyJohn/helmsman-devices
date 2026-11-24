> **Draft from documents.** No unit has been checked; the identity and assemblies are the
> EDS's (read by `scripts/eds-draft.py`) and the points are read from the 25-COMM-E2P adapter manual 520COM-UM003. Nothing
> here was seen on a device.

# Rockwell Automation PowerFlex 523 with 25-COMM-E2P

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
1822, device type 151 HS-DSI to EtherNet/IP,
revision 1.1; EDS file revision
1.1 (01-31-2013).

## What this folder stands for

Stands for the PowerFlex 523 (cat. 25A) with the 25-COMM-E2P dual-port EtherNet/IP adapter. The EDS drafted is the `25-COMM-E2P` member of ODVA's PowerFlex 525 package (`11171_EDS.zip`), a file for the adapter; ODVA has no separate listing for the 523. The 525 package is the one the 525 folder uses.Manual: 520COM-UM003A-EN-E (June 2013), fetched in a browser (Rockwell's literature site answers a plain fetch with 403) and read for the I/O image, the Logic Command and Logic Status bits, the reference/feedback scaling and the datalinks. Every `[[points]]` entry names the page and the table column it was read from; the manual numbers words by 0-based INT, and the byte.bit in `enip` is inferred from that (16-bit words, low byte first). No unit has confirmed any of it. The points use the manual's Generic Profile image, which is what is on the wire: the EDS's input assembly starts with a 4-byte `Reserved` member (Param100), the two pad words. Only the Velocity (C122 = 0) bit definitions are written out; the Position (C122 = 1) definitions are on the pages each point names. Input sizes in the manual agree with the EDS's Param1/Param2: single drive 8..16 bytes in and 4..12 out, Multi-drive mode up to five drives (4 pad bytes + 5 x 4 bytes = 24 in, 5 x 4 = 20 out). The manual states the multi-drive layout on p. 90; the points for drives 1 to 4 are written from it.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1 / 8..24 (Param1) | 2 / 4..20 (Param2) | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 525 (embedded EtherNet/IP): ODVA Declaration of Conformity | `8e85ae6dc580a772…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/580/11171_DOC_071713.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 525 (embedded EtherNet/IP): EDS (ODVA marketplace) | `388e7f6ed55bb038…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/580/11171_EDS.zip; retrieved 2026-11-23; not redistributed here |
| PowerFlex 25-COMM-E2P Dual-Port EtherNet/IP Adapter User Manual, 520COM-UM003A-EN-E | `ad7684cfe91859cb…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/um/520com-um003_-en-e.pdf; retrieved 2026-11-23, fetched in a browser; not redistributed here |


Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
