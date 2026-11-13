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

## Contributing

Open a pull request with one folder. Say which unit and firmware you
checked the facts on; mark anything inferred as inferred. Metadata and map
lines in this repository are MIT licensed; the vendors' files keep their
own terms.

## First publish

`scripts/create-github-repo.sh` makes the first commit if there is none,
creates the public repository `JimothyJohn/helmsman-devices` and pushes
`main` and `dev`.
