> **Draft from documents.** No unit has been checked; every value here is the
> document's, with its page. Anything not on a page says **inferred**.

# Moxa ioLogik E2210

Smart Ethernet remote I/O with 12 digital inputs (dry or wet contact, NPN; DI or event counter, 900 Hz) and 8 sink digital outputs (200 mA a channel, DO or pulse mode) (datasheet pp. 2-3). Modbus TCP server (function codes 1, 2, 3, 4, 5, 6, 15, 16, datasheet p. 5), SNMP v1/v2c/v3, Click&Go control logic (up to 24 rules), one 10/100BaseT(X) port, configuration by ioAdmin or web console. Neither document lists EtherNet/IP. 

**Register map not read.** The datasheet gives channels and protocol only. The register map is in the ioLogik E2200 Series User's Manual (Appendix, "Modbus/TCP Address Mappings"), which moxa.com's product page does not link and whose one copy found (v7.1, a Moxa Russia host) the fetcher could not reach, so this folder has no `[[points]]` and no unit id. See `collect/moxa.toml`.

The documents are listed in `collect/` with their hashes; they are not in this repository.
