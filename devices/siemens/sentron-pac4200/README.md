> **Draft from documents.** No unit has been checked; every value here is the
> manual's, with its page. Anything not on a page says **inferred**.

# Siemens SENTRON PAC4200

Power monitoring device with Ethernet and a configurable Modbus TCP port (default 502; 0 turns it off, System Manual p. 119). Appendix A.2 holds the Modbus tables with function codes 0x03/0x04 (A.2.1, p. 146) and Read Device Identification with FC 0x2B (A.2.19, p. 212). The device can also be configured over Modbus TCP, with an IP filter table for read or read/write access (Section 7.3).

Four rows of Table A-1 are given as points (voltage L1-N, current L1, frequency, total active power); the appendix has many more. The page numbers are the manual's printed ones.

The manual is listed in `collect/siemens.toml` with its hash; it is not in this repository.
