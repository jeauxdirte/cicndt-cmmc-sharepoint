# CMMC Preparation SharePoint naming schema

**Verified against the live site 2026-09-16** — not assumed, not sourced
from the personal-OneDrive evidence gathered earlier (which turned out to
be a different, inconsistent naming attempt in a different location).

## Rule

Lowercase the entire filename, replace every `_` with `-`, preserve
everything else exactly as-is (including whatever POL/PROC/PLAN number the
original already had — numbers are **not** reassigned) and the extension.

Confirmed with certainty via a real before/after pair already on the site:
`AU-POL-002-Audit-Logging-Retention-Policy_v1_0.pdf` (still original) and
`au-pol-002-audit-logging-retention-policy-v1-0.html` (already renamed,
same document, different format) — applying the rule to the `.pdf` name
produces an exact character match to the `.html` sibling's real name.

## Scope note

This is the CICNDT-tenant SharePoint site itself
(`cicndt.sharepoint.com/sites/AIMM-Center-CMMC/CMMC Preparation/`, drive ID
in `.env` as `SHAREPOINT_DRIVE_ID_CMMC_PREPARATION`) — reached via the
`ai-code-agent` Entra app registration and client-credentials auth, not
Claude's M365 connector (which has no reach into this tenant at all).

An earlier pass at deriving this schema from `cl@cllucas.com`'s personal
OneDrive (a different, unrelated location) found similar-looking but
**inconsistent** evidence — an org prefix sometimes present/absent, two
different collision-suffix conventions, and apparent renumbering in one
case. None of that carried over here. The real site's own already-renamed
files were internally consistent and are the only thing this schema is
based on.

## One unresolved item, not a naming question

`ma-pol-001-maintenance-policy-v1-0.1.pdf` has an unusual `_v1_0.1` version
marker on the original (vs. its sibling's plain `_v1_0`) — kept literal
since it's a content/versioning question, not a naming one. Worth the
user's own judgment on whether these are two genuinely different versions
or a duplicate.
