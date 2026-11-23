> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# ifm AL1326

EDS identity: vendor 322 ifm electronic, product code
1007, device type 12 Communications Adapter,
revision 2.3; EDS file revision
1.7 (04-27-2023).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Exclusive Owner IO-Acyc-Diag | 100 / 0..446 (Param1) | 150 / 0..302 (Param2) | 199 |
| Connection2 | Exclusive Owner IO-Acyc | 101 / 0..318 (Param11) | 150 / 0..302 (Param2) | 199 |
| Connection3 | Exclusive Owner IO | 102 / 0..276 (Param12) | 151 / 0..258 (Param13) | 199 |
| Connection4 | Input only | 100 / 0..446 (Param1) | 193 / 0 | 199 |
| Connection5 | Listen Only | 100 / 0..446 (Param1) | 192 / 0 | 199 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| ifm IO-Link Master PFL EIP XP IP67 / PFL EIP XP IP69K / DL EIP XP IP69K / CL EIP 8P IP20, ODVA declaration of conformity (ODVA Marketplace) | `400bde222c05ae2b…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/2234/11979_DOC_060623.pdf; retrieved 2026-11-23; not redistributed here |
| ifm IO-Link Master PFL EIP XP IP67 / PFL EIP XP IP69K / DL EIP XP IP69K / CL EIP 8P IP20, EDS (ODVA Marketplace) | `1b67d5dd337c5090…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/2234/11979.02_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
