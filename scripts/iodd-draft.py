#!/usr/bin/env python3 -I
"""Draft a library folder for a sensor or actuator from its IODD, read and not checked.

An IODD is the description file every IO-Link device has. This library uses
it as the device's metadata, whether or not IO-Link is ever spoken to the
device: most such devices are wired to a plain digital input or output and
switch one wire. The draft says who makes the device, what it is called,
which variants there are, how each connector is wired, whether it switches
without an IO-Link master (SIO), and what its signals are called.

Reads an IODD (IODD 1.1, an XML file) and writes devices/<vendor>/<model>/
device.toml and a README.md stub. Everything in the draft is what the IODD
says; nothing is from a unit, so the draft has no checked_on and says so.
An IODD does not say which of its signals the switching wire carries
without a master: a person or an agent reads that from the manual.

Usage:
  python3 -I scripts/iodd-draft.py show IODD
      print what the IODD says, as JSON
  python3 -I scripts/iodd-draft.py draft IODD FOLDER --url URL [--vendor TEXT] [--model TEXT]
      [--kind sensor|actuator|other] [--force]
      write FOLDER/device.toml and README.md; URL is where the IODD was downloaded
      (https), written beside its name, size and SHA-256

An existing device.toml is never overwritten without --force.
Standard library only (Python 3.11).

Reference: IO Device Description Specification V1.1.5 (IO-Link Community,
order no. 10.012) and the schemas in its package (IODD1.1.xsd,
IODD-Datatypes1.1.xsd, IODD-Communication1.1.xsd).
"""

import hashlib
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_IODD = 8 * 1024 * 1024
TEXT_MAX = 120  # build-index.py's limit for a text
XSI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"
KINDS = ("sensor", "actuator", "other")
# IODD-Datatypes1.1.xsd: the simple types and their length in bits when fixed.
SIMPLE = {
    "BooleanT": ("bool", 1),
    "UIntegerT": ("uint", None),
    "IntegerT": ("int", None),
    "Float32T": ("float32", 32),
    "StringT": ("string", None),
    "OctetStringT": ("octets", None),
    "TimeT": ("time", 64),
    "TimeSpanT": ("timespan", 64),
}


# IODD-Communication1.1.xsd: on the standard connectors wire 1 is L+ (brown),
# wire 3 is L- (blue) and wire 4 is C/Q (black) unless the file says another
# function; a file may leave these out. Wire 2 is white on the 4-pole ones.
STANDARD_CONNECTORS = ("M5", "M8", "M12-4", "M12-5")
FIXED_WIRES = {1: ("L+", "BN"), 3: ("L-", "BU"), 4: ("C/Q", "BK")}
MAX_SETTINGS = 64
MAX_VALUES = 16


class IoddError(ValueError):
    pass


def local(tag: str) -> str:
    """An element's name without its namespace."""
    return tag.rsplit("}", 1)[-1]


def child(el, name: str):
    return next((c for c in el if local(c.tag) == name), None)


def children(el, name: str):
    return [c for c in el if local(c.tag) == name]


def need(el, name: str):
    c = child(el, name)
    if c is None:
        raise IoddError(f"<{local(el.tag)}> has no <{name}>")
    return c


def clean(s: str, limit: int = TEXT_MAX) -> str:
    """A text from the file as one printable line of at most `limit` characters."""
    return " ".join("".join(c if c.isprintable() else " " for c in str(s)).split())[:limit]


def number(el, name: str, lo: int, hi: int) -> int:
    raw = el.get(name)
    if raw is None:
        raise IoddError(f"<{local(el.tag)}> has no {name}=")
    if not re.fullmatch(r"[0-9]{1,9}", raw) or not lo <= int(raw) <= hi:
        raise IoddError(f"<{local(el.tag)}> {name}={clean(raw, 40)!r}: not a number from {lo} to {hi}")
    return int(raw)


def flag(el, name: str) -> bool:
    raw = el.get(name)
    if raw not in ("true", "false", "1", "0"):
        raise IoddError(f"<{local(el.tag)}> {name}: true or false")
    return raw in ("true", "1")


