# Helmsman device library

Devices mapped once, for everyone who runs them with Helmsman. One folder
per device: how to reach it, what its points mean, where each fact comes
from. A controller or its agent looks a device up here before working the
mapping out from a manual.

## Layout

```
devices/<vendor>/<model>/
  device.toml     identity, protocols, settings, points, sources
  enip.map        the I/O map lines for EtherNet/IP (if the device speaks it)
  modbus.map      the I/O map lines for Modbus TCP (if it does)
  README.md       the device in words, with the manual's page for each claim
  record.json     a wired sensor's or actuator's facts as JSON, built from device.toml
```

A family that shares a manual and a firmware line gets a page beside its
folders (`devices/moxa/iologik-e1200-series.md`). A folder whose facts
nobody has checked on a unit has no `checked_on` and says so at the top of
its README. How firmware and versions are to be handled is planned in
[`docs/firmware-and-resilience.md`](docs/firmware-and-resilience.md).

`device.toml` is the record a lookup matches: first by what the wire gives
(an EtherNet/IP vendor id and product code from ListIdentity, a Modbus
unit's identification), then by vendor and model text. See
[`docs/device-toml.md`](docs/device-toml.md).

## Vendor files

Vendor files (an EDS, a manual) are not committed unless their terms allow
redistribution. A folder gives the file's name, size and SHA-256 and where
to download it; a controller with the file at hand checks the hash before
trusting it. `*.eds` and `*.pdf` are ignored here on purpose.

## Collecting documents

[`collect/`](collect/README.md) records where each vendor file comes from
and what was fetched: `scripts/docs-fetch.py` downloads the files a
`collect/<vendor>.toml` names (https only, public addresses only,
robots.txt honoured, every file's type and hash checked) into an ignored
`cache/`, and `scripts/eds-draft.py` drafts a folder's `device.toml` from
an EDS. `scripts/iodd-draft.py` does the same for a sensor or an actuator
from its IODD (the description file every IO-Link device has): who makes
it, its variants, how each connector is wired and what its signals are
called, for a device that sits on a plain digital channel
([`docs/device-toml.md`](docs/device-toml.md)). In Claude Code, the `collect-docs` skill runs the whole loop,
searching for the files included.

## Contributing

Open a pull request with one folder. Say which unit and firmware you
checked the facts on; mark anything inferred as inferred. An agent working
for someone with a device on their network follows [`AGENTS.md`](AGENTS.md):
identify the unit, draft or look up its entry, test it against the unit,
send the pull request. Metadata and map
lines in this repository are MIT licensed; the vendors' files keep their
own terms.

## First publish

`scripts/create-github-repo.sh` makes the first commit if there is none,
creates the public repository `JimothyJohn/helmsman-devices` and pushes
`main` and `dev`.
