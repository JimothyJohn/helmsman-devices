> **Draft from documents.** No unit has been checked; the identity and assemblies are the
> EDS's (read by `scripts/eds-draft.py`) and the points are read from the embedded EtherNet/IP adapter manual 520COM-UM001. Nothing
> here was seen on a device.

# Rockwell Automation PowerFlex 525 (embedded EtherNet/IP)

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
9, device type 151 HS-DSI to EtherNet/IP,
revision 1.3; EDS file revision
1.1 (01-31-2013).

## What this folder stands for

Stands for the PowerFlex 525 (cat. 25B) with its embedded EtherNet/IP port. The EDS drafted is `0001009700090100.eds`, one of two members of ODVA's `11171_EDS.zip`; the other (25-COMM-E2P) is the 523 folder. Ratings are not separate EDS files here, so this stands for the whole 25B range.Manual: 520COM-UM001B-EN-E (March 2013), fetched in a browser (Rockwell's literature site answers a plain fetch with 403) and read for the I/O image, the Logic Command and Logic Status bits, the reference/feedback scaling and the datalinks. Every `[[points]]` entry names the page and the table column it was read from; the manual numbers words by 0-based INT, and the byte.bit in `enip` is inferred from that (16-bit words, low byte first). No unit has confirmed any of it. The points use the manual's Generic Profile image, which is what is on the wire: the EDS's input assembly starts with a 4-byte `Reserved` member (Param100), the two pad words. Only the Velocity (C122 = 0) bit definitions are written out; the Position (C122 = 1) definitions are on the pages each point names. Input sizes in the manual (single drive: 4 pad bytes + status, feedback, up to four datalinks = 8..16 bytes in, 4..12 out) agree with the EDS's Param1/Param2.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1 / 8..16 (Param1) | 2 / 4..12 (Param2) | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 525 (embedded EtherNet/IP): ODVA Declaration of Conformity | `8e85ae6dc580a772…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/580/11171_DOC_071713.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 525 (embedded EtherNet/IP): EDS (ODVA marketplace) | `388e7f6ed55bb038…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/580/11171_EDS.zip; retrieved 2026-11-23; not redistributed here |
| PowerFlex 525 Embedded EtherNet/IP Adapter User Manual, 520COM-UM001B-EN-E | `2e1250e2629945de…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/um/520com-um001_-en-e.pdf; retrieved 2026-11-23, fetched in a browser; not redistributed here |


Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
