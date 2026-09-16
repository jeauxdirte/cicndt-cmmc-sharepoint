# Progress log

**2026-09-15** — Auth setup, not yet tested.

- Registered Entra app `ai-code-agent` in the CICNDT tenant, client secret
  created (expires 3/14/2027). Secret stored in local `.env`, gitignored,
  never committed.
- Decided: client-credentials (app-only) flow over delegated/device-code,
  since a client secret was already generated. Trade-off understood: no
  interactive login needed, but access is governed by Application
  permissions granted to the app, not by what `cllucas@cicndt.com` can do.
- Wrote `src/auth.py` (MSAL ConfidentialClientApplication) and
  `src/resolve_site.py` (connectivity smoke test).
- **Blocked on:** Tenant ID + Client ID (user has these, not yet provided),
  and the Entra portal steps (Application permissions, admin consent, and
  if using Sites.Selected, the follow-up site-grant call) — all documented
  in README.md, not yet performed.

No SharePoint operations have been performed. No naming schema has been
confirmed against the actual site — see `docs/naming-schema.md`.
