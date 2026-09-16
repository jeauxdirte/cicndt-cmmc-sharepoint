# Progress log

**2026-09-16** — Auth confirmed working, `cmmc-policy/` fully renamed.

- `resolve_site.py` confirmed the app can reach the CICNDT tenant: resolved
  the `AIMM-Center-CMMC` site, discovered it has 4 document libraries
  (`CMMC Preparation`, `CMMC`, `AIMM Center CMMC Polcy`, `Documents`) —
  the target is its own document library, not a folder inside the default
  one. Drive ID saved to `.env`.
- Listed `CMMC Preparation` root: 31 items, all already kebab-cased
  (11 folders + 20 files). Listed `cmmc-policy/`: 36 items, 12 already
  renamed (today, in a prior session that got interrupted), 24 not.
- Verified item #12/13 (`AU-POL-002-Audit-Logging-Retention-Policy_v1_0.pdf`
  / `.html`) directly against the live site: the `.pdf` was still original,
  the `.html` was already renamed. This confirmed the naming rule with
  certainty — see `docs/naming-schema.md`.
- Built and executed the rename plan for the remaining 24 items
  (`docs/cmmc-policy-rename-plan.csv`). All 24 renamed via Graph API
  `PATCH`, each verified by re-fetching the item under its new name
  immediately after. Journaled to `docs/cmmc-policy-rename-journal.jsonl`.
- **Independently re-listed the whole folder afterward** (not just trusting
  the per-item verification): 36/36 items now kebab-case, 0 exceptions.

`cmmc-policy/` is done. The other 10 subfolders under `CMMC Preparation`
were not inventoried in this pass — unclear whether they're actually fully
renamed already (the user's original description said "8 of 9," this site
now shows 11 subfolders total at the root) or whether that count has
shifted since. Worth a fresh listing before assuming they're complete.

**Not yet done** (per the original task's remaining scope): uploading
genuinely-new files into matching folders, and the final summary report
including any items needing human judgment rather than autonomous action.
The `ma-pol-001-maintenance-policy-v1-0.1.pdf` version-duplicate question
(see naming-schema.md) is one candidate for that judgment-needed list.
