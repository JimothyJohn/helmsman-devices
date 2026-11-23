> **Draft from documents.** No unit has been checked; every value here is the
> document's, with its page. Anything not on a page says **inferred**.

# Moxa ioThinx 4510

Modular remote I/O adapter (4510, and 4510-T for -40 to 75 degC) with two RJ45 Ethernet ports, one serial port (RS-232/422 or 2 x RS-485) running a Modbus RTU master, and up to 32 ioThinx 45MR modules (manual ch. 2, Technical Data). Modbus TCP server, function codes 1, 2, 3, 4, up to 7 connections. Also SNMP, MQTT and a RESTful API. Neither document lists EtherNet/IP.

The adapter has no fixed I/O map: the Modbus addresses are generated for the modules fitted and can be edited on its web console (manual "Configuring Modbus Address Settings"). The points here are the parameter names and lengths of the manual's Modbus/TCP Slave Rules (Appendix A, pp. 111-), not addresses; a unit must show the default address of each.

The documents are listed in `collect/` with their hashes; they are not in this repository.
