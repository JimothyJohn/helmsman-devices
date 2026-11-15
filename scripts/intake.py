#!/usr/bin/env python3 -I
"""Turn approved "New device:" issues into work items an agent can act on without reading the issues.

An issue is public text from a stranger. An agent that reads it can be
told things by it. So the agent never does: this script reads the issues,
and what comes out is a short list of checked fields and nothing else:
a vendor and a model (a few words in a narrow alphabet), the protocols
ticked, and https links to public hosts. No sentence a person wrote reaches the
output, and the reason an issue was skipped is one of this file's own
phrases.

Only an issue a maintainer has labelled `intake` is taken. Applying a
label needs triage rights on the repository, so the label is the gate: a
person has looked at the issue and said "draft this one".

Usage:
  gh issue list --state open --label intake --limit 50 \\
      --json number,title,body,labels | python3 -I scripts/intake.py

Prints JSON: {"items": [...], "skipped": [{"issue": N, "why": "..."}]}.
Each item: issue, vendor, model, folder, in_library, protocols,
product_page, links, has_unit, could_send. docs/intake.md says what an
agent does with it.

Exit 0 when the input was read, 2 when it was not the JSON `gh` prints.
Standard library only (Python 3.11).
"""

import ipaddress
import json
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABEL = "intake"
PREFIX = "New device:"
MAX_ISSUES = 200
MAX_BODY = 20_000
MAX_LINKS = 10
MAX_URL = 300
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._+/()&-]{0,39}", re.ASCII)
MAX_WORDS = {"vendor": 3, "model": 6}  # "Phoenix Contact"; "ET 200SP IM 155-6 MF HF"
URL = re.compile(r"https://[A-Za-z0-9.-]{1,253}(?:/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]*)?", re.ASCII)
HOST_LABEL = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", re.ASCII)
PROTOCOLS = (("enip", "ethernet/ip"), ("modbus", "modbus tcp"))
EMPTY = {"", "_no response_", "none", "n/a"}


class Skip(Exception):
    """An issue this script will not turn into an item. The message is one of this file's phrases."""


