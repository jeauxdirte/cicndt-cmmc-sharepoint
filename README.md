# cicndt-cmmc-sharepoint

Tooling for organizing the CICNDT CMMC Preparation SharePoint site
(`https://cicndt.sharepoint.com/sites/AIMM-Center-CMMC/`) via a dedicated
Azure AD app registration and the Microsoft Graph API — not Claude's M365
connector, which is bound to a personal (`cl@cllucas.com`) account with no
reach into the CICNDT tenant.

## Auth: client credentials (app-only)

The app authenticates as itself using a client secret — no interactive
login per run, good for unattended scripts. This means Graph API access is
governed entirely by whatever **Application permissions** are granted to
the app in Entra, not by what any specific user can do.

### Entra setup (portal steps — do these as `cllucas@cicndt.com`)

1. **App registration** — done: `ai-code-agent`, client secret created
   (expires 3/14/2027).
2. **API permissions** → remove any Delegated permissions if present, add
   **Application** permissions (not Delegated):
   - Choose ONE of:
     - **`Sites.Selected`** (recommended) — the app can only reach sites
       explicitly granted to it. Requires one extra step below, but keeps
       the app scoped to just this CMMC site rather than every SharePoint
       site in the tenant — appropriate given the CUI/compliance context.
     - **`Sites.ReadWrite.All`** — simpler (one admin-consent click, no
       extra step), but grants the app read/write access to *every*
       SharePoint site in the CICNDT tenant.
3. Click **Grant admin consent for CICNDT** (needs Global/SharePoint/
   Application Admin rights — flag if `cllucas@cicndt.com` doesn't have one).
4. **If using `Sites.Selected`**: admin consent alone isn't enough — a site
   admin must separately grant this app access to the specific site. Once
   you have the site ID (running `src/resolve_site.py` will fail until this
   step is done, but the error message explains it), a tenant/site admin
   runs, while signed into their own account (e.g. via Graph Explorer):
   ```
   POST https://graph.microsoft.com/v1.0/sites/{site-id}/permissions
   {
     "roles": ["write"],
     "grantedToIdentities": [{
       "application": { "id": "<AZURE_CLIENT_ID>", "displayName": "ai-code-agent" }
     }]
   }
   ```

### Local setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in AZURE_TENANT_ID and AZURE_CLIENT_ID
                        # (AZURE_CLIENT_SECRET is already set)
python3 src/resolve_site.py
```

`resolve_site.py` is the smoke test — confirms auth works end to end and
resolves the site's Graph ID, which everything else needs.

## What's next (not built yet)

- The naming schema for `cmmc-policy/` items is still unresolved — see
  `docs/naming-schema.md`. Evidence gathered so far (from the user's
  personal OneDrive, a different location, via Claude's M365 connector)
  shows an inconsistent pattern: numbers get reassigned per control family
  rather than preserved from source documents, and collision-handling
  varies between a numeric suffix and a content-hash suffix. Needs to be
  settled against the actual SharePoint site's current state once this
  app can reach it, not assumed from that other evidence.
- Rename/upload operations themselves, once `resolve_site.py` confirms
  connectivity.

## Status

2026-09-15: app registered, client secret in place, auth module and
connectivity smoke test written. Not yet tested — waiting on the Tenant ID
and Client ID, and on the Application-permissions/admin-consent portal
steps above.
