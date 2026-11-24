> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# WEG CFW300

EDS identity: vendor 853 WEG, product code
5376, device type 43 Generic Device,
revision 3.1; EDS file revision
1.0 (10-04-2019).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | 100/150 Manufacturer Speed and Drive Parameters | 150 / 4..16 (Param6) | 100 / 4..16 (Param5) | 1 |
| Connection2 | 120/170 Basic Speed and Drive Parameters | 170 / 4..16 (Param6) | 120 / 4..16 (Param5) | 1 |
| Connection3 | 121/171 Extended Speed and Drive Parameters | 171 / 4..16 (Param6) | 121 / 4..16 (Param5) | 1 |
| Connection4 | Listen Only Connection | 150 / 4..16 (Param6) | 199 / 0 | 1 |

## Scope

WEG CFW300 with its EtherNet/IP plug-in; the EDS gives no assembly sizes (instances 100 and 150).

## What a unit must settle

Everything: no unit has been on the bench, and no manual's I/O map has been read, so there are no points yet.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| WEG CFW300: declaration of conformity (ODVA), ODVA marketplace product 2202 | `a3c5162fa2aab6cc…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2202/11954_DOC_122019.pdf; retrieved 2026-11-23; not redistributed here |
| WEG CFW300: EDS, ODVA marketplace product 2202 | `c45ab18f67fb60bc…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2202/11954.01-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
