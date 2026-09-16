# cicndt-cmmc-sharepoint

Planning and tracking tooling for organizing the CICNDT CMMC Preparation
SharePoint site (`https://cicndt.sharepoint.com/sites/AIMM-Center-CMMC/`).

## What this is

Actual SharePoint mutations (renaming, uploading, moving files) are done
through Claude's Microsoft 365 MCP connector (`sharepoint_search`,
`sharepoint_rename_item`, `sharepoint_upload_file`, etc.) inside a Claude
session — not by this codebase directly. No Azure AD app registration or
Graph SDK is used.

This project holds the parts that benefit from being code instead of
one-off conversation state:

- **`docs/naming-schema.md`** — the actual kebab-case naming convention for
  the CMMC Preparation site, once defined. Not yet written; the naming
  schema must come from a real source (this project's memory, an actual
  planning session, or the user directly) rather than be assumed.
- **`docs/progress.md`** (or a CSV journal, once real work starts) — a
  durable record of what's been renamed/uploaded, in the same
  copy-verify-journal spirit as the local CICNDT migration in
  `../python-cleanup-project/docs/cicndt-migration/`. This is what lets
  a rename task actually be paused and resumed across sessions, unlike an
  unverifiable claim of prior progress.
- **`src/`** — Python helpers for the parts that are easier to script than
  to do by hand in conversation: e.g. taking a SharePoint folder listing
  (exported via `sharepoint_folder_search`/`sharepoint_search`) and
  computing a kebab-case rename plan against it, or diffing two listings
  to confirm a batch of renames landed correctly.

## Status

Scaffolded 2026-09-15. No naming schema or progress record exists yet —
those get built from scratch with real verification at each step, not
carried over from an unverified prior claim.

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
