> **Draft from documents.** No unit has been checked; every value here is the
> documents', with its page. Anything not on a page says **inferred**.

# Schneider Electric TeSys island bus coupler TPRBCEIP

Point of connection between a TeSys island (motor starters, power, digital and analog I/O modules, up to 20 modules) and an automation controller: EtherNet/IP adapter and Modbus TCP server on two switched RJ45 fieldbus ports, 24 V DC, plus a service port with a web server (data sheet, p. 1).

Schneider does not publish a generic EDS for it. The island's data layout is generated from the island's configuration: the TeSys island DTM exports L5X files (Studio 5000 AOIs and a generic Ethernet module) for the configured island (Quick Start Guide p. 11). So the folder carries no identity or assembly sizes and no points; those belong to a configured island on a unit.

The documents are listed in `collect/` with their hashes; they are not in this repository.
