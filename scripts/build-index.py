#!/usr/bin/env python3 -I
"""Build index.json and CATALOG.md from every devices/<vendor>/<model>/device.toml.

The index is what a Helmsman controller (or its canvas) fetches to look a
device up before anything is generated: identity first (ListIdentity's
vendor id and product code), then vendor and model text. Format
"helmsman-devices-index 1"; a controller refuses anything else.

CATALOG.md is the same devices as a list a person or an agent reads: one
table per category, each row with what the folder gives a project. It is
written here so that one command keeps both files true.

Usage: python3 -I scripts/build-index.py [--check]
  --check   exit 1 if index.json or CATALOG.md differs from what the folders say (CI)

Standard library only (tomllib needs Python 3.11).
"""

import datetime
import json
import pathlib
import re
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORMAT = "helmsman-devices-index 1"
TEXT_MAX = 120
URL_MAX = 400
# Characters a photo link never needs and an attribute must not see. A page sets
# it as img.src, never inside CSS url(), so a vendor's "Photo(Main)" path stays.
URL_BANNED = set(" \"'<>\\`{}|^")

# [device] category: the shelf a device is listed on in CATALOG.md and what
# scripts/find.py and a page filter by. Finer than kind, which is what a box
# reads: most of the library is kind "remote-io". Id, heading, what is in it.
CATEGORIES = (
    ("io-block", "I/O blocks (on the machine)", "Fixed channels in one sealed housing with M12 ports."),
    (
        "panel-io",
        "I/O modules (in the cabinet)",
        "Fixed channels in one module with terminals, on a DIN rail.",
    ),
    (
        "io-coupler",
        "Modular I/O couplers",
        "The head of a row of I/O slices or modules; the channels depend on what is fitted.",
    ),
    ("iolink-master", "IO-Link masters", "Ports that speak IO-Link to sensors and actuators."),
    (
        "valve-terminal",
        "Valve terminals",
        "Pneumatic valve manifolds and their bus nodes; an output switches a solenoid.",
    ),
    ("drive", "Drives", "Frequency inverters, servo drives and their network option cards."),
    (
        "motor-starter",
        "Motor starters and protection",
        "Starters, soft starters and motor management relays.",
    ),
    ("power-meter", "Power meters", "Meters that give voltage, current, power and energy."),
    ("vision", "Vision sensors and code readers", "Cameras that inspect, and readers of 1D and 2D codes."),
    ("robot", "Robots", "Robot controllers, as a device another controller reads and commands."),
    ("controller", "Controllers", "Programmable controllers that also answer as a device."),
    (
        "sensor",
        "Sensors and actuators on a digital channel",
        "Wired to a point of an I/O block, not on the network; described from the IODD.",
    ),
    ("other", "Other", "On the network, and none of the above."),
)
# A folder that names no category: drafts start here, so the list shows what is left to sort.
UNSORTED = ("unsorted", "Not yet sorted", "A draft with no category in its device.toml yet.")
CATEGORY_IDS = {c[0] for c in CATEGORIES}
PROTOCOL_NAMES = {"enip": "EtherNet/IP", "modbus": "Modbus TCP"}


def text(v, what):
    if not isinstance(v, str) or not v or len(v) > TEXT_MAX or any(ord(c) < 32 for c in v):
        raise SystemExit(f"{what}: text of 1..{TEXT_MAX} printable characters, got {v!r}")
    return v


# The file names a box takes (helmsman-project devlib `file_ok`, at most
# MAX_TEXT = 120 bytes): one it refuses takes the whole index off every box,
# as an EDS named with spaces did on 2026-11-18. Spaces become underscores
# (scripts/eds-draft.py does that for a vendor's name).
FILE_NAME = re.compile(r"[A-Za-z0-9._-]{1,120}")


def file_name(v, what):
    s = text(v, what)
    if not FILE_NAME.fullmatch(s) or s in (".", ".."):
        raise SystemExit(
            f"{what}: {s!r} is not a file name a box reads (letters, digits, '.', '_' and '-'; "
            "use _ for a space)"
        )
    return s


def date(v, what):
    """A YYYY-MM-DD date, as text, from a TOML date or a string."""
    if isinstance(v, datetime.date) and not isinstance(v, datetime.datetime):
        return v.isoformat()
    if isinstance(v, str) and len(v) == 10:
        try:
            return datetime.date.fromisoformat(v).isoformat()
        except ValueError:
            pass
    raise SystemExit(f"{what}: a date YYYY-MM-DD, got {v!r}")


