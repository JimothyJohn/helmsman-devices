> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Novanta IMS Liberty / Lexium MDrive Ethernet (LMD), EtherNet/IP

EDS identity: vendor 243 Schneider Electric, product code
15362, device type 43 Generic Device,
revision 2.22; EDS file revision
1.2 (01-17-2012).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 100 /  | 112 /  | 1 |
| Connection2 | Listen Only | 100 /  | 129 / 0 | 1 |
| Connection3 | Input Only | 100 /  | 128 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| LMD Ethernet TCP/IP Application 2.4.0.9 (firmware package; carries the EDS) | `1bb0038ceae46daf…` | https://www.novantaims.com/download/lmd-ethernet-tcp-ip-application-2-4-0-9/?wpdmdl=33950&refresh=6afbcc0d386a61794886669; retrieved 2026-11-17; not redistributed here |
| Lexium MDrive Ethernet, LMDxE57C and LMDxE85C product manual (03.2015) | `1c90c18f9a1c4b09…` | https://novanta.com/robotics-automation/wp-content/uploads/sites/3/2015/04/LMDxE57-85C.pdf; retrieved 2026-11-17; not redistributed here |
| LM57/LM85 Ethernet TCP/IP with M12 circular connectors (LMDE57-85IP hardware manual) | `750e8e1baf96fa67…` | https://www.novantaims.com/download/liberty-mdrive-ethernet-nema-2334-ip65/?wpdmdl=6719&refresh=6afbcc022b7b31794886658; retrieved 2026-11-17; not redistributed here |
| LM57/LM85 Ethernet TCP/IP with pluggable connectors (LMDE57-85 hardware manual) | `dc3bb12d1b298678…` | https://www.novantaims.com/download/liberty-mdrive-ethernet-nema-2334/?wpdmdl=6713&refresh=6afbcc028ff621794886658; retrieved 2026-11-17; not redistributed here |
| LMD EtherNet/IP Protocol Implementation | `2a5a6f726b2a5b2f…` | https://www.novantaims.com/download/liberty-mdrive-ethernetip/?wpdmdl=6728&refresh=6afbcc0fb6ea01794886671; retrieved 2026-11-17; not redistributed here |
| LMD MCode OS Programming and Reference | `3945e47f63d49752…` | https://www.novantaims.com/download/lmd-mcode-os-programming-and-reference/?wpdmdl=29637&refresh=6afbcc01dcbd91794886657; retrieved 2026-11-17; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
