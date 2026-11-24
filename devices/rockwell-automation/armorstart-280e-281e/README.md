> **Draft from documents.** No unit has been checked; every value here is the
> EDS's or the manual's, and no unit has confirmed either.

# Rockwell Automation ArmorStart 280E/281E (EtherNet/IP)

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
145, device type 22 Motor Starter,
revision 2.3; EDS file revision
2.1 (02-19-2016).

## What this folder stands for

Stands for the ArmorStart 280E/281E (and 284E) distributed motor controllers. ODVA's `10910.04-EDS.zip` holds one EDS per rating and variant (29); the drafted one is the 280E 0.5-2.5A 24 VDC, `0001001600910200.eds`, whose product code and assembly sizes may differ for the others. The others were not drafted.Manual: 280E-UM001C-EN-P (September 2015), fetched in a browser because the site answers a plain fetch with 403. The `[[points]]` were read from its Appendix B (PDF pp. 303 and 305: instance 150 in, instance 162 out) and cross-checked with Chapter 5 Tables 15-20 (PDF pp. 116-120). The 'Byte' column of those tables is 0-based and is what `enip` uses, counted from byte 0 of the assembly: bytes 0-3 of instance 150 are the 4 reserved connection-status bytes the EDS also states, so the status bits start at byte 4. Sizes agree with the EDS: 16 bytes in (4 + 12), 3 bytes out. Not read: instances 151/166 (284E inverter starters only, a different EDS) and the parameter objects. Open: the manual calls the Hand bit 'HOA is in Auto mode' (a `[[questions]]` entry). No unit has confirmed any point; the wire byte order of the four parameter words is inferred.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 150 /  | 162 /  | 1 |
| Connection2 | Listen Only | 150 /  | 192 / 0 | 1 |
| Connection3 | Input Only | 150 /  | 191 / 0 | 1 |
| Connection4 | ODVA Exclusive Owner | 52 /  | 3 /  | 1 |
| Connection5 | ODVA Listen Only | 52 /  | 192 / 0 | 1 |
| Connection6 | ODVA Input Only | 52 /  | 191 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ArmorStart EtherNet/IP family (280E/281E): ODVA Declaration of Conformity | `1836745b0fb1d49b…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/555/10910_DOC_071422.pdf; retrieved 2026-11-23; not redistributed here |
| ArmorStart EtherNet/IP family (280E/281E): EDS (ODVA marketplace) | `247261c77de33150…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/555/10910.04-EDS.zip; retrieved 2026-11-23; not redistributed here |
| ArmorStart with EtherNet/IP User Manual, Bulletin 280E, 281E, 284E, 280E-UM001C-EN-P | `aa6b32b8256d408d…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/um/280e-um001_-en-p.pdf; fetched in a browser 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
