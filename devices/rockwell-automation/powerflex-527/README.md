> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation PowerFlex 527 (embedded EtherNet/IP, STO CIP Safety listing)

EDS identity: vendor 1 Rockwell Automation - Allen-Bradley, product code
15, device type 45 CIP Motion Safety Drive,
revision 2.3; EDS file revision
1.0 (04-01-2019).

## What this folder stands for

Stands for the PowerFlex 527 (cat. 25C) with its embedded dual-port EtherNet/IP. The only EDS ODVA lists for it is the 527-STO CIP Safety one (conformance listing 1966, DOC 11388), drafted here: a CIP Motion safety connection of 500 bytes each way. A 527 without the STO option may use another EDS; that one was not found.Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | CIP Motion Safety Drive Exclusive Owner | 2 / 500 | 81 / 500 |  |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 527-STO CIP Safety: ODVA Declaration of Conformity | `e7cf75e9a25ea688…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1966/11388_DOC_052522.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 527-STO CIP Safety: EDS (ODVA marketplace) | `58e97c3d7178d4da…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1966/0001002D000F0200.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
