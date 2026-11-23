> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. The manual was read and gives no
> `[[points]]` for this connection (see below).

# Rockwell Automation PowerFlex 527 (embedded EtherNet/IP, STO CIP Safety listing)

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
15, device type 45 CIP Motion Safety Drive,
revision 2.3; EDS file revision
1.0 (04-01-2019).

## What this folder stands for

Stands for the PowerFlex 527 (cat. 25C) with its embedded dual-port EtherNet/IP. The only EDS ODVA lists for it is the 527-STO CIP Safety one (conformance listing 1966, DOC 11388), drafted here: a CIP Motion safety connection of 500 bytes each way. A 527 without the STO option may use another EDS; that one was not found.Manual: PowerFlex 527 Adjustable Frequency AC Drive User Manual 520-UM002F-EN-E (September 2025), fetched in a browser and read. It has no `[[points]]` here, on purpose: the EDS's connection is a CIP Motion safety drive connection (500 bytes each way), and the manual gives it no logic command, logic status, reference or datalink layout. It says the drive is controlled with CIP Motion commands from a Logix controller (Integrated Motion on the EtherNet/IP Network Reference Manual, MAFR and the axis tags), and the only bit tables it holds are for the Safe Torque Off safety connection (Table 9, PDF p. 92: `SI.TorqueDisabled`, `SI.SafetyFault`, `SI.ResetRequired`, `SO.SafeTorqueOff`, `SO.Reset`). Those are CIP Safety assembly attributes (0x1A0 and 0x180 are attribute ids, not byte offsets) on a separate safety connection whose size and byte layout the manual does not give, so none of them is written as a point. The 500-byte sizes are the EDS's and the manual neither confirms nor contradicts them. No unit has been checked.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | CIP Motion Safety Drive Exclusive Owner | 2 / 500 | 81 / 500 |  |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 527-STO CIP Safety: ODVA Declaration of Conformity | `e7cf75e9a25ea688…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1966/11388_DOC_052522.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 527-STO CIP Safety: EDS (ODVA marketplace) | `58e97c3d7178d4da…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1966/0001002D000F0200.eds; retrieved 2026-11-23; not redistributed here |
| PowerFlex 527 Adjustable Frequency AC Drive User Manual, 520-UM002F-EN-E | `9b722b7a8e5befda…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/um/520-um002_-en-e.pdf; retrieved 2026-11-23, fetched in a browser; not redistributed here |


Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
