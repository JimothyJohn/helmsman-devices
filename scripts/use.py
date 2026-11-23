#!/usr/bin/env python3 -I
"""What a device's folder gives a Helmsman project, as lines to paste.

Name the device the way scripts/find.py printed it and this prints every way
the folder supports, best first:

  profile   copy NAME.device into the project; channels by name, the box picks the protocol
  map       the folder's I/O map lines, with the address filled in
  eds       the vendor's EDS as a project file; the driver reads the connection from it
  explicit  the EDS's connection written out, for when the file is not at hand
  modbus    the Modbus TCP device line, and the points the documents give
  wired     a sensor or actuator on a digital channel: the word for its signal's line

then the documented points, what nobody has confirmed, and the sources.
Nothing here reaches a device or the internet.

Usage: python3 -I scripts/use.py DEVICE [options]
  DEVICE          a folder (devices/turck/tben-s2-8dxp or turck/tben-s2-8dxp),
                  or words that match exactly one device (tben-s2-8dxp)
  --address A     the device's endpoint, in place of ADDR: a host, host:port,
                  cip=VENDOR:PRODUCT or mac=AA-BB-CC-DD-EE-FF
  --id NAME       the device id in the I/O map (default dev)
  --eds PATH      check a file you have against the entry's EDS (size and SHA-256), then stop
  --json          the same as JSON, for a program

Exit 0, 1 when --eds does not match, 2 for a bad argument or an unknown device.
Standard library only; Python 3.11 or later (tomllib).
"""

import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEGMENT = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}")
DEVICE_ID = re.compile(r"[a-z][a-z0-9_]{0,23}")
RESERVED = ("box", "module", "screen")  # device ids the I/O map keeps (helmsman-io text)
ENDPOINT = re.compile(r"[A-Za-z0-9.:=\[\]_-]{1,80}")
CHANNEL = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,31}")
TYPES = ("bool", "int", "real")
MAX_EDS = 8 << 20
MAX_MAP_LINES = 400
VALUED = ("--address", "--id", "--eds")
UNCHECKED = "No unit has confirmed this entry: every value is the documents'."


class Bad(Exception):
    """An argument this script refuses, or a device it cannot find."""


def printable(v, limit=400):
    s = v if isinstance(v, str) else ("" if v is None else str(v))
    return "".join(c if c.isprintable() else "?" for c in s)[:limit]


def parse_args(argv):
    opts = {"words": []}
    it = iter(argv)
    for a in it:
        if a == "--json":
            opts[a] = True
        elif a in VALUED:
            v = next(it, None)
            if v is None:
                raise Bad(f"{a}: needs a value")
            opts[a] = v
        elif a.startswith("-"):
            raise Bad(f"{a}: not an option (python3 -I scripts/use.py --help)")
        else:
            opts["words"].append(a)
    if not opts["words"]:
        raise Bad("name a device: a folder, or words that match one (python3 -I scripts/find.py lists them)")
    dev_id = opts.get("--id", "dev")
    if not DEVICE_ID.fullmatch(dev_id) or dev_id in RESERVED:
        raise Bad(f"--id: a letter, then letters, digits or _ (at most 24), and not {', '.join(RESERVED)}")
    address = opts.get("--address")
    if address is not None and not ENDPOINT.fullmatch(address):
        raise Bad("--address: a host, host:port, cip=VENDOR:PRODUCT or mac=AA-BB-CC-DD-EE-FF")
    return opts, dev_id, address


