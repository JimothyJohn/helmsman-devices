#!/usr/bin/env python3 -I
"""Draft a library folder from an EDS: identity, assemblies and connections, read and not checked.

Reads an EtherNet/IP EDS (from the store docs-fetch.py fills, or a path) and
writes devices/<vendor>/<model>/device.toml and a README.md stub. Everything
in the draft is what the EDS says; nothing is from a unit, so the draft has
no checked_on and says so. Points and their meaning are not in an EDS: a
person or an agent reads them from the manual afterwards.

Usage:
  python3 -I scripts/eds-draft.py show EDS
      print what the EDS says, as JSON
  python3 -I scripts/eds-draft.py draft collect/<vendor>.lock.json FOLDER [--model TEXT] [--force]
      [--eds NAME]
      write FOLDER/device.toml and README.md from the EDS the lock lists for FOLDER
      (the stored file, or the archive member when the EDS came zipped); when
      more than one EDS is in reach (a family package), --eds names the file

An existing device.toml is never overwritten without --force.
Standard library only (Python 3.11).
"""

import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_EDS = 4 * 1024 * 1024
DEVICE_KINDS = {  # CIP device type -> device.toml kind
    0: "other",
    2: "drive",
    7: "remote-io",
    12: "remote-io",
    14: "controller",
    19: "drive",
    24: "remote-io",
    43: "remote-io",  # "Generic Device": what many I/O blocks declare (Balluff BNI EIP)
}


class EdsError(ValueError):
    pass


# --- the EDS grammar: [Section] Keyword = field, field, ... ; with $ comments -


def statements(text: str):
    """(section, keyword, [field text]) for every entry, in order."""
    section = None
    i, n = 0, len(text)
    buf, fields, quoted = [], [], False
    out = []

    def field():
        fields.append("".join(buf).strip())
        buf.clear()

    while i < n:
        c = text[i]
        if quoted:
            if c == "\\" and i + 1 < n:
                buf.append(text[i : i + 2])
                i += 2
                continue
            buf.append(c)
            if c == '"':
                quoted = False
            i += 1
            continue
        if c == '"':
            quoted = True
            buf.append(c)
        elif c == "$":
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        elif c == "[" and not fields and not "".join(buf).strip():
            j = text.find("]", i)
            if j < 0:
                raise EdsError("a section header with no ]")
            section = text[i + 1 : j].strip()
            if not section or len(section) > 64 or "\n" in section:
                raise EdsError(f"bad section name {section[:40]!r}")
            buf.clear()
            i = j + 1
            continue
        elif c == ",":
            field()
        elif c == ";":
            field()
            head = fields[0]
            key, eq, first = head.partition("=")
            if not eq:
                raise EdsError(f"[{section}]: an entry with no '=': {head[:40]!r}")
            if section is None:
                raise EdsError("an entry before any section")
            out.append((section, key.strip(), [first.strip()] + fields[1:]))
            fields.clear()
        else:
            buf.append(c)
        i += 1
    if quoted:
        raise EdsError("a string with no closing quote")
    if fields or "".join(buf).strip():
        raise EdsError("text after the last ';'")
    return out


def string(f: str) -> str | None:
    """A field's string value: adjacent quoted strings joined; None when not a string."""
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', f)
    if not parts or re.sub(r'"(?:[^"\\]|\\.)*"', "", f).strip():
        return None
    s = "".join(parts)
    return "".join(c for c in s if c >= " ")[:200]


def number(f: str) -> int | None:
    f = f.strip()
    try:
        if f.lower().startswith("0x"):
            return int(f, 16)
        if f.isdigit():
            return int(f)
    except ValueError:
        return None
    return None


def resolve_params(path: str, params: dict[str, int]) -> tuple[str, list[str]]:
    """An EPATH with each [ParamN] replaced by that parameter's default byte, and the names used."""
    used = []

    def sub(m):
        name = m.group(1)
        v = params.get(name.lower())
        if v is None or not 0 <= v <= 255:
            return "??"
        used.append(name)
        return f"{v:02X}"

    return re.sub(r"\[\s*(Param\d{1,5})\s*\]", sub, path, flags=re.IGNORECASE), used


