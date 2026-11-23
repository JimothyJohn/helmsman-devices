> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Festo VABX-A-S-EL-E12-CTED-EP

EDS identity: vendor 26 Festo, product code
14065, device type 12 Communications Adapter,
revision 1.2; EDS file revision
1.0 (02-27-2026).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | I/O Con. Fixed SINT 16 | 110 / 16..16 (Param3) | 111 / 16..16 (Param4) | 140 |
| Connection2 | I/O Con. Fixed SINT 32 | 112 / 32..32 (Param5) | 113 / 32..32 (Param6) | 140 |
| Connection3 | I/O Con. Fixed SINT 64 | 114 / 64..64 (Param7) | 115 / 64..64 (Param8) | 140 |
| Connection4 | I/O Con. Fixed DINT 64 | 120 / 64..64 (Param7) | 121 / 64..64 (Param8) | 140 |
| Connection5 | I/O Con. Fixed DINT 128 | 122 / 128..128 (Param12) | 123 / 128..128 (Param13) | 140 |
| Connection6 | I/O Con. Fixed DINT 488/496 | 124 / 488..488 (Param14) | 125 / 496..496 (Param15) | 140 |
| Connection7 | StatusOnly Data | 130 / 12 | 254 / 0 | 140 |
| Connection8 | Diagnostic Data | 129 / 24..480 (Param9) | 254 / 0 | 140 |
| Connection9 | Listen Only | 100 / 1..488 (Param1) | 255 / 0 | 140 |
| Connection10 | Exact I/O size | 100 / 1..488 (Param1) | 101 / 1..496 (Param2) | 140 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| VABX-A-S-EL-E12-CTED-EP / VABX-A-P-EL-E12-CTED-EP EDS (ODVA marketplace, product 2973) | `6893130fd051baab…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2973/12717.01_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
