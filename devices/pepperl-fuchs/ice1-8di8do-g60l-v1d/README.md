> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Pepperl+Fuchs ICE1-8DI8DO-G60L-V1D

EDS identity: vendor 57 Pepperl + Fuchs, product code
50, device type 7 General Purpose Discrete I/O,
revision 1.2; EDS file revision
1.1 (02-15-2017).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | 8 Bit In / Out + Diagnostic (Exclusive Owner) | 101 / 6..6 (Param14) | 100 / 1..1 (Param16) | 105 |
| Connection2 | 8 Bit In / Out (Exclusive Owner) | 102 / 3..3 (Param15) | 100 / 1..1 (Param16) | 105 |
| Connection3 | 8 Bit In / Out + Diagnostic (Input Only) | 101 / 6..6 (Param14) | 193 / 0 | 105 |
| Connection4 | 8 Bit In / Out (Input Only) | 102 / 3..3 (Param15) | 193 / 0 | 105 |
| Connection5 | 8 Bit In / Out + Diagnostic (Listen Only) | 101 / 6..6 (Param14) | 192 / 0 | 1 |
| Connection6 | 8 Bit In / Out (Listen Only) | 102 / 3..3 (Param15) | 192 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Pepperl+Fuchs ICE1-8xxxxx-G60x-xx-V1D, ICE1-16xxx-G60x-xx-V1D, ODVA declaration of conformity (ODVA Marketplace) | `f7401b8a30b50f04…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1886/11612_DOC_050417.pdf; retrieved 2026-11-23; not redistributed here |
| Pepperl+Fuchs ICE1-8xxxxx-G60x-xx-V1D, ICE1-16xxx-G60x-xx-V1D, EDS (ODVA Marketplace) | `011c1ac357b3d437…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1886/11612.01_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