def path_instances(path: str) -> list[int]:
    """The instance/connection-point numbers in an EPATH like "20 04 24 80 2C 96 2C 64"."""
    toks = path.split()
    if not toks or any(not re.fullmatch(r"[0-9A-Fa-f]{2}", t) for t in toks):
        return []
    b = [int(t, 16) for t in toks]
    out, i = [], 0
    while i < len(b):
        seg = b[i]
        if seg in (0x24, 0x2C) and i + 1 < len(b):  # 8-bit instance / connection point
            out.append(b[i + 1])
            i += 2
        elif seg in (0x25, 0x2D) and i + 3 < len(b):  # 16-bit, padded
            out.append(b[i + 2] | b[i + 3] << 8)
            i += 4
        elif seg in (0x20, 0x30) and i + 1 < len(b):  # class / attribute
            i += 2
        elif seg in (0x21, 0x31) and i + 3 < len(b):
            i += 4
        else:
            return out
    return out


def parse(data: bytes) -> dict:
    """What a draft needs from an EDS. Raises EdsError on anything it cannot read."""
    if len(data) > MAX_EDS:
        raise EdsError(f"over {MAX_EDS} bytes")
    if b"\x00" in data:
        raise EdsError("binary, not an EDS")
    text = data.decode("utf-8") if _utf8(data) else data.decode("latin-1")
    entries = statements(text.lstrip("﻿"))
    sec = {}
    for s, k, f in entries:
        sec.setdefault(s.lower(), []).append((k, f))

    def one(section, key):
        for k, f in sec.get(section, []):
            if k.lower() == key.lower():
                return f
        return None

    if "device" not in sec:
        raise EdsError("no [Device] section")
    dev = {}
    for key, name, conv in (
        ("VendCode", "vendor_id", number),
        ("ProdType", "device_type", number),
        ("ProdCode", "product_code", number),
        ("MajRev", "major_rev", number),
        ("MinRev", "minor_rev", number),
        ("VendName", "vendor_name", string),
        ("ProdTypeStr", "device_type_name", string),
        ("ProdName", "product_name", string),
        ("Catalog", "catalog", string),
    ):
        f = one("device", key)
        v = conv(f[0]) if f else None
        if v is not None:
            dev[name] = v
    for key in ("vendor_id", "product_code"):
        if not 0 <= dev.get(key, -1) <= 65535:
            raise EdsError(f"[Device] has no {key} 0..65535")
    out = {"device": dev}
    f = one("file", "Revision")
    if f and re.fullmatch(r"\d+\.\d+", f[0]):
        out["file_revision"] = f[0]
    f = one("file", "ModDate")
    if f:
        out["file_date"] = f[0][:20]

    assemblies = []
    for k, f in sec.get("assembly", []):
        m = re.fullmatch(r"Assem(\d{1,5})", k, re.IGNORECASE)
        if not m:
            continue
        rec = {"instance": int(m.group(1))}
        if f and string(f[0]):
            rec["name"] = string(f[0])
        if len(f) > 2 and number(f[2]) is not None:
            rec["bytes"] = number(f[2])
        elif len(f) > 2 and not f[2].strip():
            # No size: the sum of the members' sizes in bits (CIP Vol. 1 7-3.6.11).
            bits = [number(x) for x in f[6::2] if x.strip()]
            if bits and all(b is not None for b in bits) and sum(bits) % 8 == 0:
                rec["bytes"] = sum(bits) // 8
        assemblies.append(rec)
    out["assemblies"] = sorted(assemblies, key=lambda a: a["instance"])

    params = {}  # paramN (lower case) -> default value (field 11), when a number
    ranges = {}  # paramN (lower case) -> (name, min, max, default) when all three are numbers
    for k, f in sec.get("params", []):
        if re.fullmatch(r"Param\d{1,5}", k, re.IGNORECASE) and len(f) > 11 and number(f[11]) is not None:
            params[k.lower()] = number(f[11])
            lo, hi = number(f[9]), number(f[10])
            if lo is not None and hi is not None:
                ranges[k.lower()] = (k, lo, hi, number(f[11]))

    connections = []
    for k, f in sec.get("connection manager", []):
        if not re.fullmatch(r"Connection\d{1,4}", k, re.IGNORECASE) or len(f) < 15:
            continue
        rec = {"entry": k}
        name = string(f[12])
        if name:
            rec["name"] = name
        for idx, key in ((3, "o_to_t_bytes"), (6, "t_to_o_bytes"), (8, "config_bytes")):
            v = number(f[idx])
            if v is not None:
                rec[key] = v
            elif f[idx].strip().lower() in ranges:
                # A size the scanner sets within a range (Phoenix's AXL F BK EIP EF):
                # the assembly's declared size is then a ceiling, not the size.
                name, lo, hi, default = ranges[f[idx].strip().lower()]
                rec[key.replace("_bytes", "_size")] = {
                    "param": name,
                    "min": lo,
                    "max": hi,
                    "default": default,
                }
        p = string(f[14])
        used = []
        if p:
            p, used = resolve_params(p, params)
        inst = path_instances(p) if p else []
        if len(inst) >= 3:
            rec["config_instance"], rec["o_to_t_instance"], rec["t_to_o_instance"] = inst[:3]
        elif len(inst) == 2:
            rec["o_to_t_instance"], rec["t_to_o_instance"] = inst
        if used and len(inst) >= 2:
            rec["from_params"] = used
        connections.append(rec)
    out["connections"] = connections
    return out


