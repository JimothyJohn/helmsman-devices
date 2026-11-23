> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Banner Engineering Corp. Banner DXM

EDS identity: vendor 12 Banner Engineering Corp., product code
200, device type 43 Generic Device,
revision 2.22; EDS file revision
1.1 (01-16-2023).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | DXM Assemblies | 100 /  | 112 /  | 128 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| DXM Controller EDS File (12 Sep 2023), listed on the DXMR90-4K part page | `f5121dd57399b14a…` | https://info.bannerengineering.com/_dav/cs/idcplg?IdcService=GET_FILE&RevisionSelectionMethod=LatestReleased&dDocName=B_4205242; retrieved 2026-11-23; not redistributed here |
| DXMR90-4K IO-Link Master Product Manual, English (26 Jan 2026) | `7935c2323fb8dbf0…` | https://info.bannerengineering.com/cs/groups/public/documents/literature/229492.pdf; retrieved 2026-11-23; not redistributed here |
| DXMR90-4K Device Register and IO-Link Data Reference Guide (16 Sep 2025) | `c2d7b862f844dd4d…` | https://info.bannerengineering.com/cs/groups/public/documents/literature/229732.pdf; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
