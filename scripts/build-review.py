#!/usr/bin/env python3 -I
"""Build review.json: every claim each device.toml makes, for a page where people check them.

index.json is what a controller looks a device up in, and stays small.
review.json is what a person reads: the identity and assemblies, each
point with its meaning and the page it came from, the documents, the
wiring note. A page renders it, so every text is bounded and printable
and every number is a number; a folder that breaks that fails the build.
Format "helmsman-devices-review 1".

Usage: python3 -I scripts/build-review.py [--check]
  --check   exit 1 if review.json differs from what the folders say (CI)

Standard library only (tomllib needs Python 3.11).
"""

import datetime
import json
import pathlib
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORMAT = "helmsman-devices-review 1"
SHORT = 160
LONG = 600
MAX_ITEMS = 256  # points or sources in one folder
HEX = set("0123456789abcdef")


def text(v, what, cap=SHORT):
    if not isinstance(v, str) or not v or len(v) > cap or any(ord(c) < 32 or ord(c) == 127 for c in v):
        raise SystemExit(f"{what}: text of 1..{cap} printable characters, got {v!r:.80}")
    return v


def number(v, what, top=65535):
    if isinstance(v, bool) or not isinstance(v, int) or not 0 <= v <= top:
        raise SystemExit(f"{what}: a number 0..{top}, got {v!r:.40}")
    return v


def date(v, what):
    if isinstance(v, datetime.date) and not isinstance(v, datetime.datetime):
        return v.isoformat()
    if isinstance(v, str) and len(v) == 10:
        try:
            return datetime.date.fromisoformat(v).isoformat()
        except ValueError:
            pass
    raise SystemExit(f"{what}: a date YYYY-MM-DD, got {v!r:.40}")


def table(v, what):
    if not isinstance(v, dict):
        raise SystemExit(f"{what}: a table, got {type(v).__name__}")
    return v


def rows(v, what):
    if not isinstance(v, list) or len(v) > MAX_ITEMS:
        raise SystemExit(f"{what}: a list of at most {MAX_ITEMS}")
    return [table(r, f"{what}[{i}]") for i, r in enumerate(v)]


def optional(out, src, keys, what, cap=SHORT):
    for key in keys:
        if key in src:
            out[key] = text(src[key], f"{what}.{key}", cap)


def assembly(v, what):
    v = table(v, what)
    out = {"instance": number(v.get("instance"), f"{what}.instance")}
    if "bytes" in v:
        out["bytes"] = number(v["bytes"], f"{what}.bytes")
    return out


def entry(folder: pathlib.Path) -> dict:
    t = tomllib.loads((folder / "device.toml").read_text())
    rel = folder.relative_to(ROOT).as_posix()
    dev = table(t.get("device", {}), f"{rel}: device")
    out = {
        "folder": rel,
        "vendor": text(dev.get("vendor"), f"{rel}: device.vendor"),
        "model": text(dev.get("model"), f"{rel}: device.model"),
    }
    optional(out, dev, ("channels", "firmware"), f"{rel}: device")
    if "checked_on" in dev:
        out["checked_on"] = date(dev["checked_on"], f"{rel}: device.checked_on")
    protocols = table(t.get("protocols", {}), f"{rel}: protocols")
    if "enip" in protocols:
        p, what = table(protocols["enip"], f"{rel}: protocols.enip"), f"{rel}: protocols.enip"
        enip = {"map": "map" in p}
        ident = table(t.get("identity", {}), f"{rel}: identity").get("enip")
        if ident is not None:
            ident, iw = table(ident, f"{rel}: identity.enip"), f"{rel}: identity.enip"
            rec = {
                k: number(ident[k], f"{iw}.{k}")
                for k in ("vendor_id", "product_code", "device_type")
                if k in ident
            }
            if "revisions" in ident:
                revs = ident["revisions"]
                if not isinstance(revs, list) or len(revs) > 32:
                    raise SystemExit(f"{iw}.revisions: a list of at most 32")
                rec["revisions"] = [text(r, f"{iw}.revisions", 16) for r in revs]
            optional(rec, ident, ("product_name",), iw)
            enip["identity"] = rec
        for key, name in (
            ("input_assembly", "input"),
            ("output_assembly", "output"),
            ("config_assembly", "config"),
        ):
            if key in p:
                enip[name] = assembly(p[key], f"{what}.{key}")
        if "eds" in p:
            enip["eds"] = text(table(p["eds"], f"{what}.eds").get("name"), f"{what}.eds.name")
        out["enip"] = enip
    if "modbus" in protocols:
        p, what = table(protocols["modbus"], f"{rel}: protocols.modbus"), f"{rel}: protocols.modbus"
        modbus = {"map": "map" in p}
        if "port" in p:
            modbus["port"] = number(p["port"], f"{what}.port")
        if "unit" in p:
            modbus["unit"] = number(p["unit"], f"{what}.unit", 255)
        out["modbus"] = modbus
    points = []
    for i, p in enumerate(rows(t.get("points", []), f"{rel}: points")):
        what = f"{rel}: points[{i}]"
        rec = {"name": text(p.get("name"), f"{what}.name")}
        optional(rec, p, ("enip", "modbus"), what)
        optional(rec, p, ("meaning", "source"), what, LONG)
        points.append(rec)
    out["points"] = points
    sources = []
    for i, s in enumerate(rows(t.get("sources", []), f"{rel}: sources")):
        what = f"{rel}: sources[{i}]"
        rec = {"title": text(s.get("title"), f"{what}.title")}
        if "sha256" in s:
            sha = s["sha256"]
            if not isinstance(sha, str) or len(sha) != 64 or set(sha.lower()) - HEX:
                raise SystemExit(f"{what}.sha256: 64 hex digits")
            rec["sha256"] = sha.lower()
        optional(rec, s, ("where",), what, LONG)
        sources.append(rec)
    out["sources"] = sources
    if "wiring" in t:
        w = table(t["wiring"], f"{rel}: wiring")
        rec = {"note": text(w.get("note"), f"{rel}: wiring.note", LONG)}
        optional(rec, w, ("source",), f"{rel}: wiring", LONG)
        out["wiring"] = rec
    return out


def main() -> int:
    folders = sorted(p.parent for p in (ROOT / "devices").glob("*/*/device.toml"))
    review = {"format": FORMAT, "devices": [entry(f) for f in folders]}
    text_out = json.dumps(review, indent=1, ensure_ascii=False) + "\n"
    target = ROOT / "review.json"
    if "--check" in sys.argv[1:]:
        current = target.read_text() if target.exists() else ""
        if current != text_out:
            print("review.json is out of date: run scripts/build-review.py", file=sys.stderr)
            return 1
        print(f"review.json is current ({len(review['devices'])} device(s))")
        return 0
    target.write_text(text_out)
    print(f"wrote review.json: {len(review['devices'])} device(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
