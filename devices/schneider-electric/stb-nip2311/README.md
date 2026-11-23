> **Draft from documents.** No unit has been checked; every value here is the
> manual's, with its page. Anything not on a page says **inferred**.

# Schneider Electric Modicon STB NIP2311

Standard dual-port Ethernet network interface module of the Advantys STB island. It speaks Modbus TCP on port 502 and is the whole gateway to the island's I/O: the register map is the island's *process image*, whose layout depends on which STB modules are plugged in (the guide's example uses 40001 for the first output register and 45392 for the first input register).

Schneider publishes no EDS for it (the module is Modbus TCP, not EtherNet/IP; the se.com download page for it lists firmware only), so there is no `[identity.enip]`. Read Device Identification support is not stated in the pages read, so there is no `[identity.modbus]` either.

The firmware download page (https://www.se.com/uk/en/download/document/STBNIP2311_Exec_Firmware/) lists SV05.21 as the latest; the guide read is revision .05 (10/2019). What a unit reports under that firmware is for a unit to settle.

The manual is listed in `collect/` with its hash; it is not in this repository.
