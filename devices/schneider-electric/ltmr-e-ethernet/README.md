> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Schneider Electric TeSys T LTMR E (Ethernet)

EDS identity: vendor 243 Schneider Electric, product code
304, device type 22 Motor Starter,
revision 1.5; EDS file revision
1.5 (12-09-2019).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Basic Overload | 50 / 1 | 2 / 1 | 6 |
| Connection2 | Extended Overload | 51 / 1 | 2 / 1 | 6 |
| Connection3 | Basic Motor Starter | 52 / 1 | 3 / 1 | 6 |
| Connection4 | Extended Contactor | 53 / 1 | 4 / 1 | 6 |
| Connection5 | Extended Motor Starter 1 | 54 / 1 | 4 / 1 | 6 |
| Connection6 | Extended Motor Starter 2 | 54 / 1 | 5 / 1 | 6 |
| Connection7 | LTMR Control and Monitoring | 110 / 8 | 100 / 6 | 6 |
| Connection8 | PKW | 111 / 8 | 101 / 8 | 6 |
| Connection9 | PKW + Extended Motor Starter | 112 / 10 | 102 / 10 | 6 |
| Connection10 | PKW + LTM1 Monitoring | 113 / 16 | 103 / 14 | 6 |
| Connection11 | E_TeSys T Fast Access | 115 / 12 | 105 / 6 | 6 |
| Connection12 | EIOS_TeSys T | 116 / 128 | 106 / 10 | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| EDS File for TeSys T EIP (1.5.000) | `a9b5d5395bc39b6c…` | https://download.se.com/files?p_Doc_Ref=EIP_EDS_1.5.00&p_enDocType=Software+-+Data+Library&p_File_Name=EDS+EtherNetIP_TeSysT_1.5.000.zip; retrieved 2026-11-23; not redistributed here |
| TeSys T LTMR Motor Management Controller Ethernet Communication Guide (DOCA0129EN 03) | `7f8fcf0166e2778a…` | https://download.se.com/files?p_Doc_Ref=DOCA0129EN&p_enDocType=User+guide&p_File_Name=DOCA0129EN_03.pdf; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
