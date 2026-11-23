> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Festo AG & Co. KG CTEU-EP

EDS identity: vendor 26 Festo AG & Co. KG, product code
6001, device type 12 Communications Adapter,
revision 2.2; EDS file revision
1.3 (12-11-2015).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | I/O Con. Single Port | 111 / 8..10 (Param1) | 110 / 8..8 (Param2) | 102 |
| Connection2 | I/O Con. Dual Port 16 | 121 / 16..18 (Param3) | 120 / 16..16 (Param4) | 102 |
| Connection3 | I/O Con. Dual Port 32 | 131 / 32..34 (Param5) | 130 / 32..32 (Param6) | 102 |
| Connection4 | I/O Con. Dual Port 64 | 141 / 64..66 (Param7) | 140 / 64..64 (Param8) | 102 |
| Connection5 | Diagnostic Data | 103 / 2..2 (Param9) | 254 / 0 | 102 |
| Connection6 | Listen Only | 101 / 0..64 (Param10) | 255 / 0 | 102 |
| Connection7 | Exact I/O size | 101 / 0..64 (Param10) | 100 / 0..64 (Param12) | 102 |
| Connection8 | Input Only | 101 / 0..64 (Param10) | 254 / 0 | 102 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| CTEU-EP EDS (ODVA marketplace, product 1771) | `ca6bf7b5be775efd…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1771/CTEU-EP.eds; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
