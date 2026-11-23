> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation ArmorStart LT 290E/291E/294E (EtherNet/IP)

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
769, device type 22 Motor Starter,
revision 2.1; EDS file revision
2.01 (1-17-2019).

## What this folder stands for

A substitute for the second ArmorStart candidate: ArmorStart LT 290E/291E/294E. ODVA's `10993.02-EDS.zip` holds one EDS per rating; the drafted one is the 290E 0.24-3.5A, `0001001603010200.eds`. The others were not drafted.Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 152 /  | 150 /  | 100 |
| Connection2 | Listen Only | 152 /  | 192 / 0 | 100 |
| Connection3 | Input Only | 152 /  | 191 / 0 | 100 |
| Connection4 | ODVA Exclusive Owner | 52 /  | 3 /  | 100 |
| Connection5 | ODVA Listen Only | 52 /  | 192 / 0 | 100 |
| Connection6 | ODVA Input Only | 52 /  | 191 / 0 | 100 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ArmorStart LT EtherNet/IP family: ODVA Declaration of Conformity | `8155a32a7c606b77…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/556/10993_DOC_083020.pdf; retrieved 2026-11-23; not redistributed here |
| ArmorStart LT EtherNet/IP family: EDS (ODVA marketplace) | `07c2f541dc2a416f…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/556/10993.02-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
