> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# ifm AL1222

EDS identity: vendor 322 ifm electronic, product code
1222, device type 12 Communications Adapter,
revision 1.5; EDS file revision
1.12 (04-24-2020).

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
| ifm IO-Link Master XL EIP XP IP67 / CL EIP 8P IP20 / XL EIP XP IP69K, ODVA declaration of conformity (ODVA Marketplace) | `17dcd8b16b7daa05…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1857/11600_DOC_061920.pdf; retrieved 2026-11-23; not redistributed here |
| ifm IO-Link Master XL EIP XP IP67 / CL EIP 8P IP20 / XL EIP XP IP69K, EDS (ODVA Marketplace) | `f96eab82c48e0c96…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1857/11600.04-EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