def link(v, what):
    """An https link a page puts in an attribute: no spaces, quotes or brackets."""
    if (
        not isinstance(v, str)
        or not v.startswith("https://")
        or len(v) > URL_MAX
        or any(ord(c) < 33 or ord(c) > 126 or c in URL_BANNED for c in v)
        or not v[len("https://") :].split("/", 1)[0]
    ):
        raise SystemExit(
            f"{what}: an https:// link of at most {URL_MAX} printable ASCII characters, got {v!r}"
        )
    return v


def photo(v, rel):
    """[device.photo]: the vendor's own picture, linked and never stored here."""
    if not isinstance(v, dict):
        raise SystemExit(f"{rel}: device.photo: a table with url, page and seen")
    date(v.get("seen"), f"{rel}: device.photo.seen")
    return {
        "url": link(v.get("url"), f"{rel}: device.photo.url"),
        "page": link(v.get("page"), f"{rel}: device.photo.page"),
    }


def category(dev, t, rel):
    """[device] category, one of CATEGORIES. A folder without one is a wired
    sensor or actuator (no protocols, kind says so) or not yet sorted."""
    cat = dev.get("category")
    if cat is None:
        wired = not t.get("protocols") and dev.get("kind") in ("sensor", "actuator")
        return "sensor" if wired else UNSORTED[0]
    if cat not in CATEGORY_IDS:
        raise SystemExit(f"{rel}: device.category: one of {', '.join(c[0] for c in CATEGORIES)}; got {cat!r}")
    return cat


def gives(folder: pathlib.Path, e: dict) -> str:
    """What the folder gives a project, best first: the catalog's "to use it" column."""
    t = tomllib.loads((folder / "device.toml").read_text())
    has = []
    if "profile" in e:
        has.append("profile")
    protocols = t.get("protocols", {})
    if any("map" in p for p in protocols.values()):
        has.append("map")
    enip = protocols.get("enip", {})
    if "eds" in enip or "input_assembly" in enip:
        has.append("EDS connection")
    if "record" in e:
        has.append("record")
    points = t.get("points", [])
    if points:
        has.append(f"{len(points)} point{'s' if len(points) != 1 else ''}")
    return ", ".join(has) or "identity and sources"


def cell(v: str) -> str:
    """Text inside a Markdown table cell: no pipe ends it, no markup starts in it."""
    entities = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
    return "".join(entities.get(c) or ("\\" + c if c in "\\|[]*_`~" else c) for c in v)