class Reader:
    def __init__(self, root):
        self.texts = {}
        language = need(need(root, "ExternalTextCollection"), "PrimaryLanguage")
        for t in children(language, "Text"):
            if t.get("id") is not None and t.get("value") is not None:
                self.texts[t.get("id")] = t.get("value")
        self.datatypes = {}

    def text(self, el, name: str, required: bool = False) -> str | None:
        """The primary-language text a <Name>-like child refers to; the id itself when the text is missing."""
        ref = child(el, name)
        if ref is None or ref.get("textId") is None:
            if required:
                raise IoddError(f"<{local(el.tag)}> has no <{name} textId=>")
            return None
        return clean(self.texts.get(ref.get("textId"), ref.get("textId")))

    def datatype(self, el):
        ref = child(el, "DatatypeRef")
        if ref is not None:
            found = self.datatypes.get(ref.get("datatypeId"))
            if found is None:
                raise IoddError(f"no Datatype with id {clean(ref.get('datatypeId') or '', 40)!r}")
            return found
        for name in ("Datatype", "SimpleDatatype"):
            c = child(el, name)
            if c is not None:
                return c
        raise IoddError(f"<{local(el.tag)}> has no data type")

    def simple(self, el) -> dict:
        kind = el.get(XSI_TYPE)
        if kind not in SIMPLE:
            raise IoddError(f"data type {clean(kind or '', 40)!r} where a simple type is needed")
        name, bits = SIMPLE[kind]
        if kind in ("UIntegerT", "IntegerT"):
            bits = number(el, "bitLength", 2, 64)
        elif kind in ("StringT", "OctetStringT"):
            bits = number(el, "fixedLength", 1, 232) * 8
        out = {"type": name, "bit_length": bits}
        values = {}
        for v in children(el, "SingleValue"):
            label = self.text(v, "Name")
            if label and v.get("value") is not None:
                values[clean(v.get("value"), 24)] = label
        if values:
            out["values"] = values
        return out

    def settings(self, function) -> list[dict]:
        """The parameters a person chooses between, each with its factory value.

        Kept: a read-write variable, or an item of a read-write record, that is a
        choice (a boolean, or a number whose values have names) and has a
        default in the file. Numbers without named values (a delay, a setpoint)
        are left out, and so is anything this reader cannot type: a setting is
        an extra, and a file is not refused over one.
        """
        out = []
        collection = child(function, "VariableCollection")
        for v in children(collection, "Variable") if collection is not None else []:
            raw = v.get("index") or ""
            if v.get("accessRights") != "rw" or not re.fullmatch(r"[0-9]{1,5}", raw) or int(raw) > 65535:
                continue
            try:
                dt = self.datatype(v)
                name = self.text(v, "Name") or clean(v.get("id") or "", 64)
                if dt.get(XSI_TYPE) == "RecordT":
                    defaults = {
                        i.get("subindex"): i.get("defaultValue") for i in children(v, "RecordItemInfo")
                    }
                    for ri in children(dt, "RecordItem"):
                        sub = number(ri, "subindex", 1, 255)
                        item = self.text(ri, "Name") or str(sub)
                        self.setting(out, f"{name}: {item}", int(raw), sub, ri, defaults.get(str(sub)))
                else:
                    self.setting(out, name, int(raw), None, v, v.get("defaultValue"))
            except IoddError:
                continue
        return out[:MAX_SETTINGS]

    def setting(self, out: list, name: str, index: int, sub: int | None, el, default) -> None:
        s = self.simple(self.datatype(el))
        values = s.get("values", {})
        if default is None or not (values or s["type"] == "bool"):
            return
        default = clean(default, 24)
        rec = {"name": clean(name), "index": index}
        if sub is not None:
            rec["subindex"] = sub
        rec["default"] = default
        if default in values:
            rec["default_name"] = values[default]
        if values:
            rec["values"] = dict(list(values.items())[:MAX_VALUES])
        out.append(rec)

    def signals(self, item, bit_length: int) -> list[dict]:
        dt = self.datatype(item)
        kind = dt.get(XSI_TYPE)
        out = []
        if kind == "RecordT":
            if number(dt, "bitLength", 1, 1856) != bit_length:
                raise IoddError(
                    f"a record of {dt.get('bitLength')} bits as {bit_length} bits of process data"
                )
            for ri in children(dt, "RecordItem"):
                s = self.simple(self.datatype(ri))
                out.append(
                    {
                        "name": self.text(ri, "Name", required=True),
                        "subindex": number(ri, "subindex", 1, 255),
                        "bit_offset": number(ri, "bitOffset", 0, 1855),
                        **s,
                    }
                )
                description = self.text(ri, "Description")
                if description:
                    out[-1]["description"] = description
            if not out:
                raise IoddError("a record with no RecordItem")
        elif kind == "ArrayT":
            count = number(dt, "count", 1, 255)
            s = self.simple(self.datatype(dt))
            name = self.text(item, "Name", required=True)
            # Interface Specification Table F.17: the highest subindex is at the right.
            for i in range(1, count + 1):
                out.append(
                    {"name": f"{name} {i}", "subindex": i, "bit_offset": (count - i) * s["bit_length"], **s}
                )
        else:
            out.append(
                {
                    "name": self.text(item, "Name", required=True),
                    "subindex": 0,
                    "bit_offset": 0,
                    **self.simple(dt),
                }
            )
        out.sort(key=lambda s: s["subindex"])
        used = set()
        for s in out:
            bits = range(s["bit_offset"], s["bit_offset"] + s["bit_length"])
            if bits.stop > bit_length:
                raise IoddError(f"{s['name']!r} ends at bit {bits.stop} of {bit_length} bits of process data")
            if used & set(bits):
                raise IoddError(f"{s['name']!r} shares bits with another item")
            used |= set(bits)
        return out

    def item(self, el) -> dict:
        bits = number(el, "bitLength", 1, 256)
        return {
            "name": self.text(el, "Name", required=True),
            "bit_length": bits,
            "signals": self.signals(el, bits),
        }


