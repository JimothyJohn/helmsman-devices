> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Omron ERT1-ID32SLH-1

EDS identity: vendor 47 OMRON Corporation, product code
1104, device type 7 General Purpose Discrete I/O,
revision 2.1; EDS file revision
2.1 (11-17-2008).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | 01_Input Only | 6 / 4 | 199 / 0 | 1 |
| Connection2 | 02_Generic Status Only | 100 / 2 | 199 / 0 | 1 |
| Connection3 | 03_IO Status Only | 136 / 8 | 199 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ERT1-_32SLH-1 high density EtherNet/IP remote I/O datasheet | `4c1de6bd123f75fb…` | https://assets.omron.eu/downloads/latest/datasheet/en/r34i_ert1-_32slh-1_ethernet_ip_screwless_remote_i_o_datasheet_en.pdf; retrieved 2026-11-14; not redistributed here |
| EDS for ERT1-XD16CH-1, ERT1-XD32SLH-1, ERT1-OD32SLH-1 (ODVA marketplace, product 1237) | `4c8b911751eab799…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1237/10718-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
