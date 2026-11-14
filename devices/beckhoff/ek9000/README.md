> **Draft from documents.** No unit has been checked; every value here is the
> manual's, with its page. Anything not on a page says **inferred**.

# Beckhoff EK9000

Bus coupler for EtherCAT terminals: an Modbus TCP/UDP server with no I/O of its own.

Register map from the manual's Modbus interface table (p. 49): inputs from 0x0000, outputs from 0x0800, image lengths at 0x1010-0x1013, the coupler answers 9000 at 0x6000. Its watchdog is on by default (1000 ms, outputs to zero), unlike the ioLogik's. The page does not say which function codes read which range; that wants a unit or the manual's examples.

## Sources

The manual is listed in [`collect/beckhoff.toml`](../../../collect/beckhoff.toml)
with its hash in [`collect/beckhoff.lock.json`](../../../collect/beckhoff.lock.json);
it is not in this repository.
