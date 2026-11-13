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
```

Everything a lookup matches on is under `identity`; everything a map needs
is under `protocols`; everything a person wants to read is in the
folder's README. A field nobody has checked is left out, not guessed.
