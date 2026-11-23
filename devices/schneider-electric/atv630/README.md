> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Schneider Electric Altivar Process ATV630 / ATV930 (embedded Ethernet)

EDS identity: vendor 243 Schneider Electric, product code
6192, device type 2 AC Drive Device,
revision 2.1; EDS file revision
1.9 (11-13-2018).

The EDS is one file for the whole ATV900 family (product name `ATV9xx`, one product code),
so the ATV630 and the ATV930 share this folder; the manual covers both.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | CIP Basic Control | 70 / 4 | 20 / 4 | 1 |
| Connection2 | CIP Extended Control | 71 / 4 | 21 / 4 | 1 |
| Connection3 | Native Drive Control | 101 / 64 | 100 / 64 | 1 |
| Connection4 | ATV9xx Assembly | 107 / 24..64 (Param2) | 106 / 12..64 (Param1) | 1 |
| Connection5 | CIP Basic Control Input [Listen Only] | 70 / 4 | 199 / 0 | 1 |
| Connection6 | CIP Extended Control Input [Listen Only] | 71 / 4 | 199 / 0 | 1 |
| Connection7 | Native Drive Control Input [Listen Only] | 101 / 64 | 199 / 0 | 1 |
| Connection8 | ATV9xx Input Assembly [Listen Only] | 107 / 24..64 (Param2) | 199 / 0 | 1 |
| Connection9 | CIP Basic Control Input [Input Only] | 70 / 4 | 198 / 0 | 1 |
| Connection10 | CIP Extended Control Input [Input Only] | 71 / 4 | 198 / 0 | 1 |
| Connection11 | Native Drive Control Input [Input Only] | 101 / 64 | 198 / 0 | 1 |
| Connection12 | ATV9xx Input Assembly [Input Only] | 107 / 24..64 (Param2) | 198 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ATV900 Ethernet IP Embedded EDS V2.3 | `f2f51d2198f16e1d…` | https://download.se.com/files?p_Doc_Ref=Ethernet_IP_Embedded_EDS_V2.3&p_enDocType=Software+-+Data+Library&p_File_Name=ATV900_Ethernet_IP_Embedded_EDS_V2.3.zip; retrieved 2026-11-23; not redistributed here |
| ATV900 Embedded Ethernet manual (NHA80940.03) | `d83eebd45ea5f506…` | https://download.se.com/files?p_Doc_Ref=NHA80940&p_enDocType=User+guide&p_File_Name=ATV900_Ethernet_Manual_Embedded_NHA80940_03.pdf; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