def parse(data: bytes) -> dict:
    """What an IODD says, as plain data. Raises IoddError for anything else."""
    if len(data) > MAX_IODD:
        raise IoddError(f"{len(data)} bytes; an IODD here is at most {MAX_IODD}")
    # No DOCTYPE, so no entity can be declared and none expands.
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data:
        raise IoddError("a DOCTYPE or an entity declaration: not read")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        raise IoddError(f"not well-formed XML: {e}") from None
    except (ValueError, LookupError, RecursionError) as e:  # an encoding nobody has, among others
        raise IoddError(f"not readable XML: {type(e).__name__}") from None
    if local(root.tag) != "IODevice":
        raise IoddError(f"<{clean(local(root.tag), 40)}> is not an IODD's <IODevice>")
    body = need(root, "ProfileBody")
    ident = need(body, "DeviceIdentity")
    function = need(body, "DeviceFunction")
    r = Reader(root)
    vendor_name = ident.get("vendorName")
    if not vendor_name or not clean(vendor_name):
        raise IoddError("<DeviceIdentity> has no vendorName=")
    out = {
        "vendor_id": number(ident, "vendorId", 1, 65535),
        "device_id": number(ident, "deviceId", 1, 16777215),
        "vendor_name": clean(vendor_name),
        "device_name": r.text(ident, "DeviceName", required=True),
    }
    for key, name in (("family", "DeviceFamily"), ("vendor_text", "VendorText"), ("vendor_url", "VendorUrl")):
        value = r.text(ident, name)
        if value:
            out[key] = value
    info = child(root, "DocumentInfo")
    if info is not None:
        for key, name in (("iodd_version", "version"), ("iodd_date", "releaseDate")):
            if info.get(name):
                out[key] = clean(info.get(name), 24)
    variants = []
    collection = child(ident, "DeviceVariantCollection")
    for v in children(collection, "DeviceVariant") if collection is not None else []:
        if not v.get("productId"):
            raise IoddError("<DeviceVariant> has no productId=")
        variant = {"product_id": clean(v.get("productId"))}
        for key, name in (("name", "Name"), ("description", "Description")):
            value = r.text(v, name)
            if value:
                variant[key] = value
        variants.append(variant)
    out["variants"] = variants

    profile = child(root, "CommNetworkProfile")
    layers = child(profile, "TransportLayers") if profile is not None else None
    physical = child(layers, "PhysicalLayer") if layers is not None else None
    connections = []
    if physical is not None:
        out["sio"] = flag(physical, "sioSupported")
        if physical.get("bitrate") in ("COM1", "COM2", "COM3"):
            out["bitrate"] = physical.get("bitrate")
        if physical.get("minCycleTime") is not None:
            out["min_cycle_us"] = number(physical, "minCycleTime", 0, 132800)
        for c in children(physical, "Connection"):
            kind = (c.get(XSI_TYPE) or "").removesuffix("ConnectionT")
            wires = []
            for n in range(1, 10):
                w = child(c, f"Wire{n}")
                if w is None:
                    continue
                wire = {"n": n}
                given = {key: clean(w.get(key), 24) for key in ("function", "color") if w.get(key)}
                if kind in STANDARD_CONNECTORS:
                    fixed = FIXED_WIRES.get(n, (None, "WH" if n == 2 and kind != "M12-5" else None))
                    for key, value in zip(("function", "color"), fixed, strict=True):
                        if value:
                            given.setdefault(key, value)
                for key in ("function", "color"):
                    if key in given:
                        wire[key] = given[key]
                label = r.text(w, "Name")
                if label:
                    wire["name"] = label
                wires.append(wire)
            connections.append(
                {
                    "type": clean(kind, 24) or "Other",
                    "products": [clean(p.get("productId") or "") for p in children(c, "ProductRef")],
                    "wires": wires,
                }
            )
    out["connections"] = connections

    collection = child(function, "DatatypeCollection")
    for dt in children(collection, "Datatype") if collection is not None else []:
        if dt.get("id"):
            r.datatypes[dt.get("id")] = dt
    layouts = []
    collection = child(function, "ProcessDataCollection")
    for pd in children(collection, "ProcessData") if collection is not None else []:
        layout = {"id": clean(pd.get("id") or "", 64)}
        cond = child(pd, "Condition")
        if cond is not None:
            layout["condition"] = {
                "variable": clean(cond.get("variableId") or "", 64),
                "value": number(cond, "value", 0, 255),
            }
        for key, name in (("in", "ProcessDataIn"), ("out", "ProcessDataOut")):
            el = child(pd, name)
            if el is not None:
                layout[key] = r.item(el)
        layouts.append(layout)
    out["process_data"] = layouts
    out["settings"] = r.settings(function)
    features = child(function, "Features")
    ids = (features.get("profileCharacteristic") or "").split() if features is not None else []
    if ids and len(ids) <= 32 and all(re.fullmatch(r"[0-9]{1,5}", i) and int(i) <= 65535 for i in ids):
        out["profile_characteristic"] = [int(i) for i in ids]
    return out


