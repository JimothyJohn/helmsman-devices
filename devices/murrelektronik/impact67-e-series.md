# Murrelektronik IMPACT67 E series (EtherNet/IP)

Five IP67 I/O blocks under one handbook. Each has a folder; none has been
on the bench yet. Which article the bench block is will be known from its
label or its first `ListIdentity` answer.

| article | model | channels | input / output / config instance, bytes | folder |
| --- | --- | --- | --- | --- |
| 55085 | IMPACT67 E DI16 | 16 DI | 100: 4, 112: 2, 128: 0 | [impact67-e-di16](impact67-e-di16/README.md) |
| 55086 | IMPACT67 E DI8 DO8 | 8 DI, 8 DO (2 A) | 100: 4, 112: 2, 128: 0 | [impact67-e-di8-do8](impact67-e-di8-do8/README.md) |
| 55087 | IMPACT67 E DO8 | 8 DO (2 A) | 100: 2, 112: 2, 128: 0 | [impact67-e-do8](impact67-e-do8/README.md) |
| 55088 | IMPACT67 E DO16 | 16 DO (0.5 A) | 100: 4, 112: 2, 128: 0 | [impact67-e-do16](impact67-e-do16/README.md) |
| 55089 | IMPACT67 E DIO8 (DIO8) | 16 DIO (1.6 A) | 117: 8, 35: 2, 110: 0 | [impact67-e-dio8-dio8](impact67-e-dio8-dio8/README.md) |

Sizes are the "Always Even I/O Length" mode for 55085..55088 (each folder
says why).

## Source

*Manual for the Devices of the IMPACT67 E Series*, art. no. 55368, edition
1.8, 2019-06, 9 631 751 bytes, SHA-256
`f01edb0ad41cc1aa12de4984c68e1384afc3e6a6df38694401623be58d77c77f`. Not in
this repository ("Copyright", p. 104).

## The same on every article

- **Vendor ID 640** (technical data, pp. 93-101). The product codes are not
  in the handbook. The 55089's EDS file is named `02800007D7310101.eds`
  (p. 45), which reads as vendor 0x0280 = 640, device type 7, product code
  0xD731 = 55089, revision 1.1. If the others follow the pattern, each product
  code is its article number. That is inferred, so only the 55089's folder
  records it.
- **EtherNet/IP only.** Two M12 D-coded ports through an internal switch;
  power over 7/8" (US for the module and sensors, UA for the actuators,
  18-30 V, 9 A a connector; pp. 24-26).
- **RPI**: at least 5 ms, 10 ms by default, and anything under 10 ms "must first
  be tested" (pp. 21, 58). The controller drops the connection after four
  RPIs without data (p. 21). The profiles ask 10 ms and let the box go up to
  1 s; the handbook gives no maximum.
- **Addressing** by three rotary switches, read once at power-up (pp. 35-38):
  000 DHCP/BOOTP without saving (the default), 001-254 the last byte of
  192.168.100.xxx, 255-996 DHCP/BOOTP with saving, 998 factory reset,
  999 the saved static address (default 192.168.100.6). DHCP and BOOTP
  are asked only in the first 60 s after power-up (p. 38).
- **Diagnostics in the input data**: US and UA undervoltage (below 18 V),
  sensor supply short-circuit, actuator overload (p. 92). Below 13.5 V on UA
  every output is off (p. 89).
- **An overloaded output stays off** until the controller writes it 0 and
  then 1, or UA is cycled (pp. 33, 91). A box program that holds an output at
  1 will not bring it back after a short. The program has to drop it.
- **A web server** on every unit: article and software version ("Help ->
  Version Info", p. 46), I/O lengths, an I/O check. Outputs cannot be set from
  it while a controller holds the connection (p. 52).
- **Not said anywhere**: what the outputs do when the connection times out.
  The NS LED flashes red (p. 83). This is the first thing to check on the
  bench.

## Bring-up, in order

1. **Find it.** Power it with the rotary switches at 000 and a DHCP server on
   the device link, or set 001-254 and give this Mac an address on
   192.168.100.0/24 (a `scratch/` hand-off with `sudo ifconfig en0 alias`; the
   Mac already carries 192.168.127.10 for the Moxa default). Then from a
   session: `/usr/bin/python3 -I scripts/enip-list.py` (a ListIdentity
   sweep, as the box's Scan does).
2. **Ask it.** `/usr/bin/python3 -I scripts/enip-identify.py IP 100 112 128 5 35 117`
   prints vendor, type, product code, revision, product name and the size of
   each assembly. Read-only. Correct the folder's `identity.enip` and sizes
   from it.
3. **Set it up in its web server** (55089 only): parameterization "Over Web
   Server", pin mode, each channel's function, saved to flash (pp. 43-51).
4. **Run the exclusive owner** with helmsman's conformance harness, the
   folder's `enip-io` line as params, for example for a DI8 DO8 with output 00
   wired to input 00:
   `cargo run -p helmsman-io --example conformance -- --enip IP --param config=128
   --param o2t=112:2 --param t2o=100:4 --param rpi_ms=10 --loop out:0.0=in:0.0`.
   On macOS the binary needs the firewall exception first (helmsman's
   `scratch/02-allow-firewall.sh`).
5. **Pull the cable** with an output on and record what it does. Then
   overload one output, check that it stays off, and check that 0 and then 1
   brings it back.
6. Each folder gets `checked_on`, `firmware` (the web server's software
   version) and what the bench showed. A second EtherNet/IP unit on the bench
   also ends the contention for the E1213's single connection (helmsman card
   `murr-block-bringup`).
