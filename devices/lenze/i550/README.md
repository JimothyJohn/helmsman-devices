> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Lenze i550 cabinet

EDS identity: vendor 587 Lenze, product code
550, device type 2 AC Drive Device,
revision 7.1; EDS file revision
3.2 (08-04-2026).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Speed | 71 / 4 | 21 / 4 | 130 |
| Connection2 | Speed & Torque | 73 / 6 | 23 / 6 | 130 |
| Connection3 | Custom I/O Connection | 111 /  | 110 /  | 130 |

## Scope

The ODVA listing covers four EDS (i550 cabinet, motec, protec; i650 motec); this folder drafts from the cabinet one. The others differ by product code and are not drafted yet.

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Lenze i550 / i650: declaration of conformity (ODVA), ODVA marketplace product 2570 | `79d08c9f63de375a…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2570/12334_DOC_090926.pdf; retrieved 2026-11-23; not redistributed here |
| Lenze i550 / i650: EDS, ODVA marketplace product 2570 | `7c2cd850def387b2…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2570/12334.03_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
