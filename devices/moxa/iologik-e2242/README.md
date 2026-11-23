> **Draft from documents.** No unit has been checked; every value here is the
> document's, with its page. Anything not on a page says **inferred**.

# Moxa ioLogik E2242

Smart Ethernet remote I/O with 4 differential 16-bit analog inputs (voltage or current, up to +/-10 V and 0 to 20 mA) and 12 software-configurable DIO channels (datasheet pp. 2-4). Modbus TCP server (function codes 1, 2, 3, 4, 5, 6, 15, 16, datasheet p. 5), SNMP v1/v2c/v3, Click&Go control logic (up to 24 rules), one 10/100BaseT(X) port, configuration by ioAdmin or web console. Neither document lists EtherNet/IP. 

**Points.** The `[[points]]` are read from the Modbus/TCP Address Mappings appendix of the ioLogik E2200 Series User's Manual, v7.2 (2022-08-08), which Moxa lists on its support page for the series (`collect/moxa.toml`). Each point's `source` gives the page (the PDF's page numbers are the manual's own). No unit has confirmed any of them. Counter values as one 32-bit number (high word first) and the other places marked **inferred** are readings, not statements of the table. The manual gives no Modbus unit id (see the `[[questions]]`), so the folder names none. Only the points a project would map are listed (inputs, outputs, counters, modes and, on the E2242, the analog inputs); the table also holds power-on and safe-mode values, pulse and trigger settings, the Click&Go internal registers and system information words, which are not.

The documents are listed in `collect/` with their hashes; they are not in this repository.
