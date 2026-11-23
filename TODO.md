# TODO

Open items for the device library. The board (`/todo`) renders this file; an
`answer:` line is Nick's and is acted on by the next session.

## Open questions for Nick

- [ ] **Promote dev to main?** — main is the deploy line: the gallery at helmsman.advin.io/find reads it. dev is 38 commits ahead (#52–#63): 130 new devices (46 → 174 after two removals), a category on every entry, `channels` on 173 of 174, CATALOG.md, scripts/find.py and use.py, eds-draft refusing DeviceNet/ControlNet files, ruff 0.17.6. All merged with green CI. The gallery's category row (helmsman #564, on helmsman dev) shows only once this lands on main and helmsman dev reaches master.
      options: promote now — the gallery gains 128 devices and its category row once helmsman is promoted too | wait — nothing changes for visitors
      recommend: promote now — every PR in it passed CI, and the gallery is two promotions behind the library
      stakes: high
      id: promote-dev-main
      asked: 2026-11-23
      by: resume 2026-11-23

- [ ] **Fetch vendor manuals in a real browser?** — Rockwell's literature library, Festo and Danfoss answer 403 (Akamai) to curl and WebFetch; WAGO 750-362/363 and the Siemens IM 155-6 MF HF manual need JavaScript to download, and so do Murrelektronik's shop and (likely) Pepperl+Fuchs' product pages. So about 40 entries are an EDS and an ODVA declaration and nothing else: no `[[points]]`, so `use.py` gives the connection but not the channels' bits. A fetch through Chrome on the Air (the extension, your own browser, an honest user agent) would read the same public PDFs a person would. Files would still be hashed into the S3 store, never committed.
      options: browser fetch — points for the Rockwell, Festo, Danfoss, WAGO and Siemens entries in a follow-up batch | you download — you drop the PDFs in a folder and I hash and read them | leave them — those entries stay EDS-only
      recommend: browser fetch — it is a person's fetch of public documents, and it unblocks the biggest gap in the library
      stakes: high
      id: browser-fetch
      asked: 2026-11-22
      by: 100 new devices session

- [ ] **Raise the zip cap for Yaskawa's EDS packages?** — docs-fetch.py refuses a zip with more than 2000 members (ZIP_MAX_MEMBERS, a guard against zip bombs). Yaskawa's SI-EN3 and SI-EN3D packages hold 2816 (one EDS per drive model and rating), so those two option cards are not in the library.
      options: raise to 4000 — both cards can be drafted; the guard still stops anything larger | leave them out — no Yaskawa EtherNet/IP cards
      recommend: raise to 4000 — the size and SHA-256 checks still hold, and the zip is from Yaskawa's own site
      stakes: low
      id: yaskawa-zip-cap
      asked: 2026-11-22
      by: 100 new devices session

- [ ] **Make eds-draft.py require a category?** — every entry has a `[device] category` now, but a fresh draft from eds-draft.py has none and lands under "Not yet sorted" in CATALOG.md. build-index names it and CI passes. Requiring one would fail the daily intake routine's PRs until the routine passes a category.
      options: flag and warn — eds-draft takes `--category`, warns without one, CI stays green; the routine learns to pass it | require — CI fails an entry without one; the routine has to change first | leave it — drafts stay unsorted until someone sorts them
      recommend: flag and warn — sorted drafts without breaking the routine
      stakes: low
      id: eds-draft-category
      asked: 2026-11-22
      by: catalog session

- [ ] **What are the unit bounty terms?** — AGENTS.md says "the project pays a bounty for units it has not tested; the terms are in the Devices section of the Helmsman site", but no page there has them (helmsman's CLAUDE.md rules out a dollar amount on the site). My draft from 2026-11-16: offer first, a payment on arrival and power-up, the unit returned postage paid unless the owner says keep it, address and payment arranged privately. Still open: who pays inbound shipping, the payout method, a budget cap, and whether a reading the owner runs themselves earns anything.
      options: set the terms — I put them on the site without an amount and AGENTS.md points there | drop the pointer — AGENTS.md says to open a `Unit offer:` issue and nothing about terms until they are set
      recommend: drop the pointer — today it sends people to a page that does not exist
      stakes: high
      id: bounty-terms
      asked: 2026-11-16
      by: gallery session

- [ ] **Brainboxes ED-538/588: should helmsman switch them to Modbus TCP?** — they ship speaking Brainboxes' ASCII protocol; Modbus TCP is chosen on the device's web console first (Modbus TCP Manual p. 3). The entries say "not usable out of the box". helmsman could make that one config write itself.
      options: keep the note — a person flips it once in the web console | helmsman flips it — a config write to the device's web console, built from a captured exchange on a bench unit
      recommend: keep the note — a config write is worth building only after a unit is on the bench
      stakes: low
      id: brainboxes-ascii
      asked: 2026-11-16
      by: modbus session

## Library work

- [x] **Hash the documents some channels lines were read from** — channels for Schneider PM5560, STB NIP2311, TM3BCEIP, TPRBCEIP, Siemens SENTRON PAC3200/4200, SINAMICS G120, IM 155-6 MF HF and SMC EX260/EX600 came from vendor pages found by search, not from a document in the entry's `[[sources]]`. PAC4200 and G120 were read from other editions than the entries name.
      result: each of those lines names a document in `[[sources]]` with size and SHA-256, or is marked inferred
      est: 3h
      difficulty: med
      id: hash-channel-sources
      asked: 2026-11-23

- [ ] **Find the port count of the Pepperl+Fuchs ICE21-8IOL2-G70L-V1D** — the one entry with no channels. Searched 2026-11-23 (#65): the ODVA Marketplace page links only the EDS and the declaration of conformity, and P+F's IO-Link master page lists only the ICE1 family. The data sheet is likely on P+F's product page for article 70148669, which no fetcher reached. The "8IOL" in the model number is not a source.
      result: `channels` with a data sheet page
      depends: browser-fetch
      est: 30m
      difficulty: low
      model: fable
      notes: a browser step, so it stays with the main session
      id: pf-ice21-channels
      asked: 2026-11-23

- [ ] **Store the last two Murrelektronik files** — #69 stored the hand-collected files of the Moxa E1212/E1213, Novanta, UR and the two 55089 EDS (every hash matched, every EDS is EtherNet/IP). Two remain: the IMPACT67 E manual, art. 55368 (sha256 f01edb0a…, cited by 5 Murrelektronik folders), and the 55086 EDS (fd900040…, in 55086_IMPACT67_KF5_x_11.zip). shop.murrelektronik.com answers a fetcher with only a "Please wait..." script page. collect/murrelektronik.toml names both in a comment.
      result: both in the store by hash, collect/murrelektronik.lock.json written, the 55086 EDS's network verdict
      depends: browser-fetch
      est: 30m
      difficulty: low
      model: fable
      notes: a browser step, so it stays with the main session
      id: store-older-files
      asked: 2026-11-23

- [x] **Find the Moxa ioLogik E2200 manual** — not linked from moxa.com's product pages, so E2210/E2212/E2242 have no register points.
      result: `[[points]]` for the three, each with a page
      est: 2h
      difficulty: med
      id: moxa-e2200-points
      asked: 2026-11-22

- [x] **Drop the EDS vendor string from README titles** — 17 READMEs open with the EDS's VendName ("# SICK AG SIG300", "# Banner Engineering Corp. Banner DXM") instead of the folder's `[device] vendor`.
      result: each title is `# <vendor> <model>` as device.toml states them
      est: 30m
      difficulty: low
      id: readme-titles
      asked: 2026-11-22

- [x] **Give eds-draft.py a vendor name per vendor id** — it copies the EDS VendName into `[device] vendor`, so drafts drift from the names #60 normalized.
      result: a vendor id → name table the draft uses, with a test; VendName only for an id not in it
      est: 1h
      difficulty: med
      id: eds-draft-vendor
      asked: 2026-11-22

- [ ] **Draft Yaskawa SI-EN3 and SI-EN3D** — waiting on the zip cap.
      result: two folders under devices/yaskawa from the EDS
      depends: yaskawa-zip-cap
      est: 1h
      difficulty: med
      id: yaskawa-entries
      asked: 2026-11-22

- [ ] **Read points from the manuals behind Akamai** — Rockwell, Festo, Danfoss, WAGO 750-362/363, Siemens IM 155-6 MF HF.
      result: `[[points]]` with pages for those entries
      depends: browser-fetch
      est: 1d
      difficulty: med
      model: fable
      notes: runs in the main session, since the browser is Chrome on the Air through the extension
      id: akamai-points
      asked: 2026-11-22

## Needs a unit on the bench

- [ ] **Confirm identities matched by family** — Banner DXMR90-4K against the DXM EDS (code 200); Cognex DataMan 370 against the DM30x/36x EDS (code 1290); Datalogic Matrix 220/320 against the Matrix N EDS; Festo CPX-AP-I-EP against "-M12".
      needs: the unit on the network, `enip-identify.py` output
      result: `[identity.enip]` confirmed or corrected, with firmware
      status: blocked
      difficulty: low
      id: unit-identities
      asked: 2026-11-22

- [ ] **Settle the entries resting on one catalog number** — ArmorStart 280E/281E and ArmorStart LT each rest on one catalog number's EDS (280E, 290E); PowerFlex 523 with 25-COMM-E2P is the adapter's five-drive layout.
      needs: a unit of another catalog number, or Rockwell's manuals (see browser-fetch)
      status: blocked
      difficulty: med
      id: one-catalog-entries
      asked: 2026-11-23

- [ ] **Settle three contradictions between documents** — Omron NX-EIC202: output instance 148 in the connection path vs Assem150; Phoenix Contact data sheet p. 19 swaps in and out; Brainboxes coil 0x0000 vs 0x0001.
      needs: each unit on the network, and a person watching it
      result: the entry follows the unit, and the README names the document that was wrong
      status: blocked
      difficulty: med
      id: unit-contradictions
      asked: 2026-11-16
