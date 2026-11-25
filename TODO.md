# TODO

Open items for the device library. The board (`/todo`) renders this file; an
`answer:` line is Nick's and is acted on by the next session.

## Open questions for Nick

- [ ] **Promote dev to main?** — main is the deploy line: the gallery at helmsman.advin.io/find reads it. dev is 80 commits ahead (#52–#78): 130 new devices (46 → 174 after two removals), a category on every entry, `channels` on all 174, 445 documented points across the library (254 of them from Rockwell and Festo manuals fetched in a browser), CATALOG.md, scripts/find.py and use.py, eds-draft refusing DeviceNet/ControlNet files and naming vendors by vendor id, docs-fetch --import for browser downloads. All merged with green CI. The gallery's category row (helmsman #564, on helmsman dev) shows only once this lands on main and helmsman dev reaches master.
      options: promote now — the gallery gains 128 devices and its category row once helmsman is promoted too | wait — nothing changes for visitors
      recommend: promote now — every PR in it passed CI, and the gallery is two promotions behind the library
      stakes: high
      id: promote-dev-main
      asked: 2026-11-23
      by: resume 2026-11-23

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

## From Wayfinder research (2026-11-25)

- [ ] **Never mirror IODDs from IODDfinder; keep a link, a hash and the `ioddId`** — IODDfinder's own terms (Clause 5.2, read in its web app on 2026-11-25) let a registered user store IODDs for internal use and bar providing them to third parties "against payment or free of charge"; Clause 5.3 bars using them to imitate the portal. A public library that copied IODDs would breach that, so an IO-Link entry should hold vendor, product, `ioddId`, version, the vendor's own page, the SHA-256 of the file one contributor downloaded, and the date read, and no file. Where the vendor also posts the IODD on its own site, cite that page. This is a reading of the terms, not legal advice, and Clause 9 lets the portal change them at any time. Confidence: medium; the API guide returned 401, so rate limits are unknown.
      result: docs/intake.md and the README's vendor-files section say so in a short rule, with the date the terms were read
      model: sonnet
      est: 30m
      difficulty: low
      id: iodd-link-hash-rule
      source: https://io-link.com/legal-information
      findings: 2026-11-25-ioddfinder-terms-bar-redistribution, 2026-11-24-vendor-eds-iodd-public-addresses-terms
      asked: 2026-11-25

- [ ] **Record provenance per device, starting with Turck's Li-Q25L** — Nick backed this move on 2026-11-25. Each entry would name its page URL, file URL, read date, SHA-256 and terms URL, and CI would flag a changed hash. First row: page https://www.turck.us/en/product/IODD%20IO-Link%20Li-Q25L, file https://www.turck.us/attachment/IODD_IOL_LI-Q25L.zip, SHA-256 2493001ddf733e1670e923e9b70f1710e409933e8bdfd23da66d0fb0c75d104f (read 2026-11-24). The IODD XML inside is dated 2010-12-22 (v1.0.1), and no file-use terms were readable on Turck's pages, so ask Turck in writing before any bulk crawl. Confidence: low; one fetch, and the XML was not parsed.
      result: the Turck Li-Q25L entry carries the row; a documented place for the fields in docs/device-toml.md; if the CI check needs a schema change, stop and say so in the pull request
      model: sonnet
      est: 2h
      difficulty: med
      id: provenance-turck-li-q25l
      source: https://www.turck.us/attachment/IODD_IOL_LI-Q25L.zip
      findings: 2026-11-24-turck-iodd-public-zip-dated-2010
      asked: 2026-11-25

- [ ] **Licence the device data and take contributions with a DCO sign-off** — the repo is MIT licensed today (README line 80) and has no CONTRIBUTING. CC0 waives copyright and database rights and disclaims warranty, so firms can reuse the data with no conditions; ODbL would require share-alike on any firm that publicly uses a derived database. The Developer Certificate of Origin is one `Signed-off-by` line and transfers no rights. CC0 grants no patent or trademark rights, and vendor datasheet content may carry its own terms. Not legal advice. Confidence: medium.
      options: CC0 for device data, DCO for contributions | keep MIT for everything, add the DCO | leave as is
      recommend: CC0 for device data and the DCO; it is the cheapest way for a firm to reuse the moat
      stakes: med
      id: data-licence-dco
      source: https://developercertificate.org/
      findings: 2026-11-25-bounty-1099-threshold-dco-cc0-device-data
      asked: 2026-11-25

- [ ] **Bounties: collect a W-9 or W-8BEN at the first payment, or pay through a platform** — for payments made in 2026 the IRS threshold for a 1099-NEC is $2,000 a year per contributor (up from $600), and a platform that pays out files its own forms. Whether overseas mappers owe withholding is unsettled in the pages read, so ask an accountant before the first payment over $2,000. Today's bounty is credit and a direct line to Nick, with no cash, so nothing is due until cash returns. Not tax advice. Confidence: medium.
      needs: Nick, and an accountant before any cash payment
      status: blocked
      id: bounty-tax-forms
      source: https://www.irs.gov/pub/irs-prior/i1099mec--2026.pdf
      findings: 2026-11-25-bounty-1099-threshold-dco-cc0-device-data
      asked: 2026-11-25

## Library work

- [x] **Hash the documents some channels lines were read from** — channels for Schneider PM5560, STB NIP2311, TM3BCEIP, TPRBCEIP, Siemens SENTRON PAC3200/4200, SINAMICS G120, IM 155-6 MF HF and SMC EX260/EX600 came from vendor pages found by search, not from a document in the entry's `[[sources]]`. PAC4200 and G120 were read from other editions than the entries name.
      result: each of those lines names a document in `[[sources]]` with size and SHA-256, or is marked inferred
      est: 3h
      difficulty: med
      id: hash-channel-sources
      asked: 2026-11-23

- [x] **Find the port count of the Pepperl+Fuchs ICE21-8IOL2-G70L-V1D** — the one entry with no channels. Searched 2026-11-23 (#65): the ODVA Marketplace page links only the EDS and the declaration of conformity, and P+F's IO-Link master page lists only the ICE1 family. The data sheet is likely on P+F's product page for article 70148669, which no fetcher reached. The "8IOL" in the model number is not a source.
      result: `channels` with a data sheet page
      needs: Chrome on the Air with the Claude extension connected (headless Chromium gets 403 there; no user-agent faking)
      est: 30m
      difficulty: low
      model: fable
      notes: a browser step, so it stays with the main session
      id: pf-ice21-channels
      asked: 2026-11-23

- [x] **Store the last two Murrelektronik files** — #69 stored the hand-collected files of the Moxa E1212/E1213, Novanta, UR and the two 55089 EDS (every hash matched, every EDS is EtherNet/IP). Two remain: the IMPACT67 E manual, art. 55368 (sha256 f01edb0a…, cited by 5 Murrelektronik folders), and the 55086 EDS (fd900040…, in 55086_IMPACT67_KF5_x_11.zip). shop.murrelektronik.com answers a fetcher with only a "Please wait..." script page. collect/murrelektronik.toml names both in a comment.
      result: both in the store by hash, collect/murrelektronik.lock.json written, the 55086 EDS's network verdict
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

- [x] **Read points from the manuals behind Akamai** — 254 points on 10 entries (#75-#78, each checked against its manual before merge): ArmorStart 280E/281E and LT, PowerFlex 525, 523 with 25-COMM-E2P, 70, 70EC, 755, 6000T; Festo CTEU-EP and CMMT-AS.
      id: akamai-points
      asked: 2026-11-22

- [ ] **Fetch the next manuals in Chrome** — five entries got no points because the manual that has the layout is another document: 1732E-UM001 (16-channel configurable ArmorBlock; IN008/IN009 are installation sheets with no assembly layout, and IN008 p. 9 names UM001), a manual naming 1732E-IB16M12R/OB16M12R's assemblies, the CIP Objects and Attributes reference 35-RD001 (Armor PowerFlex 35E; 35-UM001 p. 155 points to it), Festo's "Appendix to operating instructions" for the CTEU-EP's coil mapping, and a VABX CTED-EP manual (two portal searches found none). Same route as 2026-11-23: Chrome on the Air, hash in the page, one zip per site, Nick's scp, docs-fetch --import.
      needs: Chrome on the Air with the Claude extension connected, and Nick for one scp line
      result: [[points]] for 1732E-IB16M12R, -OB16M12R, -16CFGM12R, Armor PowerFlex 35E, and the CTEU-EP coil bits
      est: 3h
      difficulty: med
      model: fable
      notes: a browser step, so it stays with the main session; readers can then be delegated
      id: browser-manuals-2
      asked: 2026-11-23

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

- [ ] **Settle three findings the manual readers could not** — PowerFlex 70EC: the entry's EDS is device type 152 ("DPI to DLR EtherNet/IP"), while 20COMM-UM010 (the 20-COMM-E) reports type 123, which it labels "PowerFlex 70 EC drive"; the 70EC's points follow the 20-COMM-E manual and are marked inferred. Festo CTEU-EP: the manual says configuration assembly 102 with size 0 for a generic module, the EDS gives 38 bytes. Festo CMMT-AS: no default telegram stated, and the byte order of the process-data words on EtherNet/IP is inferred.
      needs: each unit on the network; enip-identify.py output and one read of the input assembly
      result: the entries follow the unit; inferred marks removed where the unit confirms them
      status: blocked
      difficulty: med
      id: unit-reader-findings
      asked: 2026-11-23
