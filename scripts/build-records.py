#!/usr/bin/env python3 -I
"""Build record.json in every folder whose device.toml describes a wired sensor or actuator.

index.json says a record exists (vendor, model, kind, the order numbers).
record.json is what a controller fetches for one device once someone has
said it is on a point: what the device is, how each connector is wired,
what its signals and their states are called, and the settings it leaves
the factory with. It is device.toml's `[wired]`, `[[signals]]`,
`[[settings]]` and `[[variants]]`, checked and bounded, as JSON, because a
controller reads JSON and not TOML. Format "helmsman-device-record 1"; a
controller refuses anything else.

A folder without `[wired]` (a device reached over a network) gets none.

Usage: python3 -I scripts/build-records.py [--check]
  --check   exit 1 if a record.json differs from what its device.toml says (CI)

Standard library only (tomllib needs Python 3.11).
"""

import json
import pathlib
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORMAT = "helmsman-device-record 1"
NAME = "record.json"
SHORT = 160
MAX_ITEMS = 256  # signals or settings in one record
MAX_VARIANTS = 128
MAX_CONNECTIONS = 32
MAX_VALUES = 32
DIRS = ("in", "out")
TYPES = ("bool", "int", "uint", "float32", "string", "octets", "time", "timespan")


def text(v, what, cap=SHORT):
    if not isinstance(v, str) or not v or len(v) > cap or any(ord(c) < 32 or ord(c) == 127 for c in v):
        raise SystemExit(f"{what}: text of 1..{cap} printable characters, got {v!r:.80}")
    return v


def number(v, what, low, top):
    if isinstance(v, bool) or not isinstance(v, int) or not low <= v <= top:
        raise SystemExit(f"{what}: a number {low}..{top}, got {v!r:.40}")
    return v


def table(v, what):
    if not isinstance(v, dict):
        raise SystemExit(f"{what}: a table, got {type(v).__name__}")
    return v


def rows(v, what, most=MAX_ITEMS):
    if not isinstance(v, list) or len(v) > most:
        raise SystemExit(f"{what}: a list of at most {most}")
    return [table(r, f"{what}[{i}]") for i, r in enumerate(v)]


def optional(out, src, keys, what, cap=SHORT):
    for key in keys:
        if key in src:
            out[key] = text(src[key], f"{what}.{key}", cap)


def values(v, what):
    """A value-to-name table: {"0": "High active"}; TOML's bare keys are already text."""
    v = table(v, what)
    if len(v) > MAX_VALUES:
        raise SystemExit(f"{what}: at most {MAX_VALUES} values")
    return {text(k, f"{what} key", 32): text(name, f"{what}.{k}") for k, name in v.items()}