def catalog(index: dict) -> str:
    """CATALOG.md: every device under its category, with what its folder gives."""
    by = {}
    for e in index["devices"]:
        by.setdefault(e["category"], []).append(e)
    used = [c for c in (*CATEGORIES, UNSORTED) if c[0] in by]
    n = len(index["devices"])
    lines = [
        "# Catalog",
        "",
        "<!-- Written by scripts/build-index.py from every device.toml. Do not edit: run the script. -->",
        "",
        f"{n} device{'s' if n != 1 else ''} in {len(used)} categor{'ies' if len(used) != 1 else 'y'}.",
        "Pick a category, pick a row, then",
        "`python3 -I scripts/use.py <folder>` prints what goes into a Helmsman project",
        "([AGENTS.md](AGENTS.md), Using a device). The same list from a shell:",
        "`python3 -I scripts/find.py [category] [words]`.",
        "",
        "| category | devices | what is in it |",
        "| --- | --- | --- |",
    ]
    lines += [f"| [{cell(label)}](#{cid}) | {len(by[cid])} | {cell(what)} |" for cid, label, what in used]
    lines += [
        "",
        "In each table, **to use it** is what the folder gives, best first: a `profile`",
        "(channels by name, the box picks the protocol), a `map` (I/O map lines to copy),",
        "an `EDS connection` (the assembly instances and sizes of the vendor's file),",
        "a `record` (a wired sensor's signals), and the number of documented points.",
        "**checked** is the date a unit confirmed the entry; `documents` means none has.",
    ]
    for cid, label, what in used:
        lines += [
            "",
            f'<a name="{cid}"></a>',
            "",
            f"## {label}",
            "",
            f"{what} `find.py {cid}`",
            "",
            "| model | vendor | speaks | channels | to use it | checked |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for e in sorted(by[cid], key=lambda e: (e["vendor"].casefold(), e["model"].casefold(), e["folder"])):
            speaks = ", ".join(PROTOCOL_NAMES.get(k, k) for k in e.get("protocols", {}))
            if not speaks and "iolink" in e.get("identity", {}):
                speaks = "IO-Link, or a plain switching wire"
            lines.append(
                f"| [{cell(e['model'])}]({e['folder']}/) | {cell(e['vendor'])} | {cell(speaks)} "
                f"| {cell(e.get('channels', ''))} | {cell(gives(ROOT / e['folder'], e))} "
                f"| {e.get('checked_on', 'documents')} |"
            )
    return "\n".join(lines) + "\n"


SCHEMA = ROOT / "docs" / "device.schema.json"
TYPES = {
    "str": lambda v: isinstance(v, str),
    "int": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "bool": lambda v: isinstance(v, bool),
    # A TOML date or a quoted YYYY-MM-DD; date() checks the calendar.
    "date": lambda v: (
        (isinstance(v, datetime.date) and not isinstance(v, datetime.datetime)) or isinstance(v, str)
    ),
    "list": lambda v: isinstance(v, list),
    "map": lambda v: isinstance(v, dict),
}


def conform(v, spec, path, rel):
    """Refuse a key the schema does not list and a value of the wrong type."""
    if isinstance(spec, str):
        if not TYPES[spec](v):
            raise SystemExit(f"{rel}: {path}: a {spec}, got {type(v).__name__}")
    elif isinstance(spec, list):
        if not isinstance(v, list) or not all(isinstance(r, dict) for r in v):
            raise SystemExit(f"{rel}: {path}: a list of tables")
        for i, row in enumerate(v):
            conform(row, spec[0], f"{path}[{i}]", rel)
    else:
        if not isinstance(v, dict):
            raise SystemExit(f"{rel}: {path or 'device.toml'}: a table, got {type(v).__name__}")
        for key, val in v.items():
            where = f"{path}.{key}" if path else key
            if key not in spec:
                raise SystemExit(f"{rel}: {where}: not a key of docs/device.schema.json")
            conform(val, spec[key], where, rel)


def entry(folder: pathlib.Path) -> dict:
    t = tomllib.loads((folder / "device.toml").read_text())
    dev = t.get("device", {})
    rel = folder.relative_to(ROOT).as_posix()
    out = {
        "folder": rel,
        "vendor": text(dev.get("vendor"), f"{rel}: device.vendor"),
        "model": text(dev.get("model"), f"{rel}: device.model"),
        "kind": text(dev.get("kind", "other"), f"{rel}: device.kind"),
        "category": category(dev, t, rel),
    }
    # Catalog fields: what a page shows. A box ignores keys it does not read.
    for key in ("channels", "firmware"):
        if key in dev:
            out[key] = text(dev[key], f"{rel}: device.{key}")
    if "checked_on" in dev:
        out["checked_on"] = date(dev["checked_on"], f"{rel}: device.checked_on")
    if "photo" in dev:
        out["photo"] = photo(dev["photo"], rel)
    profile = dev.get("profile")
    if profile is not None:
        profile = text(profile, f"{rel}: device.profile")
        stem = profile[: -len(".device")] if profile.endswith(".device") else ""
        if (
            not stem
            or not (1 <= len(stem) <= 48)
            or not stem[0].isalnum()
            or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for c in stem)
        ):
            raise SystemExit(f"{rel}: device.profile: NAME.device, NAME 1 to 48 of a-z 0-9 _ -")
        if not (folder / profile).is_file():
            raise SystemExit(f"{rel}: device.profile names {profile}, which is not in the folder")
        first = (folder / profile).read_text().splitlines()[:1]
        if first != ["helmsman-device 1"]:
            raise SystemExit(f"{rel}: {profile}: the first line must be helmsman-device 1")
        out["profile"] = profile
    ident = {}
    enip = t.get("identity", {}).get("enip")
    if enip:
        v, p = enip.get("vendor_id"), enip.get("product_code")
        if not (isinstance(v, int) and isinstance(p, int) and 0 <= v <= 65535 and 0 <= p <= 65535):
            raise SystemExit(f"{rel}: identity.enip needs vendor_id and product_code 0..65535")
        ident["enip"] = {"vendor_id": v, "product_code": p}
    # A sensor or actuator's own identity (its IODD's): how a record drafted
    # from an IODD is found again. Additive: a box ignores keys it does not read.
    iolink = t.get("identity", {}).get("iolink")
    if iolink:
        v, d = iolink.get("vendor_id"), iolink.get("device_id")
        if not (
            isinstance(v, int)
            and isinstance(d, int)
            and not isinstance(v, bool)
            and not isinstance(d, bool)
            and 1 <= v <= 65535
            and 1 <= d <= 16777215
        ):
            raise SystemExit(f"{rel}: identity.iolink needs vendor_id 1..65535 and device_id 1..16777215")
        ident["iolink"] = {"vendor_id": v, "device_id": d}
    if ident:
        out["identity"] = ident
    # The order numbers one record covers (a sensor's IODD names several), so
    # a search by the number on the label finds it.
    variants = t.get("variants")
    if variants:
        if not isinstance(variants, list) or len(variants) > 128:
            raise SystemExit(f"{rel}: variants: at most 128 tables")
        out["products"] = [
            text(v.get("product_id") if isinstance(v, dict) else None, f"{rel}: variants.product_id")
            for v in variants
        ]
    # A wired sensor or actuator has its detail in record.json beside
    # device.toml (scripts/build-records.py): say that it is there.
    if "wired" in t:
        out["record"] = "record.json"
    # How many [[points]] the documents gave: a list says which entries name their channels.
    points = t.get("points", [])
    if not isinstance(points, list) or len(points) > 4096:
        raise SystemExit(f"{rel}: points: at most 4096 tables")
    if points:
        out["points"] = len(points)
    protocols = {}
    for name, p in t.get("protocols", {}).items():
        if not isinstance(p, dict):
            raise SystemExit(f"{rel}: protocols.{name}: a table with a driver")
        driver = text(p.get("driver"), f"{rel}: protocols.{name}.driver")
        if driver not in ("enip-io", "modbus-tcp", "logix-tag"):
            raise SystemExit(f"{rel}: protocols.{name}.driver: not a Helmsman driver: {driver}")
        rec = {"driver": driver}
        for key in ("map", "profile"):
            if key in p:
                rec[key] = file_name(p[key], f"{rel}: protocols.{name}.{key}")
                if key == "map" and not (folder / rec[key]).is_file():
                    raise SystemExit(
                        f"{rel}: protocols.{name}.map names {rec[key]}, which is not in the folder"
                    )
        eds = p.get("eds")
        if eds:
            sha = str(eds.get("sha256", ""))
            if len(sha) != 64 or any(c not in "0123456789abcdefABCDEF" for c in sha):
                raise SystemExit(f"{rel}: protocols.{name}.eds.sha256: 64 hex digits")
            rec["eds"] = {
                "name": file_name(eds.get("name"), f"{rel}: eds.name"),
                "size": int(eds.get("size", 0)),
                "sha256": sha.lower(),
            }
        protocols[name] = rec
    if protocols:
        out["protocols"] = protocols
    # Last, so a field's own message (what a box needs of it) wins over the schema's.
    conform(t, json.loads(SCHEMA.read_text())["root"], "", rel)
    return out


