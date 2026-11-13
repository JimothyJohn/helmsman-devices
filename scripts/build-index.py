#!/usr/bin/env python3 -I
"""Build index.json from every devices/<vendor>/<model>/device.toml.

The index is what a Helmsman controller (or its canvas) fetches to look a
device up before anything is generated: identity first (ListIdentity's
vendor id and product code), then vendor and model text. Format
"helmsman-devices-index 1"; a controller refuses anything else.

Usage: python3 -I scripts/build-index.py [--check]
  --check   exit 1 if index.json differs from what the folders say (CI)

Standard library only (tomllib needs Python 3.11).
"""

import json
import pathlib
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORMAT = "helmsman-devices-index 1"
TEXT_MAX = 120


def text(v, what):
    if not isinstance(v, str) or not v or len(v) > TEXT_MAX or any(ord(c) < 32 for c in v):
        raise SystemExit(f"{what}: text of 1..{TEXT_MAX} printable characters, got {v!r}")
    return v


def entry(folder: pathlib.Path) -> dict:
    t = tomllib.loads((folder / "device.toml").read_text())
    dev = t.get("device", {})
    rel = folder.relative_to(ROOT).as_posix()
    out = {
        "folder": rel,
        "vendor": text(dev.get("vendor"), f"{rel}: device.vendor"),
        "model": text(dev.get("model"), f"{rel}: device.model"),
        "kind": text(dev.get("kind", "other"), f"{rel}: device.kind"),
    }
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
    if ident:
        out["identity"] = ident
    protocols = {}
    for name, p in t.get("protocols", {}).items():
        driver = text(p.get("driver"), f"{rel}: protocols.{name}.driver")
        if driver not in ("enip-io", "modbus-tcp", "logix-tag"):
            raise SystemExit(f"{rel}: protocols.{name}.driver: not a Helmsman driver: {driver}")
        rec = {"driver": driver}
        for key in ("map", "profile"):
            if key in p:
                rec[key] = text(p[key], f"{rel}: protocols.{name}.{key}")
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
                "name": text(eds.get("name"), f"{rel}: eds.name"),
                "size": int(eds.get("size", 0)),
                "sha256": sha.lower(),
            }
        protocols[name] = rec
    if protocols:
        out["protocols"] = protocols
    return out


def main() -> int:
    folders = sorted(p.parent for p in (ROOT / "devices").glob("*/*/device.toml"))
    index = {"format": FORMAT, "devices": [entry(f) for f in folders]}
    seen = set()
    for d in index["devices"]:
        key = json.dumps(d.get("identity"), sort_keys=True)
        if d.get("identity") and key in seen:
            raise SystemExit(f"{d['folder']}: the same identity as another folder")
        seen.add(key)
    text_out = json.dumps(index, indent=1, ensure_ascii=False) + "\n"
    target = ROOT / "index.json"
    if "--check" in sys.argv[1:]:
        current = target.read_text() if target.exists() else ""
        if current != text_out:
            print("index.json is out of date: run scripts/build-index.py", file=sys.stderr)
            return 1
        print(f"index.json is current ({len(index['devices'])} device(s))")
        return 0
    target.write_text(text_out)
    print(f"wrote index.json: {len(index['devices'])} device(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
