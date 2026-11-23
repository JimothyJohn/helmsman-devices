# collect/

Where each vendor document for the library comes from, and what was fetched.
The files themselves are never committed (README, Vendor files): they live in
`cache/sha256/<hex>` on the machine that fetched them and in the project's
private bucket. Anyone can rebuild their own copy from these records and check
every hash.

| file | written by | says |
| --- | --- | --- |
| `families.toml` | a person | the families and models wanted, in order |
| `<vendor>.toml` | the `collect-docs` skill, or a person | the candidates: which URL holds which document for which folder, and how it was found |
| `<vendor>.lock.json` | `scripts/docs-fetch.py` | what each URL gave: name, size, SHA-256, type, final URL after redirects, date; an archive's members |

## `<vendor>.toml`

```toml
format = "helmsman-devices-collect 1"
vendor = "Turck"

[[doc]]
folder = "devices/turck/tben-s2-8dxp"   # the library folder it is for; a family package
                                        # serving several: folders = ["...", "..."]
kind = "eds"                            # eds gsdml esi manual release-notes register-map datasheet archive
url = "https://..."                     # https on 443 only
title = "TBEN-S2-8DXP EDS"
found = "2026-11-14 search: turck tben-s2-8dxp eds; product page https://..."
terms = "none stated"                   # optional: what the vendor says about redistribution
browser = true                          # optional: only a person's browser gets the file (below)
```

## The fetch rules

`scripts/docs-fetch.py` holds every request, each redirect hop included, to:
https on port 443, no userinfo; every address the host resolves to must be
global unicast, and the connection is made to the address that was checked;
robots.txt honoured (a 4xx robots.txt allows, a 5xx or unreachable one
disallows, RFC 9309); one request a second per host; 64 MiB a file, 256 MiB
unpacked from an archive; at most 5 redirects, never to http; the bytes must be
the kind claimed (a PDF starts `%PDF-`, an EDS has `[File]` and `[Device]`, and
an HTML page is never a document).

## Documents only a browser gets

Some vendors serve a file only to a person's browser: a script wall, a terms
box to tick, a bot filter that answers anything else with 403. The fetcher does
not work around those. Such a `[[doc]]` says `browser = true`, and its `url` is
the page the file is downloaded from (the file may have no URL of its own: a
form post, a script). `docs-fetch.py` never requests it, and reports it
`refused` until it is in the store.

Someone downloads the file in a browser, from that page, and imports it:

```sh
python3 -I scripts/docs-fetch.py collect/<vendor>.toml --import URL FILE
```

`URL` is the `[[doc]]`'s url; `FILE` is what the browser saved. The file is held
to the fetcher's own checks (the size cap, the kind, an archive's caps and
members), stored by hash like any other, and its lock entry carries
`"via": "browser"` with the page as `final_url`. From then on it is `stored`.
Say in `found` what the page asked for (a terms box ticked, and by whose
leave), so the next person knows what downloading it again involves.

## The bucket

`HELMSMAN_DOCS_BUCKET=<name>` makes the fetcher copy each new file to
`s3://<name>/sha256/<hex>` (SSE-S3) and look there before the vendor's URL, so
a file a vendor has since moved or put behind a login is still at hand for
those with access. It uses the `aws` CLI and whatever credentials it has. The
bucket is private; it is not a way to redistribute.
