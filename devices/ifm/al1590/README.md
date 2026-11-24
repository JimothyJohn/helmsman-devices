> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# ifm AL1590

EDS identity: vendor 322 ifm electronic, product code
1590, device type 12 Communications Adapter,
revision 1.1; EDS file revision
1.1 (04-02-2025).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner IO-Acyc-Diag-EnMo | 101 / 0..450 (Param12) | 151 / 0..302 (Param13) | 199 |
| Connection2 | Exclusive Owner IO | 100 / 0..276 (Param1) | 150 / 0..258 (Param2) | 199 |
| Connection3 | Input Only IO | 100 / 0..276 (Param1) | 193 / 0 | 199 |
| Connection4 | Listen Only IO | 100 / 0..276 (Param1) | 192 / 0 | 199 |
| Connection5 | Input Only IO-Acyc-Diag-EnMo | 101 / 0..450 (Param12) | 193 / 0 | 199 |
| Connection6 | Listen Only IO-Acyc-Diag-EnMo | 101 / 0..450 (Param12) | 192 / 0 | 199 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ifm IO-LINK MASTER SOL MP 8P IP67 / IP69K, ODVA declaration of conformity (ODVA Marketplace) | `f22c45810e294b3e…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2861/12637_DOC_072425.pdf; retrieved 2026-11-23; not redistributed here |
| ifm IO-LINK MASTER SOL MP 8P IP67 / IP69K, EDS (ODVA Marketplace) | `bce2c6886a4fed3d…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2861/12637.01_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
