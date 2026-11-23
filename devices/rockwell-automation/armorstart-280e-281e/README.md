> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Rockwell Automation ArmorStart 280E/281E (EtherNet/IP)

EDS identity: vendor 1 Rockwell Automation/Allen-Bradley, product code
145, device type 22 Motor Starter,
revision 2.3; EDS file revision
2.1 (02-19-2016).

## What this folder stands for

Stands for the ArmorStart 280E/281E (and 284E) distributed motor controllers. ODVA's `10910.04-EDS.zip` holds one EDS per rating and variant (29); the drafted one is the 280E 0.5-2.5A 24 VDC, `0001001600910200.eds`, whose product code and assembly sizes may differ for the others. The others were not drafted.Manuals: Rockwell's literature site refused the fetcher (HTTP 403), so no manual was read for this folder. It has no `[[points]]`; the assemblies are the EDS's, and what their bytes mean is still to be read from the manual.

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner | 150 /  | 162 /  | 1 |
| Connection2 | Listen Only | 150 /  | 192 / 0 | 1 |
| Connection3 | Input Only | 150 /  | 191 / 0 | 1 |
| Connection4 | ODVA Exclusive Owner | 52 /  | 3 /  | 1 |
| Connection5 | ODVA Listen Only | 52 /  | 192 / 0 | 1 |
| Connection6 | ODVA Input Only | 52 /  | 191 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ArmorStart EtherNet/IP family (280E/281E): ODVA Declaration of Conformity | `1836745b0fb1d49b…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/555/10910_DOC_071422.pdf; retrieved 2026-11-23; not redistributed here |
| ArmorStart EtherNet/IP family (280E/281E): EDS (ODVA marketplace) | `247261c77de33150…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/555/10910.04-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