def field(body, label):
    """One answer from an issue: the form's '### Label' block, or a 'Label: value' line. '' when absent."""
    m = re.search(
        rf"^###[ \t]+{re.escape(label)}[ \t]*\n(.*?)(?=^###[ \t]|\Z)",
        body,
        re.DOTALL | re.MULTILINE | re.IGNORECASE,
    )
    if m:
        return m.group(1).strip()
    m = re.search(rf"^{re.escape(label)}[^:\n]{{0,60}}:[ \t]*(.*)$", body, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def name(value, what):
    if "\n" in value or "\t" in value:
        raise Skip(f"the {what} is missing or is not a plain name")
    value = " ".join(value.split(" "))
    while "  " in value:
        value = value.replace("  ", " ")
    if not NAME.fullmatch(value) or value.lower() in EMPTY or len(value.split(" ")) > MAX_WORDS[what]:
        raise Skip(f"the {what} is missing or is not a plain name")
    return value


def link(text):
    """text as an https link to a public host, or None."""
    if len(text) > MAX_URL or not URL.fullmatch(text):
        return None
    try:
        u = urllib.parse.urlsplit(text)
        port = u.port
    except ValueError:
        return None
    host = u.hostname or ""
    if u.scheme != "https" or port is not None or u.username is not None or u.password is not None:
        return None
    if "@" in u.netloc or "." not in host or host.endswith(".") or len(host) > 253:
        return None
    labels = host.split(".")
    if not all(HOST_LABEL.fullmatch(part) for part in labels) or labels[-1].isdigit():
        return None
    try:
        ipaddress.ip_address(host)
        return None  # an address, not a name
    except ValueError:
        pass
    if labels[-1].lower() in ("localhost", "local", "internal", "lan", "home", "invalid", "test", "example"):
        return None
    return urllib.parse.urlunsplit(("https", host.lower(), u.path, u.query, ""))


def links(text):
    """The https links in a block of text. A link is taken whole or not at all: no prefix of a longer token."""
    out = []
    for token in re.split(r"[\s<>\"'`()\[\]{}|\\^]+", text):
        if not token.startswith("https://"):
            continue
        u = link(token.rstrip(".,;:!?"))
        if u and u not in out:
            out.append(u)
        if len(out) == MAX_LINKS:
            break
    return out


def ticked(body, phrase):
    """A form checkbox ('- [x] phrase') or the site's line ('phrase...: yes')."""
    p = re.escape(phrase)
    return bool(
        re.search(rf"^[ \t]*-[ \t]*\[[xX]\][ \t]*{p}", body, re.MULTILINE | re.IGNORECASE)
        or re.search(rf"^{p}[^:\n]{{0,60}}:[ \t]*yes\b", body, re.MULTILINE | re.IGNORECASE)
    )


def folder(vendor, model):
    def slug(s):
        return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

    v, m = slug(vendor), slug(model)
    if not v or not m:
        raise Skip("the vendor or model has no letters or digits")
    return f"devices/{v}/{m}"


def item(issue, known):
    if not isinstance(issue, dict):
        raise Skip("not an issue")
    number, title, body = issue.get("number"), issue.get("title"), issue.get("body")
    if isinstance(number, bool) or not isinstance(number, int) or not 0 < number < 10**9:
        raise Skip("no issue number")
    labels = issue.get("labels")
    names = (
        {lab.get("name") for lab in labels if isinstance(lab, dict)} if isinstance(labels, list) else set()
    )
    if LABEL not in names:
        raise Skip(f"not labelled {LABEL}")
    if not isinstance(title, str) or not title.startswith(PREFIX):
        raise Skip(f"the title does not start with {PREFIX}")
    if not isinstance(body, str) or len(body) > MAX_BODY:
        raise Skip("no body, or a body too long to read")
    body = body.replace("\r\n", "\n").replace("\r", "\n")
    vendor = name(field(body, "Vendor"), "vendor")
    model = name(field(body, "Model"), "model")
    path = folder(vendor, model)
    proto_text = (field(body, "Protocols") or "").lower()
    protocols = [
        key
        for key, phrase in PROTOCOLS
        if ticked(body, phrase)
        or (phrase in proto_text and "[x]" not in proto_text and "[ ]" not in proto_text)
    ]
    page = links(field(body, "Product page"))
    found = [u for u in links(field(body, "Documents you know of")) if u not in page[:1]]
    return {
        "issue": number,
        "vendor": vendor,
        "model": model,
        "folder": path,
        "in_library": path in known,
        "protocols": protocols,
        "product_page": page[0] if page else None,
        "links": found,
        "has_unit": ticked(body, "I have one and can run a read-only test")
        or ticked(body, "I have a unit and can run a read-only test"),
        "could_send": ticked(body, "I could send one to the bench")
        or ticked(body, "I could send a unit to the bench"),
    }


def known_folders():
    try:
        index = json.loads((ROOT / "index.json").read_text())
        return {
            d["folder"] for d in index["devices"] if isinstance(d, dict) and isinstance(d.get("folder"), str)
        }
    except (OSError, ValueError, KeyError, TypeError):
        return set()


def main(stream=None):
    try:
        issues = json.loads((stream or sys.stdin).read(8 * 1024 * 1024))
    except ValueError:
        issues = None
    if not isinstance(issues, list):
        print(
            "intake.py reads the JSON list that `gh issue list --json number,title,body,labels` prints",
            file=sys.stderr,
        )
        return 2
    known, items, skipped, seen = known_folders(), [], [], set()
    for issue in issues[:MAX_ISSUES]:
        try:
            it = item(issue, known)
            if it["folder"] in seen:
                raise Skip("the same device as an earlier issue in this run")
            seen.add(it["folder"])
            items.append(it)
        except Skip as why:
            n = issue.get("number") if isinstance(issue, dict) else None
            skipped.append(
                {"issue": n if isinstance(n, int) and not isinstance(n, bool) else None, "why": str(why)}
            )
    print(json.dumps({"items": items, "skipped": skipped}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
