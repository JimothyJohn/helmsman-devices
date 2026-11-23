> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# WEG CFW500

EDS identity: vendor 853 WEG, product code
6656, device type 43 Generic Device,
revision 1.1; EDS file revision
1.0 (11-16-2022).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | 100/150 Manufacturer Speed + I/O data | 150 / 0..28 (Param6) | 100 / 0..28 (Param5) | 1 |
| Connection2 | 120/170 CIP Basic Speed + I/O data | 170 / 0..28 (Param6) | 120 / 0..28 (Param5) | 1 |
| Connection3 | 121/171 CIP Ext. Speed + I/O data | 171 / 0..28 (Param6) | 121 / 0..28 (Param5) | 1 |
| Connection4 | Listen Only Connection | 150 / 0..28 (Param6) | 199 / 0 | 1 |

## Scope

The ODVA listing's zip holds two EDS (CFW500 and MW500); this folder drafts from the CFW500 one (CETH2 card).

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| WEG CFW500: declaration of conformity (ODVA), ODVA marketplace product 2768 | `7809fda67ec0bf33…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2768/12524_DOC_091124.pdf; retrieved 2026-11-23; not redistributed here |
| WEG CFW500: EDS, ODVA marketplace product 2768 | `11acd09b50d3e720…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2768/12524.01.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