def main() -> int:
    folders = sorted(p.parent for p in (ROOT / "devices").glob("*/*/device.toml"))
    devices = [entry(f) for f in folders]
    used = {d["category"] for d in devices}
    index = {
        "format": FORMAT,
        # A box reads "format" and "devices" and ignores the rest; a page and
        # scripts/find.py take the categories' names from here.
        "categories": [
            {"id": cid, "label": label, "what": what}
            for cid, label, what in (*CATEGORIES, UNSORTED)
            if cid in used
        ],
        "devices": devices,
    }
    seen = set()
    for d in index["devices"]:
        key = json.dumps(d.get("identity"), sort_keys=True)
        if d.get("identity") and key in seen:
            raise SystemExit(f"{d['folder']}: the same identity as another folder")
        seen.add(key)
    outputs = {
        "index.json": json.dumps(index, indent=1, ensure_ascii=False) + "\n",
        "CATALOG.md": catalog(index),
    }
    unsorted = [d["folder"] for d in devices if d["category"] == UNSORTED[0]]
    if "--check" in sys.argv[1:]:
        stale = [
            n for n, want in outputs.items() if not (ROOT / n).exists() or (ROOT / n).read_text() != want
        ]
        if stale:
            print(f"{' and '.join(stale)} out of date: run scripts/build-index.py", file=sys.stderr)
            return 1
        print(f"index.json and CATALOG.md are current ({len(devices)} device(s))")
        return 0
    for name, want in outputs.items():
        (ROOT / name).write_text(want)
    print(f"wrote index.json and CATALOG.md: {len(devices)} device(s)")
    if unsorted:
        ids = ", ".join(c[0] for c in CATEGORIES)
        print(f"no [device] category yet (one of {ids}):", file=sys.stderr)
        for f in unsorted:
            print(f"  {f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
