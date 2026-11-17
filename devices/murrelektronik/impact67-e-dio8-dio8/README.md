# Murrelektronik IMPACT67 E DIO8 (DIO8) (art. no. 55089)

IP67 EtherNet/IP I/O block: 16 DIO (pin 4 and pin 2 of 8 M12 ports, each an input or an output, 1.6 A). Two Ethernet ports (M12 D-coded), power over 7/8".
EtherNet/IP adapter only: no Modbus.

**Checked on a unit on 2026-11-16** for its identity, its assemblies and its connection ("On the
bench" below). The meaning of each bit is still from the handbook alone: nothing was wired to the
unit, so no channel was seen switching. What the five articles share is in
[impact67-e-series.md](../impact67-e-series.md).

## Source

*Manual for the Devices of the IMPACT67 E Series, art. no. 55368, edition 1.8 (2019-06)*, 9631751 bytes, SHA-256 `f01edb0ad41cc1aa12de4984c68e1384afc3e6a6df38694401623be58d77c77f`. "p. N" is the handbook's page number. Nick's
copy; Murrelektronik's terms ("Copyright", p. 104) do not allow redistributing it here.

## The EDS

`55089_Impact67_E_DIO16.eds`, EDS revision 1.3 (modified 09-18-2017), 43 388 bytes, SHA-256
`6eb94568f8b5fc73420611ac1633073da2c6e8cda75d81593bd73631807bef3d`, from Murrelektronik's shop page for the article (a browser download; the page does not answer
a fetch). Not in this repository. It agrees with the unit and the handbook:

- Identity: vendor 640, device type 7 "General Purpose Discrete I/O", product code 55089, revision
  1.2, `IMPACT67 E DIO8 (DIO8)`: what the unit answered.
- Assemblies 5, 35, 105, 135 (2 bytes), 117 and 118 (8), 109 (3), 110 (0). It does not list 100 and
  101, which the unit also answers.
- Six connections: exclusive owner without and with diagnosis, each once with configuration
  instance 109 ("Config over EDS") and once with 110 ("Config over Web Server"), and two listen-only
  connections. Every owner is O->T run/idle, T->O modeless, point-to-point; no RPI is given.
- The three configuration parameters default to 0: pin mode, every channel an input.

There is a second file on the same page, `55089_Impact67_E_DIO16_Omron.eds` (regenerated 07-09-2019,
43 416 bytes, SHA-256 `2320dbc1dded11586c969412e8e0e11182c010325a598af4bd823fc4c1c1f225`). It differs in two things: assembly 109 has a fourth, reserved byte (the
unit reports 4 bytes for that instance), and the two channel parameters are USINT instead of BYTE.
Helmsman connected to the unit from either file (2026-11-17), with the file's defaults and with the
channel setup given as `config_data=` (3 bytes for the first file, 4 for the second). From an EDS
Helmsman opens the first exclusive owner, which is the one without diagnosis; the profile in this
folder opens the one with.

## The connection (pp. 73-75, 101)

| | instance | bytes |
| --- | --- | --- |
| input (T->O) | 117 | 8 |
| output (O->T) | 35 | 2 |
| configuration, as delivered ("Over EDS File") | 109 | 3 (the unit reports 4) |
| configuration, set to "Over Web Server" | 110 | 0 |

The profile's `enip-io` line: `config=109 o2t=35:2 t2o=117:8`, RPI 10 ms. With no configuration
data every channel of a block as delivered is an input. To make channels outputs the device line
carries the three configuration bytes as hex, `config_data=MMP4P2`:

| byte | |
| --- | --- |
| MM | bit 0: 0 pin mode, 1 port mode |
| P4 | pin 4 of port 0 (bit 0) .. port 7 (bit 7): 1 = output, 0 = input |
| P2 | pin 2 of port 0 (bit 0) .. port 7 (bit 7): 1 = output, 0 = input |

`config_data=00ff00` is pin mode with pin 4 of every port an output and pin 2 an input (pp. 62-63,
70). The controller sends it with every connection, so a block that is swapped or power-cycled gets
its setup again. `config_data=` needs a Helmsman with configuration data in `enip-io` (2026-11-16
or later).

## On the bench (2026-11-16)

One unit as it came out of its box: 24 V on US and UA, one Ethernet cable, nothing on its ports, an
address from DHCP. `scripts/enip-identify.py` and a Class 1 connection from Helmsman's `enip-io`.

```toml
[identity.enip]
vendor_id = 640
device_type = 7
product_code = 55089
revision = '1.2'
status = '0x0030'
product_name = 'IMPACT67 E DIO8 (DIO8)'
```

- **Assemblies that answer** (attribute 3): 5, 35, 100, 101, 105, 135 with 2 bytes; 117 and 118
  with 8; 110 with none; 109 with 4, of which the fourth read 0. Instances 100 and 101 are not in the
  handbook's tables for this article.
