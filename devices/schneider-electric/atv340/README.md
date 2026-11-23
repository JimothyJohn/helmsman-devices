> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Schneider Electric Altivar Machine ATV340 (embedded Ethernet)

EDS identity: vendor 243 Schneider Electric, product code
6176, device type 2 Altivar Machine,
revision 3.4; EDS file revision
1.12 (04-26-2021).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | CIP Basic Control | 70 / 4 | 20 / 4 | 1 |
| Connection2 | CIP Extended Control | 71 / 4 | 21 / 4 | 1 |
| Connection3 | Native Drive Control | 101 / 64 | 100 / 64 | 1 |
| Connection4 | CIP Basic Control Input [Listen Only] | 70 / 4 | 199 / 0 | 1 |
| Connection5 | CIP Extended Control Input [Listen Only] | 71 / 4 | 199 / 0 | 1 |
| Connection6 | Native Drive Control Input [Listen Only] | 101 / 64 | 199 / 0 | 1 |
| Connection7 | CIP Basic Control Input [Input Only] | 70 / 4 | 198 / 0 | 1 |
| Connection8 | CIP Extended Control Input [Input Only] | 71 / 4 | 198 / 0 | 1 |
| Connection9 | Native Drive Control Input [Input Only] | 101 / 64 | 198 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ATV340 Ethernet IP Embedded EDS V3.6 | `46cd0b7348bfbde8…` | https://download.se.com/files?p_Doc_Ref=ATV340_Ethernet_IP_Emb_V3.6&p_enDocType=Software+-+Data+Library&p_File_Name=ATV340_Ethernet_IP_Embedded_EDS_V3.6.zip; retrieved 2026-11-23; not redistributed here |
| ATV340 Ethernet Embedded Manual (NVE61653.03) | `4c0f9ab27f7f8ade…` | https://download.se.com/files?p_Doc_Ref=NVE61653&p_enDocType=User+guide&p_File_Name=ATV340_Ethernet_Embedded_Manual_NVE61653_03.pdf; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