def _utf8(b: bytes) -> bool:
    try:
        b.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


# --- the draft -------------------------------------------------------------


def toml_str(s: str) -> str:
    return json.dumps(str(s), ensure_ascii=False)


def pick_connection(eds: dict) -> dict | None:
    """The connection a draft names: the first Exclusive Owner, else the first with both instances."""
    full = [c for c in eds["connections"] if "o_to_t_instance" in c and "t_to_o_instance" in c]
    for c in full:
        if "exclusive" in c.get("name", "").lower() or "owner" in c.get("name", "").lower():
            return c
    return full[0] if full else None


def draft(eds: dict, eds_file: dict, sources: list[dict], vendor: str, model: str) -> str:
    d = eds["device"]
    kind = DEVICE_KINDS.get(d.get("device_type"), "other")
    lines = [
        "# Drafted by scripts/eds-draft.py from the EDS alone. No unit has been checked:",
        "# checked_on, firmware and checked_by stay out until one has, and every value",
        "# below is what the vendor's file says, not what a device did.",
        "[device]",
        f"vendor = {toml_str(vendor)}",
        f"model = {toml_str(model)}",
        f"kind = {toml_str(kind)}",
    ]
    if d.get("catalog"):
        lines.append(f"article = {toml_str(d['catalog'])}")
    lines += ["", "[identity.enip]", f"vendor_id = {d['vendor_id']}", f"product_code = {d['product_code']}"]
    if "device_type" in d:
        lines.append(f"device_type = {d['device_type']}")
    if "major_rev" in d:
        rev = f"{d['major_rev']}.{d.get('minor_rev', 0)}"
        lines.append(f"revisions = [{toml_str(rev)}]   # the EDS's MajRev.MinRev")
    if d.get("product_name"):
        lines.append(f"product_name = {toml_str(d['product_name'])}")
    lines += ["", "[protocols.enip]", 'driver = "enip-io"']
    c = pick_connection(eds)
    sizes = {a["instance"]: a.get("bytes") for a in eds["assemblies"]}
    if c:
        lines.append(f"# from {c['entry']}{' ' + toml_str(c['name']) if c.get('name') else ''}")
        if c.get("from_params"):
            lines.append(
                f"# instances are the defaults of {', '.join(c['from_params'])}: the EDS lets a scanner choose others"
            )
        for role, inst_key, size_key in (
            ("input_assembly", "t_to_o_instance", "t_to_o_bytes"),
            ("output_assembly", "o_to_t_instance", "o_to_t_bytes"),
            ("config_assembly", "config_instance", "config_bytes"),
        ):
            if inst_key not in c:
                continue
            inst = c[inst_key]
            ranged = c.get(size_key.replace("_bytes", "_size"))
            if ranged:
                lines.append(
                    f"# {role}: the size is set by {ranged['param']}: "
                    f"{ranged['min']}..{ranged['max']} bytes, default {ranged['default']}"
                )
                size = None
            else:
                size = c.get(size_key, sizes.get(inst))
            body = f"instance = {inst}" + (f", bytes = {size}" if size is not None else "")
            lines.append(f"{role} = {{ {body} }}")
    lines.append(
        "eds = { "
        + ", ".join(
            f"{k} = {toml_str(eds_file[k]) if isinstance(eds_file[k], str) else eds_file[k]}"
            for k in ("name", "size", "sha256", "url", "terms")
            if k in eds_file
        )
        + " }"
    )
    for s in sources:
        lines += ["", "[[sources]]", f"title = {toml_str(s['title'])}", f"sha256 = {toml_str(s['sha256'])}"]
        lines.append(f"where = {toml_str(s['where'])}")
    return "\n".join(lines) + "\n"


