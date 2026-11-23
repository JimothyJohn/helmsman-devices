#!/usr/bin/env python3 -I
"""Find a device in the library: by category, by words, by what the wire says.

Reads index.json and nothing else: no network, no vendor file. With no
arguments it lists the categories; a category lists its devices; words
narrow any list. Each line ends with what the folder gives a project, and
`scripts/use.py <folder>` prints how to add the one you pick.

Usage: python3 -I scripts/find.py [options] [CATEGORY] [WORD ...]
  CATEGORY          a category id from the first list (drive, io-block, ...)
  WORD ...          every word must be in the vendor, model, channels, an order number or
                    the folder: "relay", "8 di", "powerflex 525"
  --protocol NAME   only devices that speak it: enip, modbus or iolink
  --id V:P          the EtherNet/IP vendor id and product code ListIdentity gave (1:9)
  --ready           only devices whose folder has a profile or a map: the channels are named already
  --checked         only devices checked on a unit
  --json            the matches as JSON, one object each, for a program
  --index PATH      another index.json than this checkout's

Exit 0 with matches, 1 with none, 2 for a bad argument.
Standard library only, Python 3.9 or later.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORMAT = "helmsman-devices-index 1"
MAX_BYTES = 4 << 20  # what a box reads at most (helmsman-project devlib)
PROTOCOLS = ("enip", "modbus", "iolink")
FLAGS = ("--ready", "--checked", "--json")
VALUED = ("--protocol", "--id", "--index")


class Bad(Exception):
    """An argument or an index this script refuses; the text says why."""


def printable(v, limit=200):
    """Text from the index as one terminal line: no control character survives."""
    s = v if isinstance(v, str) else ""
    return "".join(c if c.isprintable() else "?" for c in s)[:limit]


def load(path):
    try:
        raw = pathlib.Path(path).read_bytes()
    except OSError as e:
        raise Bad(f"{path}: {e.strerror or e}") from None
    if len(raw) > MAX_BYTES:
        raise Bad(f"{path}: over {MAX_BYTES} bytes")
    try:
        index = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as e:
        raise Bad(f"{path}: not JSON: {e}") from None
    if not isinstance(index, dict) or index.get("format") != FORMAT:
        raise Bad(f"{path}: not a {FORMAT!r} file")
    devices = index.get("devices")
    if not isinstance(devices, list) or not all(isinstance(d, dict) for d in devices):
        raise Bad(f"{path}: devices: not a list of entries")
    cats = index.get("categories", [])
    if not isinstance(cats, list) or not all(isinstance(c, dict) for c in cats):
        raise Bad(f"{path}: categories: not a list")
    return cats, devices


def speaks(d):
    """The protocol names of an entry: its protocols' keys, and iolink for a wired device."""
    p = d.get("protocols")
    names = list(p) if isinstance(p, dict) else []
    ident = d.get("identity")
    if isinstance(ident, dict) and "iolink" in ident:
        names.append("iolink")
    return names


def gives(d):
    """What the folder gives a project, best first, as far as the index says."""
    has = []
    if d.get("profile"):
        has.append("profile")
    p = d.get("protocols") if isinstance(d.get("protocols"), dict) else {}
    if any(isinstance(v, dict) and v.get("map") for v in p.values()):
        has.append("map")
    if any(isinstance(v, dict) and v.get("eds") for v in p.values()):
        has.append("eds")
    if d.get("record"):
        has.append("record")
    n = d.get("points")
    if isinstance(n, int) and not isinstance(n, bool) and n > 0:
        has.append(f"{n} point{'s' if n != 1 else ''}")
    return has


def haystack(d):
    products = d.get("products") if isinstance(d.get("products"), list) else []
    parts = [d.get("vendor"), d.get("model"), d.get("channels"), d.get("folder"), *products]
    return " ".join(p for p in parts if isinstance(p, str)).casefold()


def parse_id(v):
    a, sep, b = v.partition(":")
    if not sep or not a.isdigit() or not b.isdigit() or int(a) > 65535 or int(b) > 65535:
        raise Bad(f"--id: VENDOR:PRODUCT, two numbers 0..65535 (1:9), got {v!r}")
    return int(a), int(b)