def toml_str(s: str) -> str:
    return json.dumps(str(s), ensure_ascii=False)


def guess_kind(iodd: dict) -> str:
    """Inputs make a sensor, outputs alone an actuator; an IODD does not say."""
    has_in = any("in" in layout for layout in iodd["process_data"])
    has_out = any("out" in layout for layout in iodd["process_data"])
    return "sensor" if has_in else "actuator" if has_out else "other"


def toml_key(k: str) -> str:
    return k if re.fullmatch(r"[A-Za-z0-9_-]+", k) else toml_str(k)


def inline(table: dict) -> str:
    body = ", ".join(
        f"{toml_key(k)} = {toml_str(v) if isinstance(v, str) else json.dumps(v, ensure_ascii=False)}"
        for k, v in table.items()
    )
    return "{ " + body + " }"


def bits(s: dict) -> str:
    last = s["bit_offset"] + s["bit_length"] - 1
    return str(s["bit_offset"]) if last == s["bit_offset"] else f"{s['bit_offset']}..{last}"


def draft(iodd: dict, file: dict, vendor: str, model: str, kind: str) -> str:
    lines = [
        "# Drafted by scripts/iodd-draft.py from the IODD alone. No unit has been checked:",
        "# checked_on and checked_by stay out until one has, and every value below is",
        "# what the vendor's file says, not what a device did.",
        "[device]",
        f"vendor = {toml_str(vendor)}",
        f"model = {toml_str(model)}",
        "# kind: inputs make a sensor, outputs alone an actuator; the IODD does not say. Change it if wrong.",
        f"kind = {toml_str(kind)}",
    ]
    if iodd.get("family"):
        lines.append(f"family = {toml_str(iodd['family'])}")
    if iodd.get("vendor_url"):
        lines.append(f"vendor_url = {toml_str(iodd['vendor_url'])}")
    lines += [
        "",
        "# What the device answers on an IO-Link port. Not needed to use it on a digital channel;",
        "# it is how this record is found again from the device's IODD.",
        "[identity.iolink]",
        f"vendor_id = {iodd['vendor_id']}",
        f"device_id = {iodd['device_id']}",
    ]
    for v in iodd["variants"]:
        lines += ["", "[[variants]]"] + [
            f"{k} = {toml_str(v[k])}" for k in ("product_id", "name", "description") if k in v
        ]
    lines += ["", "# The device on plain digital channels, with no IO-Link master.", "[wired]"]
    if "sio" in iodd:
        lines.append(
            f"sio = {'true' if iodd['sio'] else 'false'}   # "
            + (
                "it switches its C/Q wire on its own (SIO mode)"
                if iodd["sio"]
                else "the IODD says it does not switch without a master"
            )
        )
    lines.append("# Which signal the switching wire carries is not in an IODD: read it from the manual,")
    lines.append('# then add: switching = "<signal name>", source = "<manual, page>"')
    for c in iodd["connections"]:
        lines += ["", "[[wired.connections]]", f"type = {toml_str(c['type'])}"]
        if c["products"]:
            lines.append("products = [" + ", ".join(toml_str(p) for p in c["products"]) + "]")
        if c["wires"]:
            lines.append("wires = [")
            lines += [f"  {inline(w)}," for w in c["wires"]]
            lines.append("]")
    for layout in iodd["process_data"]:
        for direction in ("in", "out"):
            for s in layout.get(direction, {}).get("signals", []):
                lines += [
                    "",
                    "[[signals]]   # as the device names it over IO-Link",
                    f"dir = {toml_str(direction)}",
                    f"name = {toml_str(s['name'])}",
                    f"type = {toml_str(s['type'])}",
                    f"bits = {toml_str(bits(s))}",
                ]
                if "condition" in layout:
                    lines.append(
                        f"layout = {toml_str(layout['id'])}   # one of several the device can be set to"
                    )
                if s.get("description"):
                    lines.append(f"description = {toml_str(s['description'])}")
                values = s.get("values", {})
                if s["type"] == "bool" and values:
                    for key, label in (("false", "off"), ("true", "on")):
                        if key in values:
                            lines.append(f"{label} = {toml_str(values[key])}")
                elif values:
                    lines.append(f"values = {inline(values)}")
    for st in iodd.get("settings", []):
        lines += [
            "",
            "[[settings]]   # a parameter that is a choice, with its factory value, as the IODD states it",
            f"name = {toml_str(st['name'])}",
            f"index = {st['index']}",
        ]
        if "subindex" in st:
            lines.append(f"subindex = {st['subindex']}")
        lines.append(f"default = {toml_str(st['default'])}")
        if "default_name" in st:
            lines.append(f"default_name = {toml_str(st['default_name'])}")
        if st.get("values"):
            lines.append(f"values = {inline(st['values'])}")
    lines += [
        "",
        "[iodd]",
        "file = " + inline({k: file[k] for k in ("name", "size", "sha256", "url") if k in file}),
    ]
    for key in ("iodd_version", "iodd_date"):
        if iodd.get(key):
            lines.append(f"{key.removeprefix('iodd_')} = {toml_str(iodd[key])}")
    if iodd.get("profile_characteristic"):
        lines.append(
            f"profile_characteristic = {json.dumps(iodd['profile_characteristic'])}"
            "   # the profiles and function classes the device declares"
        )
    lines += [
        "",
        "[[sources]]",
        f"title = {toml_str('IODD ' + file['name'])}",
        f"sha256 = {toml_str(file['sha256'])}",
        f"where = {toml_str(file['url'] + '; not redistributed here')}",
    ]
    return "\n".join(lines) + "\n"