def readme(eds: dict, vendor: str, model: str, sources: list[dict]) -> str:
    d = eds["device"]
    rows = "\n".join(f"| {s['title']} | `{s['sha256'][:16]}…` | {s['where']} |" for s in sources)

    def size(c, d):
        r = c.get(f"{d}_size")
        return f"{r['min']}..{r['max']} ({r['param']})" if r else c.get(f"{d}_bytes", "")

    conns = "\n".join(
        f"| {c['entry']} | {c.get('name', '')} | {c.get('t_to_o_instance', '')} / {size(c, 't_to_o')} "
        f"| {c.get('o_to_t_instance', '')} / {size(c, 'o_to_t')} | {c.get('config_instance', '')} |"
        for c in eds["connections"]
    )
    return f"""> **Draft from documents.** No unit has been checked; every value here is the
> EDS's, read by `scripts/eds-draft.py`. Points and their meaning are still to be
> read from the manual, with its page for each.

# {vendor} {model}

EDS identity: vendor {d["vendor_id"]} {d.get("vendor_name", "")}, product code
{d["product_code"]}, device type {d.get("device_type", "?")} {d.get("device_type_name", "")},
revision {d.get("major_rev", "?")}.{d.get("minor_rev", "?")}; EDS file revision
{eds.get("file_revision", "?")} ({eds.get("file_date", "no date")}).

## Connections the EDS offers

| entry | name | input (T->O) instance / bytes | output (O->T) instance / bytes | config instance |
| --- | --- | --- | --- | --- |
{conns or "| none read | | | | |"}

## Sources

| what | SHA-256 | where |
| --- | --- | --- |
{rows}

Vendor files are not in this repository; fetch them with
`scripts/docs-fetch.py` from the `collect/` file that lists them and check the hash.
"""


def file_name(vendor_name: str) -> str:
    """The vendor's file name as one a box reads (helmsman-project devlib
    `file_ok`: letters, digits, `.`, `_`, `-`): each run of anything else,
    spaces first, becomes one `_`. The sha256 still names the vendor's file."""
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", vendor_name).strip("_")[:120]
    if not name or name in (".", ".."):
        raise SystemExit(f"{vendor_name!r}: nothing of it is a file name")
    return name