- **As delivered it is in "Over EDS File" mode.** A `Forward_Open` with configuration instance 110
  is refused: general status 0x01, extended status 0x0119, then sixteen more status words (two
  zeros, fourteen 0x5555). With 109, with or without data, or with no configuration segment, it
  opens. Three bytes of configuration (padded to four on the wire) read back in instance 109.
- **O->T** is 2 bytes behind a 32-bit run/idle header (without the header: refused 0x0127).
  **T->O** is 8 bytes with no header (0x0128 otherwise). Point-to-point both ways.
- **RPI 10 ms**: a packet every 10 ms (median gap 9.8 to 10.2 ms, 99th percentile 12 to 14 ms over
  300 packets, none lost), the first one 10 to 11 ms after the `Forward_Open`. Twenty minutes at
  10 ms with one output toggled twice a second: 120 000 reads, one connection, the link never lost.
- **Inputs go to UDP 2222 only**: a T->O socket-address item naming another port is ignored.
- **An output channel does not read back as an input**: with pin 4 of port 0 an output and on,
  input bit 0.0 stayed 0.
- **After a `Forward_Close` the output assembly (35) still read the last values written.** Whether
  the pins stay on was not seen.

Not run: any input changed by hand, any output watched, the diagnosis bits (all read 0 with no
load and both supplies on), a pulled cable, port mode, RPIs other than 10 ms.

## Input assembly 117

| byte | bits |
| --- | --- |
| 0 | input channel 00 (port 0, pin 4, bit 0) .. 07 (port 7, pin 4, bit 7) |
| 1 | input channel 10 (port 0, pin 2, bit 0) .. 17 (port 7, pin 2, bit 7) |
| 2 | bit 1 no actuator voltage, bit 2 sensor supply undervoltage, bit 3 actuator supply undervoltage |
| 3 | sensor short-circuit, port 0 (bit 0) .. port 7 (bit 7) |
| 4 | actuator overload, channel 00 .. 07 |
| 5 | actuator overload, channel 10 .. 17 |
| 6 | actuator warning, channel 00 .. 07 |
| 7 | actuator warning, channel 10 .. 17 |

## Output assembly 35

| byte | bits |
| --- | --- |
| 0 | output channel 00 (port 0, pin 4, bit 0) .. 07 (port 7, pin 4, bit 7) |
| 1 | output channel 10 (port 0, pin 2, bit 0) .. 17 (port 7, pin 2, bit 7) |

Channel numbers are Murrelektronik's: 00..07 are pin 4 of M12 ports 0..7, 10..17 pin 2 of the
same ports. Bit 0 of a byte is the lowest channel of that byte.

## Notes

- **Four connections** (p. 69): 1 "Exclusive Owner w/o Diags" (input 5, 2 bytes), 2 "Exclusive Owner w/ Diags" (input 117, 8 bytes), 3 "Listen Only w/o Diags" (input 105, 2 bytes), 4 "Listen Only w/ Diags" (input 118, 8 bytes). Output 35 (2 bytes) for the owners, 135 (2 reserved bytes) for the listeners. A listen-only connection "may only be established if the Connection1 or Connection2 have already been established". The profile uses connection 2: the diagnosis costs six bytes a cycle.
- **Two parameterization modes** (web server, "Properties", p. 43). "Over Web Server": each channel's function is set and saved to flash in the web server (pp. 48-51), and the configuration instance is 110 of 0 bytes. "Over EDS File": the controller sends the functions in configuration instance 109 (3 bytes: pin/port mode, pin 4 functions, pin 2 functions, pp. 62-63, 70). The unit on the bench was in **Over EDS File** as delivered, which is what the profile is written for; a block someone has switched to Over Web Server needs `config=110` on its device line instead.
- **Pin mode or port mode** changes the bit layout (pp. 71-75): pin mode puts pin 4's eight channels in byte 0 and pin 2's in byte 1; port mode interleaves them by port (byte 0: 00, 10, 01, 11, ...). The profile is written for **pin mode**. Set it in the web server, "Port/Pin Configuration" (p. 49).
- Device Level Ring from software version 1.01 (p. 81).

## Inferred

- What each bit means on a unit: every assembly table here is the handbook's.
- What the outputs do when the controller is lost. The handbook shows the network LED flashing red when "at least one connection has timeout" (p. 83) and nothing about the outputs. Expect them off; the bench decides.
- The 1 s RPI ceiling in `cycle_ms`: the handbook gives no maximum.

## Files

- [`murrelektronik-impact67-e-dio8-dio8.device`](murrelektronik-impact67-e-dio8-dio8.device): the profile a controller copies into a project.
- [`enip.map`](enip.map): the same channels as `enip-io` map lines, `ADDR` to fill in.
- [`device.toml`](device.toml): the record a lookup matches.

## Still to check on a unit

- Every channel once, with something wired: an input bridged, an output watched.
- A pulled cable and a closed connection, to see what the outputs do.
