> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. The installation instructions in the
> store give no I/O layout, so there are no points (see the end of this file).

# Rockwell Automation 1732E-OB16M12R

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
370, device type 7 General Purpose Discrete I/O,
revision 1.1; EDS file revision
1.004 (09-03-2009).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 192 / 0 | 35 /  | 100 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ArmorBlock 1732E 16-point EDS package 10748.04 | `1e30150bed43e04b…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1240/10748.04-EDS.zip; retrieved 2026-11-23; not redistributed here |
| ArmorBlock 2-port EtherNet/IP Modules Installation Instructions, 1732E-IN009 | `01b24672f1e986f0…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/in/1732e-in009_-en-p.pdf; fetched in a browser 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.

## What is not here

The manual in the store for this folder is the installation instructions 1732E-IN009E (read through its sections for an I/O data layout). They cover mounting, wiring, power, QuickConnect, the status indicators and the specifications, and give no input or output assembly layout: no byte or bit is mapped to a channel. So this folder has no `[[points]]`. The channel count is the EDS's. No unit has been checked. Its Additional Resources do not name a user manual for the I/O data.
