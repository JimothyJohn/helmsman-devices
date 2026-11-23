> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Pepperl+Fuchs ICE21-8IOL2-G70L-V1D

EDS identity: vendor 57 Pepperl+Fuchs, product code
69, device type 12 Communications Adapter,
revision 1.7; EDS file revision
1.01 (12-22-2025).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Read/Write All Ports | 101 / 2..499 (Param4) | 117 / 2..499 (Param6) | 1 |
| Connection2 | Read Only - All Ports | 101 / 2..499 (Param4) | 254 / 0 | 1 |

## Channels

No `channels` line: searched 2026-11-23 (web search on the full model number, the article number 70148669 and the family name ICE21; the ODVA Marketplace product page; the Pepperl+Fuchs IO-Link master page `/en/gp32668`) and found no Pepperl+Fuchs data sheet or manual for this model, and the EDS states no port count. The "8IOL" in the model number is not a source.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Pepperl+Fuchs ICE21-8IOL2-G70L-V1D, ODVA declaration of conformity (ODVA Marketplace) | `8f2b24783cd09130…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2992/12602_DOC_070426.pdf; retrieved 2026-11-23; not redistributed here |
| Pepperl+Fuchs ICE21-8IOL2-G70L-V1D, EDS (ODVA Marketplace) | `791d7df8a0cd649f…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2992/12602.02.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
