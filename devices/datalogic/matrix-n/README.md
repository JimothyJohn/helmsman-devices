> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Datalogic Matrix N Series

EDS identity: vendor 850 Datalogic, Inc., product code
3000, device type 43 Generic Device (keyable),
revision 1.8; EDS file revision
1.8 (08-01-2023).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 101 / 138..138 (Param2) | 113 / 3..4 (Param3) | 128 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Datalogic MATRIX N product line (Matrix 120N, 210N, 220N, 300N, 320N, 410N, 450N), ODVA declaration of conformity (ODVA Marketplace) | `4e1e5721d495b6e6…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/461/10049_DOC_103123.pdf; retrieved 2026-11-23; not redistributed here |
| Datalogic MATRIX N product line (Matrix 120N, 210N, 220N, 300N, 320N, 410N, 450N), EDS (ODVA Marketplace) | `fa431657fd6394bf…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/461/10049.03_EDSFile.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