def folder_of(words):
    """The device's folder, from a path or from words that match one index entry."""
    if len(words) == 1:
        name = words[0].strip("/")
        name = name.removeprefix("devices/")
        parts = name.split("/")
        if len(parts) == 2 and all(SEGMENT.fullmatch(p) for p in parts):
            folder = ROOT / "devices" / parts[0] / parts[1]
            inside = folder.resolve().is_relative_to((ROOT / "devices").resolve())
            if inside and (folder / "device.toml").is_file():
                return folder
            raise Bad(f"devices/{name}: no such folder (python3 -I scripts/find.py lists them)")
    try:
        devices = json.loads((ROOT / "index.json").read_text())["devices"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise Bad(f"index.json: {e}") from None
    want = [w.casefold() for w in words]
    found = []
    for d in devices:
        products = d.get("products") if isinstance(d.get("products"), list) else []
        hay = " ".join(
            str(x) for x in (d.get("vendor"), d.get("model"), d.get("folder"), *products)
        ).casefold()
        if all(w in hay for w in want):
            found.append(d)
    if len(found) == 1:
        return folder_of([found[0]["folder"]])
    if not found:
        raise Bad(f"{' '.join(words)!r} matches no device (python3 -I scripts/find.py lists them)")
    listing = "\n".join(f"  {printable(d.get('folder'))}" for d in found[:12])
    more = f"\n  and {len(found) - 12} more" if len(found) > 12 else ""
    raise Bad(f"{' '.join(words)!r} matches {len(found)} devices; name one folder:\n{listing}{more}")


def signal_name(dev_id, channel):
    """The signal a channel becomes: helmsman-io's profile::signal_name."""
    return f"{dev_id}_{channel.lower().replace('-', '_')}"


def profile_way(folder, rel, name, dev_id, endpoint):
    stem = name[: -len(".device")]
    transports, channels = [], []
    for line in (folder / name).read_text().splitlines()[:5000]:
        f = line.split("#", 1)[0].split()
        if len(f) >= 2 and f[0] == "transport":
            transports.append(printable(f[1], 40))
        elif len(f) >= 3 and f[0] in ("in", "out") and CHANNEL.fullmatch(f[1]) and f[2] in TYPES:
            channels.append((f[0], f[1], f[2]))
    lines = [f"device {dev_id} device:{stem} {endpoint}"]
    for direction in ("in", "out"):
        first = next((c for c in channels if c[0] == direction), None)
        if first:
            lines.append(f"{direction:<3} {signal_name(dev_id, first[1])} {first[2]} {dev_id} ch:{first[1]}")
    notes = [
        f"{len(channels)} channels: {', '.join(c[1] for c in channels[:12])}{', ...' if len(channels) > 12 else ''}"
    ]
    if transports:
        notes.append(f"The box tries {', then '.join(transports)} and uses the first that answers.")
    notes.append("A signal binds a channel by name (ch:NAME); name the signals as the machine calls them.")
    return {
        "how": "profile",
        "title": "A device profile: channels by name, the box picks the protocol",
        "steps": [f"Copy {rel}/{name} into the project, keeping its name."],
        "lines": lines,
        "notes": notes,
    }


def map_way(folder, rel, protocol, name, address):
    text = (folder / name).read_text().splitlines()[:MAX_MAP_LINES]
    lines = []
    for line in text:
        f = line.split()
        if address and len(f) >= 4 and f[0] == "device":
            # ADDR on a device line only, as a box does it (helmsman-project devlib
            # with_address); an endpoint that brings its own port or is an identity
            # (cip=, mac=) takes the place of ADDR:PORT whole.
            whole = ":" in address or "=" in address
            pattern = r"(?<![A-Za-z0-9_])ADDR" + (r"(:\d+)?" if whole else "") + r"(?![A-Za-z0-9_])"
            line = re.sub(pattern, lambda _: address, line, count=1)
        lines.append(printable(line))
    return {
        "how": "map",
        "title": f"I/O map lines for {protocol}: {rel}/{name}",
        "steps": ["Copy the lines into the project's I/O map."],
        "lines": lines,
        "notes": [
            "The signal names are the bench's: keep the points, rename the signals.",
            *([] if address else ["ADDR is the device's address."]),
        ],
    }


def assembly(enip, key, need_bytes):
    a = enip.get(key)
    if not isinstance(a, dict) or not isinstance(a.get("instance"), int):
        return None
    if need_bytes and not isinstance(a.get("bytes"), int):
        return None
    return a


def eds_ways(rel, enip, dev_id, endpoint, checked):
    ways = []
    eds = enip.get("eds") if isinstance(enip.get("eds"), dict) else None
    config = assembly(enip, "config_assembly", False)
    eds_config, explicit_config = [], []
    if config and isinstance(config.get("bytes"), int) and config["bytes"] > 0:
        n = config["bytes"]
        gives = f"The EDS gives the configuration assembly {n} bytes"
        defaults = "the driver sends the EDS's defaults when every member has one"
        eds_config = [f"{gives}: {defaults}; otherwise add config_data=HEX."]
        explicit_config = [f"{gives}; this form sends none unless you add config_data=HEX."]
    if eds and eds.get("name"):
        name = printable(eds.get("name"), 120)
        ways.append(
            {
                "how": "eds",
                "title": "The vendor's EDS as a project file: the driver reads the connection from it",
                "steps": [
                    f"Get {name} ({eds.get('size')} bytes) from {printable(eds.get('url')) or 'the source below'}.",
                    f"Check it is the file this entry read: python3 -I scripts/use.py {rel} --eds PATH",
                    f"Put it in the project as {name}.",
                ],
                "lines": [f"device {dev_id} enip-io {endpoint} eds={name}"],
                "notes": [f"SHA-256 {printable(eds.get('sha256'), 64)}", *eds_config],
            }
        )
    t2o, o2t = assembly(enip, "input_assembly", True), assembly(enip, "output_assembly", True)
    if t2o and o2t and config:
        line = (
            f"device {dev_id} enip-io {endpoint} config={config['instance']} "
            f"o2t={o2t['instance']}:{o2t['bytes']} t2o={t2o['instance']}:{t2o['bytes']}"
        )
        rpi = enip.get("rpi_ms")
        if isinstance(rpi, dict) and isinstance(rpi.get("default"), int):
            line += f" rpi_ms={rpi['default']}"
        ways.append(
            {
                "how": "explicit",
                "title": "The same connection written out, with no file",
                "steps": [],
                "lines": [line],
                "notes": [
                    "o2t is what the box sends (the device's outputs), t2o what the device sends (its inputs).",
                    *(
                        []
                        if checked
                        else ["These are the EDS's numbers; no unit has opened this connection."]
                    ),
                    *explicit_config,
                ],
            }
        )
    return ways


def modbus_way(modbus, dev_id, endpoint):
    port = modbus.get("port") if isinstance(modbus.get("port"), int) else 502
    where = endpoint if ":" in endpoint or "=" in endpoint else f"{endpoint}:{port}"
    line = f"device {dev_id} modbus-tcp {where}"
    notes = []
    if isinstance(modbus.get("unit"), int):
        line += f" unit={modbus['unit']}"
    else:
        notes.append("The entry states no unit id; the driver's default is 1.")
    notes.append("Points are 0-based: coil:N, di:N, hr:N, ir:N, with :u32, :i16, :f32 for a format.")
    return {"how": "modbus", "title": "Modbus TCP", "steps": [], "lines": [line], "notes": notes}


def wired_way(rel, t):
    name = rel[len("devices/") :]
    wired = t.get("wired", {})
    notes = [
        f"{len(t.get('signals', []))} signals and {len(t.get('settings', []))} factory settings are in {rel}/record.json."
    ]
    if wired.get("switching"):
        notes.append(
            f"Its switching wire carries {printable(wired['switching'])} ({printable(wired.get('source'))})."
        )
    else:
        notes.append(
            "Which signal its switching wire carries is not in the entry yet: read it from the manual."
        )
    return {
        "how": "wired",
        "title": "A sensor or actuator on a digital channel",
        "steps": ["On the I/O map line of the point it is wired to, name it:"],
        "lines": [f"in  part_present bool rio di:3 wired={name}"],
        "notes": ["rio and di:3 are an example: the I/O block and the point it is wired to.", *notes],
    }


def category_label(cid):
    """The category's heading, from index.json; the id when the index does not have it."""
    try:
        cats = json.loads((ROOT / "index.json").read_text()).get("categories", [])
        return next(printable(c["label"]) for c in cats if c.get("id") == cid)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, StopIteration):
        return printable(cid, 40)