def cell(s) -> str:
    return str(s).replace("|", "/")


def readme(iodd: dict, file: dict, vendor: str, model: str) -> str:
    variants = "\n".join(
        f"| {cell(v['product_id'])} | {cell(v.get('name', ''))} | {cell(v.get('description', ''))} |"
        for v in iodd["variants"]
    )
    wires = "\n".join(
        f"| {cell(c['type'])} | {cell(', '.join(c['products']))} | "
        + cell(
            "; ".join(
                f"{w['n']}: {w.get('function', '?')}" + (f" ({w['color']})" if "color" in w else "")
                for w in c["wires"]
            )
        )
        + " |"
        for c in iodd["connections"]
    )
    signals = "\n".join(
        f"| {direction} | {cell(s['name'])} | {s['type']} | {bits(s)} | "
        + cell(", ".join(f"{k} = {v}" for k, v in s.get("values", {}).items()))
        + " |"
        for layout in iodd["process_data"]
        for direction in ("in", "out")
        for s in layout.get(direction, {}).get("signals", [])
    )
    settings = "\n".join(
        f"| {cell(st['name'])} | {st['index']}{'.' + str(st['subindex']) if 'subindex' in st else ''} | "
        f"{cell(st.get('default_name', st['default']))} | "
        + cell(", ".join(st.get("values", {}).values()))
        + " |"
        for st in iodd.get("settings", [])
    )
    sio = {True: "yes", False: "no"}.get(iodd.get("sio"), "not stated")
    return f"""> **Draft from documents.** No unit has been checked; every value here is the
> IODD's, read by `scripts/iodd-draft.py`. Which signal the switching wire
> carries without an IO-Link master is still to be read from the manual, with
> its page.

# {vendor} {model}

IODD identity: vendor {iodd["vendor_id"]} {iodd["vendor_name"]}, device {iodd["device_id"]};
IODD file {iodd.get("iodd_version", "?")} ({iodd.get("iodd_date", "no date")}).
Switches without a master (SIO): {sio}.

## Variants

| product id | name | description |
| --- | --- | --- |
{variants or "| none listed | | |"}

## Connections

| connector | products | wires |
| --- | --- | --- |
{wires or "| none listed | | |"}

## Signals, as the device names them over IO-Link

| dir | name | type | bits | values |
| --- | --- | --- | --- | --- |
{signals or "| none | | | | |"}

## Settings and their factory values

| setting | index | factory value | choices |
| --- | --- | --- | --- |
{settings or "| none read | | | |"}

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
| IODD {cell(file["name"])} | `{file["sha256"][:16]}…` | {cell(file["url"])} |

Vendor files are not in this repository; download the IODD and check the hash.
"""


