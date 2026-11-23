> **Draft from documents.** No unit has been checked; every value here is the
> EDS's or the manual's, and no unit has confirmed either.

# Rockwell Automation ArmorStart LT 290E/291E/294E (EtherNet/IP)

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
769, device type 22 Motor Starter,
revision 2.1; EDS file revision
2.01 (1-17-2019).

## What this folder stands for

A substitute for the second ArmorStart candidate: ArmorStart LT 290E/291E/294E. ODVA's `10993.02-EDS.zip` holds one EDS per rating; the drafted one is the 290E 0.24-3.5A, `0001001603010200.eds`. The others were not drafted.Manual: 290E-UM001C-EN-P, fetched in a browser because the site answers a plain fetch with 403. The `[[points]]` were read from its Appendix B (PDF pp. 201-202: instance 150 out, instance 152 in) and cross-checked with Chapter 3 Tables 16-21 (PDF pp. 90-95). The 'Byte' column is 0-based and is what `enip` uses, counted from byte 0 of the assembly: bytes 0-3 of instance 152 are reserved (connection fault in the Logix tag). Sizes agree with the EDS: 30 bytes in, 6 bytes out, and the 84-byte configuration assembly 100 (last member at byte 82, 2 bytes). Not read: the 294E assemblies 154/156 (inverter type) and the parameter table. No unit has confirmed any point; the 16-bit values are marked inferred where the manual gives only INT and low/high byte labels.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 152 /  | 150 /  | 100 |
| Connection2 | Listen Only | 152 /  | 192 / 0 | 100 |
| Connection3 | Input Only | 152 /  | 191 / 0 | 100 |
| Connection4 | ODVA Exclusive Owner | 52 /  | 3 /  | 100 |
| Connection5 | ODVA Listen Only | 52 /  | 192 / 0 | 100 |
| Connection6 | ODVA Input Only | 52 /  | 191 / 0 | 100 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ArmorStart LT EtherNet/IP family: ODVA Declaration of Conformity | `8155a32a7c606b77…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/556/10993_DOC_083020.pdf; retrieved 2026-11-23; not redistributed here |
| ArmorStart LT EtherNet/IP family: EDS (ODVA marketplace) | `07c2f541dc2a416f…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/556/10993.02-EDS.zip; retrieved 2026-11-23; not redistributed here |
| ArmorStart LT EtherNet/IP Version User Manual, Bulletin 290E, 291E, 294E, 290E-UM001C-EN-P | `e520232cad2973a1…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/um/290e-um001_-en-p.pdf; fetched in a browser 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
