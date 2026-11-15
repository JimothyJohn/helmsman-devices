> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and wiring in device.toml are read
> from the data sheet, with the page for each; the connection sizes left blank
> below are parameters the EDS lets the scanner choose (see device.toml).

# Phoenix Contact AXL F BK EIP EF

EDS identity: vendor 562 Phoenix Contact, product code
8169, device type 12 Communications Adapter,
revision 1.10; EDS file revision
1.03 (09-07-2016).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Class1 Exclusive Owner | 110 /  | 100 /  | 1 |
| Connection2 | Class1 Input Only | 110 /  | 198 / 0 | 1 |
| Connection3 | Class1 Listen Only | 110 /  | 199 / 0 | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| AXL F BK EIP EF data sheet 107469_en_01 (DigiKey mirror) | `f20dca065b58f94b…` | https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/778/2702782_Ds.pdf; retrieved 2026-11-14; not redistributed here |
| AXL F BK EIP EF EDS (ODVA marketplace 1873) | `a77166694c46c26f…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1873/AXL_F_BK_EIP_EF.eds; retrieved 2026-11-14; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
