> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# WEG SSW900

EDS identity: vendor 853 WEG, product code
5888, device type 43 Generic Device,
revision 1.30; EDS file revision
1.0 (10-04-2019).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | 110/160 Manufacturer Parameters | 160 / 2..100 (Param4) | 110 / 2..40 (Param3) | 1 |
| Connection2 | Listen Only Connection | 160 / 2..100 (Param4) | 199 / 0 | 1 |

## Scope

A soft starter, not a drive: kind is `other`.

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| WEG SSW900: declaration of conformity (ODVA), ODVA marketplace product 2394 | `6b22e25567968fc1…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2394/12119_DOC_070121.pdf; retrieved 2026-11-23; not redistributed here |
| WEG SSW900: EDS, ODVA marketplace product 2394 | `8ed475238b4c7fa6…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2394/12119.01-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
