> **Draft from documents.** No unit has been checked. Identity and connections
> are the EDS's, read by `scripts/eds-draft.py`; the points are read from the
> operating instructions, with the page for each. No unit has confirmed any of them.

# Festo CTEU-EP

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

## Points

Nine points, all from the operating instructions (CTEU-EP_2017-02a, a 2-page
sheet), PDF p. 1 (section 5.2, DIL switches) and p. 2 (section 5.5, the
"Connection Parameters" table). They give the size and instance of each
connection: single port 8 bytes out and in (110/111), dual port 16, 32 and 64
bytes (120/121, 130/131, 140/141), and the two status bytes (DIL switch 2.5
ON prefixes them to the input image; assembly 103 carries them on a separate
connection). The bytes are the I-Port device's: which bit switches which
solenoid coil depends on the valve terminal or connection box behind the bus
node, and the manual does not give a coil table (it refers to an "Appendix to
operating instructions" that is not in the store). So no point names a coil.
Where the status bytes sit in the image ("prefixed", so bytes 0 and 1) is
inferred. The 2024-07 "additional information" is a cyber-security addendum
(ports and service functions) and has no process data.

No unit has confirmed any of this.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| CTEU-EP EDS (ODVA marketplace, product 1771) | `ca6bf7b5be775efd…` | https://nyc3.digitaloceanspaces.com/odva-marketplace/uploads/product/eds_file/1771/CTEU-EP.eds; retrieved 2026-11-23; not redistributed here |
| Operating instructions CTEU-EP (2017-02a), 2 pages | `de54e31c2882b1c8…` | https://www.festo.com/assets/attachment/en/661102, downloaded in a browser 2026-11-23; private store |
| CTEU-EP / CTEU-VN additional information (2024-07), cyber security addendum | `e50154d290627a0b…` | https://www.festo.com/assets/attachment/en/700368, downloaded in a browser 2026-11-23; private store |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
