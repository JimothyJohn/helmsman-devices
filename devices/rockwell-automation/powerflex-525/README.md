> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation PowerFlex 525 (embedded EtherNet/IP)

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
9, device type 151 HS-DSI to EtherNet/IP,
revision 1.3; EDS file revision
1.1 (01-31-2013).

## What this folder stands for

Stands for the PowerFlex 525 (cat. 25B) with its embedded EtherNet/IP port. The EDS drafted is `0001009700090100.eds`, one of two members of ODVA's `11171_EDS.zip`; the other (25-COMM-E2P) is the 523 folder. Ratings are not separate EDS files here, so this stands for the whole 25B range.Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1 / 8..16 (Param1) | 2 / 4..12 (Param2) | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 525 (embedded EtherNet/IP): ODVA Declaration of Conformity | `8e85ae6dc580a772…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/580/11171_DOC_071713.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 525 (embedded EtherNet/IP): EDS (ODVA marketplace) | `388e7f6ed55bb038…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/580/11171_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
