> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Schneider Electric Altivar Machine ATV320 with VW3A3616

EDS identity: vendor 243 Schneider Electric, product code
6153, device type 2 AC Drive Device,
revision 1.20; EDS file revision
1.04 (08-23-2022).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | CIP Basic Control | 70 / 4 | 20 / 4 | 5 |
| Connection2 | CIP Extended Control | 71 / 4 | 21 / 4 | 5 |
| Connection3 | Native Drive Control | 101 / 12 | 100 / 12 | 5 |
| Connection4 | CIP Basic Control [Listen Only] | 70 / 4 | 199 / 0 | 5 |
| Connection5 | CIP Extended Control [Listen Only] | 71 / 0 | 199 / 0 | 5 |
| Connection6 | Native Drive Control [Listen Only] | 101 / 12 | 199 / 0 | 5 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Ethernet EDS VW3A3616 V1.20 (EDS files for the VW3A3616 card) | `21eacb40dfd56362…` | https://download.se.com/files?p_Doc_Ref=Ethernet_EDS_VW3A3616_V1.20&p_enDocType=Software+-+Data+Library&p_File_Name=Ethernet_EDS_VW3A3616_V1.20.zip; retrieved 2026-11-23; not redistributed here |
| ATV320 Modbus TCP-EtherNet IP Manual (NVE41313.02) | `23f1712406743b5f…` | https://download.se.com/files?p_Doc_Ref=NVE41313&p_enDocType=User+guide&p_File_Name=ATV320_Modbus_TCP_EtherNet_IP_Manual_NVE41313_02.pdf; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