def option(args: list[str], name: str) -> str | None:
    if name not in args:
        return None
    i = args.index(name)
    if i + 1 >= len(args):
        raise SystemExit(f"{name} needs a value")
    value = args[i + 1]
    del args[i : i + 2]
    return value


def main(argv: list[str], root: pathlib.Path = ROOT) -> int:
    if len(argv) == 2 and argv[0] == "show":
        path = pathlib.Path(argv[1])
        if not path.is_file():
            raise SystemExit(f"{argv[1]}: no such file")
        try:
            print(json.dumps(parse(path.read_bytes()), indent=1, ensure_ascii=False))
        except IoddError as e:
            raise SystemExit(f"{argv[1]}: {e}") from None
        return 0
    if len(argv) >= 3 and argv[0] == "draft":
        args = argv[1:]
        force = "--force" in args
        if force:
            args.remove("--force")
        url, vendor, model, kind = (option(args, n) for n in ("--url", "--vendor", "--model", "--kind"))
        if len(args) != 2:
            raise SystemExit("draft needs IODD FOLDER --url URL")
        if not url or not re.fullmatch(r"https://[!-~]{4,400}", url) or '"' in url:
            raise SystemExit("--url: where the IODD was downloaded, an https address")
        if kind is not None and kind not in KINDS:
            raise SystemExit(f"--kind: one of {', '.join(KINDS)}")
        path = pathlib.Path(args[0])
        folder = args[1].rstrip("/")
        if not re.fullmatch(r"devices/[a-z0-9][a-z0-9_.-]{0,63}/[a-z0-9][a-z0-9_.-]{0,63}", folder):
            raise SystemExit("FOLDER must be devices/<vendor>/<model>, a-z 0-9 . _ -")
        if not path.is_file():
            raise SystemExit(f"{args[0]}: no such file")
        data = path.read_bytes()
        try:
            iodd = parse(data)
        except IoddError as e:
            raise SystemExit(f"{path.name}: {e}") from None
        file = {
            "name": clean(path.name),
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "url": url,
        }
        vendor = clean(vendor or iodd["vendor_name"])
        model = clean(model or iodd["device_name"])
        if not vendor or not model:
            raise SystemExit("--vendor and --model: a printable text")
        target = root / folder
        if (target / "device.toml").exists() and not force:
            raise SystemExit(f"{folder}/device.toml exists: --force to overwrite")
        target.mkdir(parents=True, exist_ok=True)
        (target / "device.toml").write_text(draft(iodd, file, vendor, model, kind or guess_kind(iodd)))
        if not (target / "README.md").exists() or force:
            (target / "README.md").write_text(readme(iodd, file, vendor, model))
        print(f"wrote {folder}/device.toml and README.md (draft from {file['name']})")
        return 0
    print(__doc__.split("Usage:")[1].split("An existing")[0], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
