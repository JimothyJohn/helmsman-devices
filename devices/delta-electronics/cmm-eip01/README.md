> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Delta electronics, inc. CMM-EIP01

EDS identity: vendor 799 Delta electronics, inc., product code
260, device type 12 Communications Adapter,
revision 1.1; EDS file revision
1.01 (02-08-2017).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | IO Connection | 105 /  | 104 /  | 128 |
| Connection2 | IO Connection listen only | 105 /  | 199 / 0 | 128 |

## Scope

CMM-EIP01, Delta's EtherNet/IP communication card for its AC drives; the MS300 with CMM-EIP02 was not found on the ODVA marketplace. Which drives take the card is not stated in the files collected here.

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Delta CMM-EIP01: declaration of conformity (ODVA), ODVA marketplace product 1924 | `87f27de8f6ca5f4f…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1924/11630_DOC_081617.pdf; retrieved 2026-11-23; not redistributed here |
| Delta CMM-EIP01: EDS, ODVA marketplace product 1924 | `4dcd355ef630c292…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1924/11630.01-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
