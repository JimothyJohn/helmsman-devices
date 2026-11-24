> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# Cognex DataMan 300 Series Reader

EDS identity: vendor 678 Cognex, product code
1290, device type 773 DataMan 300 Series Reader,
revision 1.5; EDS file revision
1.2 (09-03-2015).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
| Connection1 | Consume Data From/Produce Data To | 11 / 2..500 (Param2) | 21 / 2..500 (Param3) | 1 |
| Connection2 | Consume Data From | 11 / 2..500 (Param2) | 254 / 0 | 1 |
| Connection3 | Produce Data To | 254 / 0 | 21 / 2..500 (Param3) | 1 |

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| Cognex DataMan DM30x, DM36x, AID36x readers, ODVA declaration of conformity (ODVA Marketplace) | `091798f45c8a0d42…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/doc_file/1679/11346_DOC_11022015.pdf; retrieved 2026-11-23; not redistributed here |
| Cognex DataMan DM30x, DM36x, AID36x readers, EDS (ODVA Marketplace) | `12b1749f01a75311…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1679/11346.02_EDS.zip; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
