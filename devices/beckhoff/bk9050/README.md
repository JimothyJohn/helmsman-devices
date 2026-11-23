> **Draft from documents.** No unit has been checked; every value here is
> read from the manual. Nothing was run against a device.

# Beckhoff BK9050

Compact Ethernet Bus Coupler for K-bus Bus Terminals. It speaks Modbus TCP
(port 502) and Beckhoff's ADS; it has no EtherNet/IP and no EDS. One manual
covers the BK9000, BK9050 and BK9100, so this folder uses only what is stated
for all three or for the BK9050.

## What the manual gives

- Modbus TCP interface table (p. 58): process data inputs from address 0x0000,
  outputs from 0x0800, coupler identification, status, process image lengths
  and the watchdog registers from 0x1000.
- Function codes 1, 2, 3, 4, 5, 6, 8, 15, 16 and 23 (p. 60-66).

## What a unit must settle

- Which Modbus function codes reach the 0x1000 register block (see the
  question in `device.toml`).
- How the bit view (coils, discrete inputs) and the word view of the
  process image line up for a given terminal set; marked **inferred** in the points.

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| BK9000, BK9050 and BK9100 Bus Coupler Documentation V4.7.0 | `8bad38660eadc363…` | https://download.beckhoff.com/download/document/io/bus-terminals/bk9000_bk9050_bk9100en.pdf; retrieved 2026-11-23; not redistributed here |

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
