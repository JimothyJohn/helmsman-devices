> **Draft from documents.** No unit has been checked; every value here is the
> manual's, with its page. Anything not on a page says **inferred**.

# Siemens SENTRON PAC3200

Power monitoring device for three-phase networks. The Ethernet (RJ45) port speaks SEAbus TCP by default and Modbus TCP on port 502 once the protocol is switched on the device (Manual pp. 38-39). The manual's tables use function codes 0x03/0x04 for the measured variables (Table 3-6, pp. 40-41), and Read Device Identification (FC 0x2B) answers manufacturer, device name and firmware (p. 62).

Only four rows of the table are given as points here (voltage a-n, current a, frequency, total active power); the table has 100+ more, each a float over two registers. The manual read is the 12/2016 PDF whose own cover says 02/2008. Whether the offsets are one-based and the float word order are open questions in `device.toml`.

The manual is listed in `collect/siemens.toml` with its hash; it is not in this repository.
