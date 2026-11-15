# device.toml

One file per device. Keys and what a lookup does with them.

```toml
[device]
vendor = "Moxa"                 # text, for a search
model = "ioLogik E1213"         # text, for a search
kind = "remote-io"              # remote-io | drive | controller | sensor | other
checked_on = "2026-11-02"       # the date the facts were last checked on a unit
firmware = "V3.1 Build19110615" # the firmware they were checked against
profile = "moxa-iologik-e1213.device"  # the device profile in this folder (helmsman-device 1): a controller copies it into a project when the device is added

[identity.enip]                 # ListIdentity, the first key a lookup tries
vendor_id = 991
product_code = 515
device_type = 12
revisions = ["3.1", "4.1"]      # the ones known to match this record

[identity.modbus]               # Read Device Identification (FC 43/14) when the device answers it
vendor_name = "Moxa"
product_code = "E1213"

[protocols.enip]
driver = "enip-io"              # the Helmsman driver
map = "enip.map"                # the map lines to append, with ADDR to fill in
profile = "moxa-e1213"          # a built-in profile, if Helmsman has one
eds = { name = "...", size = 42906, sha256 = "...", url = "..." }   # the vendor's file, by reference

[protocols.modbus]
driver = "modbus-tcp"
map = "modbus.map"
unit = 1

[[points]]                      # what the bytes and registers mean, one per channel group
name = "DI-00..DI-11"
enip = "in:0.0..in:1.3"         # Helmsman point syntax
modbus = "di:0..di:11"
meaning = "digital input state, 1 = on"
source = "E1200 manual v15.10 p. B-1; bench 2026-11-02"

[[sources]]
title = "ioLogik E1200 Series User's Manual, Version 15.10"
sha256 = "..."
where = "..."

[[questions]]                   # what the documents leave open or contradict; a unit settles it
ask = "Which coil switches the first output: 0x0000, as the table says, or 0x0001, as the example writes?"
source = "Modbus TCP Manual p. 7 (the table) and p. 8 (the example)"
```

A `[[questions]]` entry is removed in the change that answers it, and the
answer goes where it belongs (a point, an assembly) with the unit and
firmware it was seen on.

Everything a lookup matches on is under `identity`; everything a map needs
is under `protocols`; everything a person wants to read is in the
folder's README. A field nobody has checked is left out, not guessed.

## A sensor or actuator on a digital channel

A proximity switch, a photo eye or a valve is not reached over a network:
one of its wires goes to a digital input or output of a remote I/O block,
and the block's record covers the address. What the library holds for such
a device is what it is and what its signals mean. Most of them are also
IO-Link devices, and every IO-Link device has a description file from its
vendor, the IODD. The library reads the IODD for the device's metadata
whether or not IO-Link is ever spoken to it. `scripts/iodd-draft.py`
drafts the record from the IODD; it has no `protocols` table.

```toml
[device]
vendor = "..."                  # the IODD's vendorName
model = "..."                   # its DeviceName
kind = "sensor"                 # sensor | actuator | other: inputs make a sensor, outputs alone an actuator
family = "..."                  # its DeviceFamily
vendor_url = "..."

[identity.iolink]               # what the device answers on an IO-Link port; how the record is found from an IODD
vendor_id = 310
device_id = 666

[[variants]]                    # the order numbers the one IODD covers
product_id = "..."
name = "..."
description = "..."

[wired]                         # the device with no IO-Link master
sio = true                      # it switches its C/Q wire on its own
switching = "Switching signal 1"   # which signal that wire carries: from the manual, never from the IODD
source = "manual, p. 12"

[[wired.connections]]           # one per connector or cable the variants have
type = "M12-4"                  # M5 | M8 | M12-4 | M12-5 | Cable | Other
products = ["..."]
wires = [
  { n = 1, function = "L+", color = "BN" },
  { n = 2, function = "Other", color = "WH", name = "Q2 (second switching output)" },
  { n = 3, function = "L-", color = "BU" },
  { n = 4, function = "C/Q", color = "BK" },
]

[[signals]]                     # as the device names them over IO-Link
dir = "in"
name = "Switching signal 1"
type = "bool"                   # bool | int | uint | float32 | string | octets | time | timespan
bits = "0"                      # in its IO-Link process data, counted from the last octet's lowest bit
off = "No target"               # what each state is called, when the IODD says
on = "Target present"
description = "..."

[[settings]]                    # a parameter that is a choice, with the value it leaves the factory with
name = "SSC1 Config: Logic"     # a record's item is "record: item"
index = 61                      # where it is on the device, for a tool that can set it
subindex = 1
default = "0"
default_name = "High active"
values = { 0 = "High active", 1 = "Low active" }

[iodd]
file = { name = "...", size = 123456, sha256 = "...", url = "https://..." }
version = "V1.2"
date = "2026-11-14"
profile_characteristic = [1, 32768, 32769]   # the profiles and function classes the device declares
```

`settings` holds only choices: a boolean, or a number whose values have
names, that is read-write and has a default in the IODD. They are what a
sensor does as delivered: whether its output is PNP or NPN, whether a
switching signal is high or low when a target is there, what the second
pin does. A setpoint or a delay is a number someone sets and is not
listed. On the standard connectors (M5, M8, M12 with 4 or 5 poles) wire 1
is L+ (brown), wire 3 is L- (blue) and wire 4 is C/Q (black) by the IODD
schema, so the draft fills them in when the file leaves them bare.

An IODD says how the device is wired and what its signals are called. It
does not say which signal the switching wire carries when no master is
connected, or whether the output is normally open: `wired.switching`
stays out of a draft until someone has read it in the manual and given
the page. The Smart Sensor Profile leaves it open too: "While the Device
is used in SIO the physical output on C/Q may represent the activity
state of the switching signal SSC1. The behavior of the sensor in SIO
mode is not scope of this standard." (IO-Link Smart Sensor Profile
V1.2.1, order no. 10.042, p. 59-60.) The index carries `identity.iolink`
beside `identity.enip`, and the variants' order numbers as `products`,
so a search by the number on the label finds the record.

The IODD comes from IODDfinder (https://ioddfinder.io-link.com), as a
`kind = "archive"` entry in `collect/<vendor>.toml`; the record's
`iodd.file` is the description inside that zip, with its own hash.
