> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. The installation instructions in the
> store give no I/O layout, so there are no points (see the end of this file).

# Rockwell Automation 1732E-16CFGM12R

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
357, device type 7 General Purpose Discrete I/O,
revision 3.12; EDS file revision
3.12 (07-17-2022).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Logix - Exclusive Owner | 105 /  | 35 /  | 102 |
| Connection2 | Open - Exclusive Owner | 5 /  | 35 /  | 102 |
| Connection3 | Logix - Listen Only | 105 /  | 191 / 0 | 102 |
| Connection4 | Open - Listen Only | 5 /  | 191 / 0 | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ArmorBlock 1732E 16-point M12 EDS package 11894.05 | `6d733a423323020a…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2159/11894.05-EDS.zip; retrieved 2026-11-23; not redistributed here |
| ArmorBlock 2-port EtherNet/IP Modules Installation Instructions, 1732E-IN009 | `01b24672f1e986f0…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/in/1732e-in009_-en-p.pdf; fetched in a browser 2026-11-23; not redistributed here |
| ArmorBlock I/O 16-channel Configurable Digital Modules Installation Instructions, 1732E-IN008 | `4d178b8251128919…` | https://literature.rockwellautomation.com/idc/groups/literature/documents/in/1732e-in008_-en-p.pdf; fetched in a browser 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.

## What is not here

The manuals in the store for this folder are the installation instructions 1732E-IN009E and 1732E-IN008C (both read through their sections for an I/O data layout). They cover mounting, wiring, power, QuickConnect, the status indicators and the specifications, and give no input or output assembly layout: no byte or bit is mapped to a channel. So this folder has no `[[points]]`. The channel count is the EDS's. No unit has been checked. 1732E-IN008C (Additional Resources, PDF p. 9) names the ArmorBlock 16-channel Configurable Digital Module User Manual, publication 1732E-UM001, as the place for configuring and operating the module; it is not in the store, and would be the next document to collect for the bit order and the input/output configuration.