def parse_args(argv):
    opts = {"words": []}
    it = iter(argv)
    for a in it:
        if a in FLAGS:
            opts[a] = True
        elif a in VALUED:
            v = next(it, None)
            if v is None:
                raise Bad(f"{a}: needs a value")
            opts[a] = v
        elif a.startswith("-"):
            raise Bad(f"{a}: not an option (python3 -I scripts/find.py --help)")
        else:
            opts["words"].append(a)
    if "--protocol" in opts and opts["--protocol"] not in PROTOCOLS:
        raise Bad(f"--protocol: one of {', '.join(PROTOCOLS)}")
    if "--id" in opts:
        opts["--id"] = parse_id(opts["--id"])
    return opts


def matches(devices, category, opts):
    words = [w.casefold() for w in opts["words"]]
    out = []
    for d in devices:
        if category and d.get("category") != category:
            continue
        if "--protocol" in opts and opts["--protocol"] not in speaks(d):
            continue
        if "--id" in opts:
            ident = d.get("identity") if isinstance(d.get("identity"), dict) else {}
            enip = ident.get("enip") if isinstance(ident.get("enip"), dict) else {}
            if (enip.get("vendor_id"), enip.get("product_code")) != opts["--id"]:
                continue
        if opts.get("--ready") and not {"profile", "map"} & set(gives(d)):
            continue
        if opts.get("--checked") and not d.get("checked_on"):
            continue
        hay = haystack(d)
        if all(w in hay for w in words):
            out.append(d)
    return sorted(out, key=lambda d: (str(d.get("vendor")).casefold(), str(d.get("model")).casefold()))


def list_categories(cats, devices):
    counts = {}
    for d in devices:
        counts[d.get("category")] = counts.get(d.get("category"), 0) + 1
    width = max((len(str(c.get("id"))) for c in cats), default=0)
    print(
        f"{len(devices)} devices. A category lists its devices: python3 -I scripts/find.py CATEGORY [WORD ...]\n"
    )
    for c in cats:
        cid = printable(c.get("id"), 40)
        print(f"  {cid:<{width}}  {counts.get(c.get('id'), 0):>4}  {printable(c.get('label'))}")
    print("\nWords alone search every category: python3 -I scripts/find.py powerflex 525")


def list_devices(found, label):
    rows = [
        (
            printable(d.get("folder")),
            f"{printable(d.get('vendor'), 40)} {printable(d.get('model'), 60)}",
            printable(d.get("channels"), 60) or "-",
            ",".join(speaks(d)) or "-",
            ", ".join(gives(d)) or "identity only",
            printable(d.get("checked_on"), 10) or "documents",
        )
        for d in found
    ]
    widths = [max(len(r[k]) for r in rows) for k in range(5)]
    print(f"{len(found)} {label}\n")
    for r in rows:
        print("  " + "  ".join(f"{r[k]:<{widths[k]}}" for k in range(5)) + "  " + r[5])
    print("\nColumns: folder, device, channels, speaks, what the folder gives a project")
    print("(profile, map, eds, record, documented points), checked on a unit or from documents.")
    print(f"Next: python3 -I scripts/use.py {rows[0][0]}")


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        return 0
    try:
        opts = parse_args(argv)
        cats, devices = load(opts.get("--index", ROOT / "index.json"))
    except Bad as e:
        print(f"find.py: {e}", file=sys.stderr)
        return 2
    ids = [c.get("id") for c in cats]
    category = None
    if opts["words"] and opts["words"][0] in ids:
        category = opts["words"].pop(0)
    narrowed = (
        category or opts["words"] or any(k in opts for k in ("--protocol", "--id", "--ready", "--checked"))
    )
    if not narrowed and not opts.get("--json"):
        list_categories(cats, devices)
        return 0
    found = matches(devices, category, opts)
    if opts.get("--json"):
        for d in found:
            print(json.dumps({**d, "gives": gives(d)}, ensure_ascii=False))
        return 0 if found else 1
    if not found:
        print("nothing matches. The categories:", file=sys.stderr)
        print("  " + " ".join(printable(i, 40) for i in ids), file=sys.stderr)
        return 1
    n = "device" if len(found) == 1 else "devices"
    label = next((printable(c.get("label")) for c in cats if c.get("id") == category), "")
    list_devices(found, f"{n} under {label}" if label else n)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