def sheet(folder, dev_id, address):
    import tomllib

    rel = folder.relative_to(ROOT).as_posix()
    t = tomllib.loads((folder / "device.toml").read_text())
    dev = t.get("device", {})
    protocols = t.get("protocols", {})
    checked = dev.get("checked_on")
    endpoint = address or "ADDR"
    ways = []
    if isinstance(dev.get("profile"), str) and (folder / dev["profile"]).is_file():
        ways.append(profile_way(folder, rel, dev["profile"], dev_id, endpoint))
    for protocol, p in protocols.items():
        if isinstance(p.get("map"), str) and (folder / p["map"]).is_file():
            ways.append(map_way(folder, rel, printable(protocol, 20), p["map"], address))
    if "enip" in protocols:
        ways += eds_ways(rel, protocols["enip"], dev_id, endpoint, bool(checked))
    if "modbus" in protocols and not protocols["modbus"].get("map"):
        ways.append(modbus_way(protocols["modbus"], dev_id, endpoint))
    if not protocols and "wired" in t:
        ways.append(wired_way(rel, t))
    points = [
        {k: printable(p.get(k)) for k in ("name", "enip", "modbus", "meaning", "source") if p.get(k)}
        for p in t.get("points", [])
        if isinstance(p, dict)
    ]
    open_ = []
    if not checked:
        open_.append(f"{UNCHECKED} Test it on yours before a machine depends on it (AGENTS.md, step 4).")
    if protocols and not points and not dev.get("profile"):
        open_.append(
            "No channel is mapped: the entry has no points. Read them from the manual in the sources, "
            "or work them out on the unit, and send them back (AGENTS.md, Mapping a device)."
        )
    if not ways:
        open_.append("The folder has identity and sources only: nothing to paste yet.")
    open_ += [f"{printable(q.get('ask'))} ({printable(q.get('source'))})" for q in t.get("questions", [])]
    enip_id = t.get("identity", {}).get("enip", {})
    hints = []
    if not address and any(w["how"] in ("profile", "eds", "explicit") for w in ways):
        if isinstance(enip_id.get("vendor_id"), int) and isinstance(enip_id.get("product_code"), int):
            hints.append(
                f"ADDR is the device's address, or cip={enip_id['vendor_id']}:{enip_id['product_code']} "
                "to let the box find it by identity (--address fills it in)."
            )
        else:
            hints.append("ADDR is the device's address (--address fills it in).")
    return {
        "folder": rel,
        "vendor": printable(dev.get("vendor")),
        "model": printable(dev.get("model")),
        "kind": printable(dev.get("kind", "other"), 40),
        "category": printable(dev.get("category"), 40),
        "category_label": category_label(dev.get("category")) if dev.get("category") else "",
        "checked_on": str(checked) if checked else None,
        "firmware": printable(dev.get("firmware")) or None,
        "ways": ways,
        "hints": hints,
        "points": points,
        "open": open_,
        "sources": [
            {"title": printable(s.get("title")), "where": printable(s.get("where"))}
            for s in t.get("sources", [])
            if isinstance(s, dict)
        ],
    }


