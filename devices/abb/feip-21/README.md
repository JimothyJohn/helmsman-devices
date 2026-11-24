> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# ABB ABB Drive via Ethernet/IP FEIP-21

EDS identity: vendor 46 ABB, Inc., product code
1, device type 103 Drive,
revision 1.64; EDS file revision
1.2 (04-07-2026).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | ODVA 20/70 Basic speed control | 70 /  | 20 /  | 1 |
| Connection2 | ODVA 21/71 Extended speed control | 71 /  | 21 /  | 1 |
| Connection3 | ODVA 22/72 Basic Speed and Torque control | 72 /  | 22 /  | 1 |
| Connection4 | ODVA 23/73 Extended Speed and Torque control | 73 /  | 23 /  | 1 |
| Connection5 | ODVA 120/170 Basic Speed Control plus Drive Parameters | 170 /  | 120 /  | 1 |
| Connection6 | ODVA 121/171 Enhanced Speed Control plus Drive Parameters | 171 /  | 121 /  | 1 |
| Connection7 | ODVA 122/172 Basic speed and torque control plus Drive parameters | 172 /  | 122 /  | 1 |
| Connection8 | ODVA 123/173 Enhanced speed and torque control plus Drive parameters | 173 /  | 123 /  | 1 |
| Connection9 | ABB Drives 1/51 Set Speed | 51 /  | 1 /  | 1 |
| Connection10 | ABB Drives 2/52 Set Speed and Set Torque | 52 /  | 2 /  | 1 |
| Connection11 | ABB Drives 101/151 Set Speed plus Drive Paramters | 151 /  | 101 /  | 1 |
| Connection12 | ABB Drives 102/152 Set Speed and Set Torque plus Drive Paramters | 152 /  | 102 /  | 1 |
| Connection13 | TRANS16 11/61 One | 61 /  | 11 /  | 1 |
| Connection14 | TRANS16 12/62 Two | 62 /  | 12 /  | 1 |
| Connection15 | TRANS16 111/161 One plus Drive Parameters | 161 /  | 111 /  | 1 |
| Connection16 | TRANS16 112/162 Two plus Drive Parameters | 162 /  | 112 /  | 1 |
| Connection17 | TRANS32 41/91 One | 91 /  | 41 /  | 1 |
| Connection18 | TRANS32 42/92 Two | 92 /  | 42 /  | 1 |
| Connection19 | TRANS32 141/191 One plus Drive Parameters | 191 /  | 141 /  | 1 |
| Connection20 | TRANS32 142/192 Two plus Drive Parameters | 192 /  | 142 /  | 1 |

## Scope

Substituted for the candidate FENA-21: the ODVA marketplace lists the FEIP-21 (ABB's dedicated EtherNet/IP module) with an EDS; no EDS for the FENA-21 or FENA-11 was found, and ABB's product pages could not be read. Which drives take the module is not stated in the files collected here.

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ABB FEIP-21 EtherNet/IP adapter module: declaration of conformity (ODVA), ODVA marketplace product 2829 | `d6ec1bc5d20db9ba…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2829/12553_DOC_092426.pdf; retrieved 2026-11-23; not redistributed here |
| ABB FEIP-21 EtherNet/IP adapter module: EDS, ODVA marketplace product 2829 | `42bf024b5ecb8a0c…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2829/12553.02.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
