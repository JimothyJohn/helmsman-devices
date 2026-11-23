> **Draft from documents.** No unit has been checked; every value here is the
> manual's, with its page. Anything not on a page says **inferred**.

# Siemens SINAMICS G120 CU240E-2 PN, EtherNet/IP mode

The CU240E-2 PN control unit has two RJ45 ports (X150 P1/P2) and speaks PROFINET, and EtherNet/IP when switched to it (Fieldbus Function Manual, section 4.1 table and section 4.2). The drive profile is chosen with p8980: 0 is the SINAMICS profile (factory setting), 1 is the ODVA AC/DC profile, for which the standard telegram p0922 = 1 is used (p. 66).

The manual lists the required ODVA assemblies 20 (output) and 70 (input), four bytes each, and optional 21-25 / 71-75 (pp. 67-68); the two required ones are written as points. Siemens' EDS is named in the manual but sits behind a JavaScript portal page, so no EDS is collected and there is no `[identity.enip]`.

The manual read is the 04/2014 edition for firmware V4.7; a unit on newer firmware may differ.

The manual is listed in `collect/siemens.toml` with its hash; it is not in this repository.
