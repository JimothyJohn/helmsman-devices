> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation PowerFlex 6000T

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
10640, device type 143 Vendor Specific,
revision 11.1; EDS file revision
1.3 (05-20-2026).

## What this folder stands for

Stands for the PowerFlex 6000T medium-voltage drive (6000T...), from ODVA listing 2255 (DOC 12040). The EDS file is named `12040.08_EDS` with no extension on ODVA's server.Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Discrete Exclusive Owner | 1 / 12..76 (Param1) | 2 / 8..72 (Param2) | 6 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| PowerFlex 6000T MV AC drive: ODVA Declaration of Conformity | `66cbf2811650eb12…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2255/12040_DOC_082126.pdf; retrieved 2026-11-23; not redistributed here |
| PowerFlex 6000T MV AC drive: EDS (ODVA marketplace) | `42d2fad7e8521edb…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2255/12040.08_EDS; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
