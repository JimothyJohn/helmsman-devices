#!/usr/bin/env bash
# First publish of the device library: the first commit if there is none,
# then the PUBLIC GitHub repo JimothyJohn/helmsman-devices with main + dev.
#
# Needs: gh authenticated as JimothyJohn (gh auth status), this checkout.
# Does:  `git init` + first commit when the folder has no repository yet;
#        creates the repo as PUBLIC if missing; sets it as `origin`; pushes
#        main; creates dev from main if missing. Idempotent.
# Verifies: no vendor file is tracked; the repo exists, is public, and has
#        main and dev.
#
# Usage (in your own shell): ./scripts/create-github-repo.sh
set -euo pipefail
cd "$(dirname "$0")/.."
die() { echo "error: $*" >&2; exit 1; }
command -v gh >/dev/null || die "gh not found: brew install gh && gh auth login"
command -v git >/dev/null || die "git not found"
repo="JimothyJohn/helmsman-devices"

if [ ! -d .git ]; then
  git init -q -b main .
fi
if [ -z "$(git rev-parse --verify -q HEAD || true)" ]; then
  git add -A
  git commit -q -m "Device library: layout, device.toml schema, the Moxa ioLogik E1213 as the first entry

Metadata and map lines MIT; vendor files by reference (name, size,
SHA-256, where), never committed. The E1213 record carries what the
bench showed on 2026-11-02 (firmware 3.1, O->T on the port the reply
names, bit order, EXT field power) with the manual's pages as sources.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
fi
# Nothing a vendor owns may be in the tree.
if git ls-files | grep -Eiq '\.(eds|pdf)$'; then
  die "a vendor file is tracked; see README (Vendor files)"
fi

if ! gh repo view "$repo" >/dev/null 2>&1; then
  gh repo create "$repo" --public --description "Helmsman device library: remote I/O, drives and controllers mapped once, with sources"
fi
vis="$(gh repo view "$repo" --json visibility --jq .visibility)"
[ "$vis" = "PUBLIC" ] || die "$repo is $vis, expected PUBLIC"
if git remote get-url origin >/dev/null 2>&1; then
  [ "$(git remote get-url origin)" = "git@github.com:$repo.git" ] \
    || [ "$(git remote get-url origin)" = "https://github.com/$repo.git" ] \
    || die "origin points elsewhere: $(git remote get-url origin)"
else
  git remote add origin "git@github.com:$repo.git"
fi
git push -u origin main
if ! git ls-remote --exit-code --heads origin dev >/dev/null 2>&1; then
  git push origin main:dev
fi
gh api "repos/$repo/branches/main" --jq .name >/dev/null || die "main missing on GitHub"
gh api "repos/$repo/branches/dev" --jq .name >/dev/null || die "dev missing on GitHub"
echo "verified: $repo is public with main and dev"
echo "next: wire CI with the repo-baseline skill (draft PR into dev)"
