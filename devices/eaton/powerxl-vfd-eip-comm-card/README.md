> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Eaton PowerXL VFD EIP Comm. Card

EDS identity: vendor 68 Eaton Electrical, product code
12338, device type 2 AC Drive Device,
revision 2.1; EDS file revision
1.9 (06-09-2026).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Asm 20 OT - 70 TO | 70 /  | 20 /  | 1 |
| Connection2 | Asm 20 OT - 129 TO | 129 /  | 20 /  | 1 |
| Connection3 | Asm 20 OT - 130 TO | 130 /  | 20 /  | 1 |
| Connection4 | Asm 20 OT - 131 TO | 131 /  | 20 /  | 1 |
| Connection5 | Asm 121 OT - 70 TO | 70 /  | 121 /  | 1 |
| Connection6 | Asm 121 OT - 129 TO | 129 /  | 121 /  | 1 |
| Connection7 | Asm 121 OT - 130 TO | 130 /  | 121 /  | 1 |
| Connection8 | Asm 121 OT - 131 TO | 131 /  | 121 /  | 1 |
| Connection9 | Asm 122 OT - 70 TO | 70 /  | 122 /  | 1 |
| Connection10 | Asm 122 OT - 129 TO | 129 /  | 122 /  | 1 |
| Connection11 | Asm 122 OT - 130 TO | 130 /  | 122 /  | 1 |
| Connection12 | Asm 122 OT - 131 TO | 131 /  | 122 /  | 1 |
| Connection13 | Asm 123 OT - 70 TO | 70 /  | 123 /  | 1 |
| Connection14 | Asm 123 OT - 129 TO | 129 /  | 123 /  | 1 |
| Connection15 | Asm 123 OT - 130 TO | 130 /  | 123 /  | 1 |
| Connection16 | Asm 123 OT - 131 TO | 131 /  | 123 /  | 1 |
| Connection17 | Asm 124 OT - 132 TO | 132 /  | 124 /  | 1 |

## Scope

Eaton's EtherNet/IP communication card for PowerXL VFDs (v1.9 EDS). Which drives take it is not stated in the files collected here.

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Eaton PowerXL EtherNet/IP comm card: declaration of conformity (ODVA), ODVA marketplace product 2764 | `ac8a66900ee14a4d…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2764/12511_DOC_090226.pdf; retrieved 2026-11-23; not redistributed here |
| Eaton PowerXL EtherNet/IP comm card: EDS, ODVA marketplace product 2764 | `665a566f6fa43ac4…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2764/PowerXL_VFD_EIP_Comm_Card_v1.9.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