def render(s):
    out = [f"{s['vendor']} {s['model']}", f"  {s['folder']}  ({s['category_label'] or s['kind']})"]
    if s["checked_on"]:
        out.append(
            f"  Checked on a unit {s['checked_on']}"
            + (f", firmware {s['firmware']}." if s["firmware"] else ".")
        )
    else:
        out.append(f"  {UNCHECKED}")
    out += ["", "Add it to a Helmsman project" + (", best way first:" if len(s["ways"]) > 1 else ":")]
    for n, w in enumerate(s["ways"], 1):
        out += ["", f"{n}. {w['title']}"]
        out += [f"   {step}" for step in w["steps"]]
        out += [f"     {line}" for line in w["lines"]]
        out += [f"   {note}" for note in w["notes"]]
    if not s["ways"]:
        out += ["", "   Nothing to paste yet."]
    out += [f"\n{h}" for h in s["hints"]]
    if s["points"]:
        out += ["", f"Points the documents give ({len(s['points'])}):"]
        for p in s["points"]:
            where = "; ".join(f"{k} {p[k]}" for k in ("enip", "modbus") if k in p)
            out.append(f"  {p.get('name', '')}: {where}")
            out.append(f"    {p.get('meaning', '')}  [{p.get('source', 'no source')}]")
    if s["open"]:
        out += ["", "Not known yet:"] + [f"  - {o}" for o in s["open"]]
    if s["sources"]:
        out += ["", "Sources:"] + [f"  - {x['title']}: {x['where']}" for x in s["sources"]]
    return "\n".join(out)


def check_eds(folder, path):
    import tomllib

    eds = tomllib.loads((folder / "device.toml").read_text()).get("protocols", {}).get("enip", {}).get("eds")
    if not isinstance(eds, dict) or not eds.get("sha256"):
        raise Bad(f"{folder.relative_to(ROOT).as_posix()}: the entry names no EDS")
    p = pathlib.Path(path)
    try:
        size = p.stat().st_size
        if size > MAX_EDS:
            raise Bad(f"{path}: over {MAX_EDS} bytes, not an EDS")
        data = p.read_bytes()
    except OSError as e:
        raise Bad(f"{path}: {e.strerror or e}") from None
    got = hashlib.sha256(data).hexdigest()
    if got == str(eds["sha256"]).lower() and len(data) == eds.get("size"):
        print(
            f"{path} is the entry's EDS: {printable(eds.get('name'), 120)}, {len(data)} bytes, SHA-256 {got}"
        )
        return 0
    print(f"{path} is NOT the file this entry read.", file=sys.stderr)
    print(f"  entry: {eds.get('size')} bytes, SHA-256 {str(eds['sha256']).lower()}", file=sys.stderr)
    print(f"  file:  {len(data)} bytes, SHA-256 {got}", file=sys.stderr)
    print(
        "  Another revision of the EDS may still fit the device; the entry's numbers are for its own.",
        file=sys.stderr,
    )
    return 1


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        return 0
    try:
        import tomllib  # noqa: F401 (3.11 or later; said here, before any work)
    except ImportError:
        print("use.py: needs Python 3.11 or later (tomllib); find.py runs on 3.9", file=sys.stderr)
        return 2
    try:
        opts, dev_id, address = parse_args(argv)
        folder = folder_of(opts["words"])
        if "--eds" in opts:
            return check_eds(folder, opts["--eds"])
        s = sheet(folder, dev_id, address)
    except Bad as e:
        print(f"use.py: {e}", file=sys.stderr)
        return 2
    print(json.dumps(s, indent=1, ensure_ascii=False) if opts.get("--json") else render(s))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