def eds_from_lock(lock: dict, folder: str, store_dir: pathlib.Path, choose: str | None = None):
    """(EDS bytes, its file record, the folder's sources) from the lock and the store.

    A family package holds many models' EDS; with more than one in reach, choose
    (a file name) must say which, and nothing is guessed.
    """
    docs = [d for d in lock["docs"].items() if folder in d[1].get("folders", [])]
    if not docs:
        raise SystemExit(f"the lock lists nothing for {folder}")
    candidates = []
    for url, d in docs:
        if d["kind"] != "eds":
            continue
        if d["type"] == "eds":
            candidates.append((d["name"], d["sha256"], d["size"], url, d))
        for m in d.get("members", []):
            if m["type"] == "eds":
                candidates.append((pathlib.PurePosixPath(m["name"]).name, m["sha256"], m["size"], url, d))
    if not candidates:
        raise SystemExit(f"the lock has no EDS for {folder}")
    names = sorted(c[0] for c in candidates)
    if choose is not None:
        candidates = [c for c in candidates if c[0] == choose]
        if len(candidates) != 1:
            raise SystemExit(f"--eds {choose}: not exactly one of: {', '.join(names)}")
    elif len(candidates) > 1:
        raise SystemExit(f"{len(candidates)} EDS for {folder}; name one with --eds: {', '.join(names)}")
    name, sha, size, url, d = candidates[0]
    p = store_dir / "sha256" / sha
    if not p.is_file():
        raise SystemExit(f"{sha[:12]} is not in the store: run scripts/docs-fetch.py first")
    data = p.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha:
        raise SystemExit(f"{p}: does not match its hash")
    eds_file = {"name": file_name(name), "size": size, "sha256": sha, "url": url}
    if d.get("members"):
        eds_file["url"] = f"{url} (member of {d['name']})"
    eds_file["terms"] = d.get("terms", "none stated; not redistributed here")
    sources = [
        {
            "title": e["title"],
            "sha256": e["sha256"],
            "where": f"{u}; retrieved {e['retrieved'][:10]}; not redistributed here",
        }
        for u, e in sorted(docs, key=lambda x: (x[1]["kind"], x[0]))
    ]
    return data, eds_file, sources


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[0] == "show":
        path = pathlib.Path(argv[1])
        if not path.is_file():
            raise SystemExit(f"{argv[1]}: no such file")
        try:
            print(json.dumps(parse(path.read_bytes()), indent=1, ensure_ascii=False))
        except EdsError as e:
            raise SystemExit(f"{argv[1]}: {e}") from None
        return 0
    if len(argv) >= 3 and argv[0] == "draft":
        args = argv[1:]
        force = "--force" in args
        if force:
            args.remove("--force")
        model = choose = vendor = None
        if "--vendor" in args:
            i = args.index("--vendor")
            vendor = args[i + 1] if i + 1 < len(args) else None
            del args[i : i + 2]
        if "--eds" in args:
            i = args.index("--eds")
            choose = args[i + 1] if i + 1 < len(args) else None
            del args[i : i + 2]
        if "--model" in args:
            i = args.index("--model")
            model = args[i + 1] if i + 1 < len(args) else None
            del args[i : i + 2]
        if len(args) != 2:
            raise SystemExit("draft needs LOCK FOLDER")
        lock = json.loads(pathlib.Path(args[0]).read_text())
        folder = args[1].rstrip("/")
        if not re.fullmatch(r"devices/[a-z0-9][a-z0-9_.-]{0,63}/[a-z0-9][a-z0-9_.-]{0,63}", folder):
            raise SystemExit("FOLDER must be devices/<vendor>/<model>, a-z 0-9 . _ -")
        parts = folder.split("/")
        data, eds_file, sources = eds_from_lock(lock, folder, ROOT / "cache", choose)
        try:
            eds = parse(data)
        except EdsError as e:
            raise SystemExit(f"{eds_file['name']}: {e}") from None
        vendor = vendor or eds["device"].get("vendor_name") or parts[1]
        model = model or eds["device"].get("product_name") or parts[2]
        target = ROOT / folder
        if (target / "device.toml").exists() and not force:
            raise SystemExit(f"{folder}/device.toml exists: --force to overwrite")
        target.mkdir(parents=True, exist_ok=True)
        (target / "device.toml").write_text(draft(eds, eds_file, sources, vendor, model))
        if not (target / "README.md").exists() or force:
            (target / "README.md").write_text(readme(eds, vendor, model, sources))
        print(f"wrote {folder}/device.toml and README.md (draft from {eds_file['name']})")
        return 0
    print(__doc__.split("Usage:")[1].split("An existing")[0], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
