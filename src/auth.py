"""
Client-credentials (app-only) auth against the CICNDT Microsoft Entra tenant.

Note on "token caching": with delegated/device-code auth, caching matters
because it avoids repeating an *interactive* login. Client-credentials auth
has no interactive step at all -- acquire_token_for_client() is already a
silent, non-interactive call. MSAL's ConfidentialClientApplication caches
the resulting app token in memory automatically for the life of the
process, which is all that's needed here; no file-based token persistence
is used.

Requires these env vars (see .env.example): AZURE_TENANT_ID, AZURE_CLIENT_ID,
AZURE_CLIENT_SECRET.
"""

from __future__ import annotations

import os

import msal
from dotenv import load_dotenv

load_dotenv()

GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]  # app-only: scopes come from
                                                          # the Application permissions
                                                          # granted in Entra, not a list
                                                          # chosen at runtime


class ConfigError(RuntimeError):
    pass


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value or value.startswith("REPLACE_WITH_"):
        raise ConfigError(
            f"{name} is not set. Copy .env.example to .env and fill in real "
            f"values from the Entra app registration's Overview page."
        )
    return value


def get_access_token() -> str:
    """Returns a valid Graph API access token, acquiring a fresh one if needed."""
    tenant_id = _require_env("AZURE_TENANT_ID")
    client_id = _require_env("AZURE_CLIENT_ID")
    client_secret = _require_env("AZURE_CLIENT_SECRET")

    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
    )

    result = app.acquire_token_for_client(scopes=GRAPH_SCOPE)

    if "access_token" not in result:
        raise ConfigError(
            f"Token acquisition failed: {result.get('error')} — "
            f"{result.get('error_description')}"
        )

    return result["access_token"]


def graph_headers() -> dict:
    """Convenience: an Authorization header dict ready to pass to requests."""
    return {"Authorization": f"Bearer {get_access_token()}"}
