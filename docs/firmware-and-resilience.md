# Firmware, versions and resilience: a plan

What one benched E1213 and the ioLogik family's documents have taught so far,
and what the library and the box should do about it. Each step below is one
PR, in the order given. The first three are this repository; the rest are
helmsman's, and become cards on its board.

## What we have seen

1. **A device's behaviour changes with its firmware, silently.** The E1213 at
   3.1 names UDP 5222 for O->T data in its `Forward_Open` reply and ignores
   O->T sent to 2222. Release 3.2 sends to 2222 "by default". Two units of
   one model, one wire protocol, two behaviours. The box survives it only
   because its scanner honours the reply's socket-address item.
2. **A register can change meaning between releases.** The E1241's AO scaled
   value is input register 0 up to 3.2 and holding register 0 from 3.3. One
   request reads the value on one unit and fails, or reads something else,
   on another. A profile today cannot say "this point from firmware 3.3".
3. **An update can make a device disappear.** Firmware 4.0 turns EtherNet/IP
   off by default. A unit updated in the field stops answering
   `ListIdentity` and refuses `Forward_Open`. The box falls back to Modbus
   (the profile's second transport) but nothing tells anyone why.
4. **The vendor's files lag or lead the device.** The E1213's EDS v2.0
   describes revision 4.1. The bench unit reports 3.1. `key=exact` would
   refuse a working device. The E1212's only readable EDS is from 2017
   (revision 2.6), and its Input Only path differs from the E1213's.
5. **Updates are a procedure, not an action.** "Update only the next or the
   previous released firmware version" (release notes from 3.0): 3.1 to 4.0
   is four flashes, each with a reboot, and the last one undoes the
   EtherNet/IP setting.
6. **The safe state is off out of the box.** The ioLogik's communication
   watchdog is disabled by default (Appendix E), so a unit whose controller
   vanishes holds its outputs. Nothing on the box knows whether a given unit
   has it on.
7. **Ownership is scarce.** The E1213 at 3.1 grants one Class 1 connection of
   any kind. A second controller (the try box, the P4 node) turns into a
   refused `Forward_Open`, and an owner that vanishes holds the unit for
   about 10 s.
8. **The library cannot tell checked facts from read ones yet**, except by
   prose. Nine of ten ioLogik folders are read from documents only.

## The plan

### In this repository

**1. Firmware in `device.toml`** (schema, `build-index.py`, the ten ioLogik
folders). A `[[firmware]]` table per release that matters, from the release
notes, with what a controller sees:

```toml
[[firmware]]
version = "3.2"
build = "Build20111915"
date = "2020-12-25"
changes = ["o_to_t_port: 2222 (before: the port the Forward_Open reply names)"]
source = "release notes p. 4"

[[firmware]]
version = "4.0"
changes = ["enip_default: off"]
```

and `[[checked]]` replacing the flat `checked_on` / `firmware` /
`checked_by`: one entry per bench run, with the firmware it ran on, so a
fact is "checked on 3.1" and not just "checked". `build-index.py` carries the
firmware versions and the newest checked one into `index.json`; a box can
then say "this library entry was checked on 3.1, your unit runs 4.0".

**2. A content hash per profile in `index.json`** (`profile_sha256`). A
project holds a copy of the profile (decided 2026-11-11: updates offered,
never applied). The box compares its copy's hash with the library's to
offer an update, and names the library commit it came from. No profile
version numbers to keep by hand; the hash is the version.

**3. CI holds every profile to the box's own rules.** Today `build-index.py`
checks a profile's first line only. The checks that matter are helmsman's
`Profile::parse` and the map validator: they passed for all ten folders
here, but only from a one-off test in a helmsman checkout. A CI job that
checks out helmsman at `dev`, runs that test against this tree, and fails
the PR otherwise. The job pins helmsman by commit and Dependabot-style bumps
it, so a format change in helmsman reaches this repo as a red PR, not a
broken box.

### In helmsman (cards)

**4. Read the firmware at connect.** The box already reads the identity it
resolves a device by. Add the firmware: `ListIdentity`'s revision, or for a
Modbus-only unit the profile's own identity registers (a new profile line,
`firmware modbus-tcp=ir:5029:u32`, the E1200's `firmwareVersion`). Shown in
the device's details, written into the event log when it changes between
two connects ("iologik_e1213: firmware 3.1 -> 3.2"), and compared with the
library's checked firmware.

**5. Firmware-dependent points in a profile** (`helmsman-device 2`, or an
option `fw=3.3..` on a channel's point). A channel may give a point per
firmware range: `out AO-00-scaled real modbus-tcp=ir:0:f32@..3.2
modbus-tcp=hr:0:f32@3.3..`. The box picks by the firmware read in step 4
and refuses the channel, as a point error naming both, when it cannot read
the firmware. Until this lands, a firmware-dependent register stays out of
the profile, as the E1241's scaled value does.

**6. Say why a transport fell back.** When `ProfileDriver` moves from
EtherNet/IP to Modbus, the reason goes to the device's details and the event
log in words: "EtherNet/IP is off on the unit (firmware 4.0 ships with it
off; switch it on in its web console)" for a unit that answers Modbus and
not `ListIdentity`; "another controller owns the unit's one connection"
for extended status 0x0100. The library's `[[firmware]]` changes give the
text.

**7. Commissioning check: the safe state.** A profile may say how the device
protects itself when the box is lost and how to read whether that is on:
`watchdog modbus-tcp=...`. Adding a device runs the check once; a device
whose outputs would hold says so on its row ("holds its outputs if this box
stops: its watchdog is off"). Writing the device's own configuration stays
out of scope: the box reads, the engineer sets it in the vendor's console.

**8. Configuration snapshots.** The ioLogik exports its whole configuration
as a text file (manual p. 3-29). A project file kind for a device's exported
configuration, kept beside its profile and diffed like any other project
file, so a replaced unit is set up from the project, and a changed one shows
as a diff. Import stays the vendor's tool.

**9. A firmware update is a scripted, verified procedure** (the
`e1213-firmware-update` card is the first use). One script per step,
idempotent: export the configuration, flash the next release only, wait for
the unit, read back model, firmware and build, re-enable what the release
turns off (EtherNet/IP after 4.0), rerun the bench probes, append a
`[[checked]]` entry. A failed read-back stops the chain. The box never
flashes a third-party device on its own.

### Bench evidence, for every step

Each change of a device's firmware on the bench reruns the same probes
(`scratch/enip-fo-probe.py`, `enip-hold-probe.py`, the Modbus loop) and
lands its results in the folder, so the library's claims carry the firmware
they were seen on. The E1213 update (3.1 to 4.0, four steps) is the first
run, and checks the release notes' claims about the O->T port, the second
input-only session and EtherNet/IP's default.

## Not in this plan

- Hosting vendor firmware or EDS files: neither carries redistribution
  terms. Folders give a name, size, hash and where to download.
- Rolling a device back automatically. A downgrade is the same one-step
  procedure in reverse, run by a person.
- Our own devices' firmware (the edge node): A/B slots and rollback on an
  unconfirmed boot are helmsman's `node-ota` card.
