---
name: collect-docs
description: Find and collect the vendor documents (EDS, GSDML, ESI, manuals, register maps, release notes) for I/O modules and drives, fetch them safely into the store, and draft their library folders. Use when asked to add a device or family to the library, "collect docs for X", "find the EDS for X", refresh a vendor's files, or work through collect/families.toml.
---

# Collect device documents

The pipeline is three steps, each leaving a committed record:

1. **Find** (you, with WebSearch and WebFetch) → `collect/<vendor>.toml`, one
   `[[doc]]` per document: which URL holds which file for which library folder,
   and how it was found.
2. **Fetch** (`scripts/docs-fetch.py`) → the files in `cache/sha256/` (and the
   private bucket when `HELMSMAN_DOCS_BUCKET` is set), and
   `collect/<vendor>.lock.json`: name, size, SHA-256, final URL, date.
3. **Draft** (`scripts/eds-draft.py draft`) → `devices/<vendor>/<model>/device.toml`
   and a README stub from the EDS: identity, assemblies, connections. Nothing in a
   draft is checked on a unit.

Then a PR into `dev`, one per family, opened ready so auto-merge takes it.

## 1. Find

Work from `collect/families.toml` (the list of families and models wanted) or the
ask. For each model:

- Search the vendor's own site first: `"<vendor> <model> EDS"`,
  `"<model> manual pdf"`, `"<model> GSDML"`, `site:<vendor domain> <model>`.
  Open the product page with WebFetch and take the download links from it.
- **Every URL comes from a page you saw.** Never build one from a pattern you
  expect; a vendor's portal changes and a guessed URL fetches someone's login page.
- **The ODVA marketplace** (`marketplace.odva.org/products/...`) lists the EDS a
  vendor submitted for conformance, with a direct file link. Try it for any
  EtherNet/IP device whose vendor page builds its downloads in JavaScript (WAGO's
  does: a page fetch sees no links). Some devices write their own EDS (Beckhoff's
  EK9500): then there is no file to collect, only the manual's page saying so.
- Prefer the vendor's domain. A mirror (a university wiki, a distributor) only
  when the vendor's link serves HTML instead of the file; say so in `found`.
- One `[[doc]]` per file (a URL appears once). An EDS that ships in a zip is
  `kind = "eds"` with the zip's URL; the fetcher records each member. A family
  package (Turck's TBEN-S zip holds 21 EDS) is one doc with
  `folders = [...]`, and the draft names its member with `--eds`.
- `found` says how: `"2026-11-14 search: turck tben-s2-8dxp eds; product page https://..."`.
- `terms`: only what the page or file says about redistribution, quoted short.
  Silence is `"none stated"`, not a guess. Nothing is committed either way.
- A file behind a login or a form: leave it out and add a `# behind login: <page>`
  comment beside the folder's entries, so the next person does not search again.

Kinds: `eds`, `gsdml`, `esi`, `manual`, `release-notes`, `register-map`,
`datasheet`, `archive`. Folder names follow the existing ones:
`devices/<vendor-lowercase>/<model-lowercase-dashed>`.

## 2. Fetch

```sh
python3 -I scripts/docs-fetch.py collect/<vendor>.toml
HELMSMAN_DOCS_BUCKET=<bucket> python3 -I scripts/docs-fetch.py collect/<vendor>.toml   # also to S3
```

Python 3.11+ (Homebrew's `python3`; Apple's 3.9 has no `tomllib`). Internet only:
the fetcher refuses every private, loopback, link-local and CGNAT address, so the
macOS LAN rule does not apply to it.

Each line is `fetched`, `stored` (already in the store, no request), `changed`
(the vendor's file is not the one the lock had: read why before trusting it) or
`refused: <why>`. Refusals are the rules working: robots.txt, a redirect off the
internet, HTML where a PDF was promised, a cap. Fix the candidate (a better URL),
do not work around the rule. Exit 1 when anything was refused.

## 3. Draft

```sh
python3 -I scripts/eds-draft.py show cache/sha256/<hex>          # what an EDS says
python3 -I scripts/eds-draft.py draft collect/<vendor>.lock.json devices/<vendor>/<model> [--eds NAME] [--vendor TEXT] [--model "TEXT"]
```

With several EDS in reach the draft refuses to pick: name the model's own file,
the newest revision (`_R2.8` over `_R2.7`). A config assembly without `bytes`
is one the EDS gives no size for (often instance 1, "no configuration data").

A folder with no EDS (a Modbus-only unit) gets a hand-written `device.toml`
with `[device]` and `[[sources]]` only, from the manual. Then, for any folder,
read the manual for `[[points]]` and `[wiring]` with the page for each claim, and
write **inferred** for anything not on a page. Points are optional in a first PR;
identity and sources are not.

Keep the draft honest: no `checked_on`, `firmware` or `checked_by` until a unit
has been on the bench (README: Contributing).

## 4. Ship

```sh
python3 -I scripts/build-index.py
uvx ruff@0.17.4 check . && uvx ruff@0.17.4 format --check . && python3 -I scripts/build-index.py --check
python3 -I -B -m unittest discover -s tests
```

Commit `collect/<vendor>.toml`, `collect/<vendor>.lock.json`, the folders and
`index.json`; never a file from `cache/`. Open the PR ready, not as a draft (Nick,
2026-11-14): the auto-merge workflow skips drafts, and a folder from documents
already says so (no `checked_on`), which the site shows as "from documents". Say
in the PR body what a unit must settle (a contradiction between documents, a
size the EDS leaves open). Two family PRs both regenerate `index.json`: when one
merges, merge `origin/dev` into the other and rerun `scripts/build-index.py`.