def record(folder: pathlib.Path, root: pathlib.Path = ROOT) -> dict | None:
    """The record for one folder, or None when its device is not a wired one."""
    t = tomllib.loads((folder / "device.toml").read_text())
    if "wired" not in t:
        return None
    rel = folder.relative_to(root).as_posix()
    dev = table(t.get("device", {}), f"{rel}: device")
    out = {
        "format": FORMAT,
        "folder": rel,
        "vendor": text(dev.get("vendor"), f"{rel}: device.vendor", 120),
        "model": text(dev.get("model"), f"{rel}: device.model", 120),
        "kind": text(dev.get("kind", "other"), f"{rel}: device.kind", 24),
        # Nobody has checked a unit until the folder says when.
        "draft": "checked_on" not in dev,
    }
    optional(out, dev, ("family", "vendor_url"), f"{rel}: device")
    iolink = table(t.get("identity", {}), f"{rel}: identity").get("iolink")
    if iolink is not None:
        iolink = table(iolink, f"{rel}: identity.iolink")
        out["iolink"] = {
            "vendor_id": number(iolink.get("vendor_id"), f"{rel}: identity.iolink.vendor_id", 1, 65535),
            "device_id": number(iolink.get("device_id"), f"{rel}: identity.iolink.device_id", 1, 16777215),
        }
    out["variants"] = []
    for i, v in enumerate(rows(t.get("variants", []), f"{rel}: variants", MAX_VARIANTS)):
        what = f"{rel}: variants[{i}]"
        rec = {"product_id": text(v.get("product_id"), f"{what}.product_id", 120)}
        optional(rec, v, ("name", "description"), what)
        out["variants"].append(rec)

    wired = table(t["wired"], f"{rel}: wired")
    w = {}
    if "sio" in wired:
        if not isinstance(wired["sio"], bool):
            raise SystemExit(f"{rel}: wired.sio: true or false")
        w["sio"] = wired["sio"]
    # Which signal the switching wire carries: never without where it was read.
    if "switching" in wired:
        w["switching"] = text(wired["switching"], f"{rel}: wired.switching")
        w["source"] = text(wired.get("source"), f"{rel}: wired.source (a switching signal needs its source)")
    w["connections"] = []
    for i, c in enumerate(rows(wired.get("connections", []), f"{rel}: wired.connections", MAX_CONNECTIONS)):
        what = f"{rel}: wired.connections[{i}]"
        products = c.get("products", [])
        if not isinstance(products, list) or len(products) > MAX_VARIANTS:
            raise SystemExit(f"{what}.products: a list of at most {MAX_VARIANTS}")
        conn = {
            "type": text(c.get("type"), f"{what}.type", 24),
            "products": [text(p, f"{what}.products", 120) for p in products],
            "wires": [],
        }
        for j, wire in enumerate(rows(c.get("wires", []), f"{what}.wires", 9)):
            ww = f"{what}.wires[{j}]"
            one = {"n": number(wire.get("n"), f"{ww}.n", 1, 9)}
            optional(one, wire, ("function", "color"), ww, 24)
            optional(one, wire, ("name",), ww)
            conn["wires"].append(one)
        w["connections"].append(conn)
    out["wired"] = w

    out["signals"] = []
    for i, s in enumerate(rows(t.get("signals", []), f"{rel}: signals")):
        what = f"{rel}: signals[{i}]"
        if s.get("dir") not in DIRS:
            raise SystemExit(f"{what}.dir: in or out")
        if s.get("type") not in TYPES:
            raise SystemExit(f"{what}.type: one of {', '.join(TYPES)}")
        rec = {"dir": s["dir"], "name": text(s.get("name"), f"{what}.name"), "type": s["type"]}
        optional(rec, s, ("bits",), what, 16)
        optional(rec, s, ("on", "off", "description", "layout"), what)
        if "values" in s:
            rec["values"] = values(s["values"], f"{what}.values")
        out["signals"].append(rec)

    out["settings"] = []
    for i, s in enumerate(rows(t.get("settings", []), f"{rel}: settings")):
        what = f"{rel}: settings[{i}]"
        rec = {
            "name": text(s.get("name"), f"{what}.name"),
            "index": number(s.get("index"), f"{what}.index", 0, 65535),
        }
        if "subindex" in s:
            rec["subindex"] = number(s["subindex"], f"{what}.subindex", 1, 255)
        rec["default"] = text(s.get("default"), f"{what}.default", 32)
        optional(rec, s, ("default_name",), what)
        if "values" in s:
            rec["values"] = values(s["values"], f"{what}.values")
        out["settings"].append(rec)
    return out


def render(rec: dict) -> str:
    return json.dumps(rec, indent=1, ensure_ascii=False) + "\n"


def main(argv: list[str], root: pathlib.Path = ROOT) -> int:
    check = "--check" in argv
    stale, count = [], 0
    for toml in sorted((root / "devices").glob("*/*/device.toml")):
        folder = toml.parent
        rec = record(folder, root)
        target = folder / NAME
        if rec is None:
            if target.exists():
                stale.append(f"{target.relative_to(root)}: its device.toml has no [wired]")
                if not check:
                    target.unlink()
            continue
        count += 1
        want = render(rec)
        if (target.read_text() if target.exists() else "") != want:
            stale.append(f"{target.relative_to(root)}: out of date")
            if not check:
                target.write_text(want)
    if check:
        for line in stale:
            print(line, file=sys.stderr)
        if stale:
            print("run scripts/build-records.py", file=sys.stderr)
            return 1
        print(f"record.json is current in {count} folder(s)")
        return 0
    print(f"{count} record(s), {len(stale)} written or removed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
