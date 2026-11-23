> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Schneider Electric Lexium 32M with VW3A3616

EDS identity: vendor 243 Schneider Electric, product code
2564, device type 0 Generic Device,
revision 1.20; EDS file revision
1.11 (08-23-2022).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 113 / 38 | 103 / 38 | 5 |
| Connection2 | Input Only | 113 / 38 | 198 / 0 | 5 |
| Connection3 | Listen Only | 113 / 38 | 199 / 0 | 5 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Ethernet EDS VW3A3616 V1.20 (EDS files for the VW3A3616 card) | `21eacb40dfd56362…` | https://download.se.com/files?p_Doc_Ref=Ethernet_EDS_VW3A3616_V1.20&p_enDocType=Software+-+Data+Library&p_File_Name=Ethernet_EDS_VW3A3616_V1.20.zip; retrieved 2026-11-23; not redistributed here |
| VW3A3616 - LXM32M Ethernet TCP/IP Module (Protocol EtherNet/IP) User Guide (0198441113802) | `6a2f23d1c81400e6…` | https://download.se.com/files?p_Doc_Ref=0198441113802-EN&p_enDocType=User+guide&p_File_Name=0198441113802_LXM32M+EtherNet_IP_EN.pdf; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
