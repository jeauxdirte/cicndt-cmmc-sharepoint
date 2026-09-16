#!/usr/bin/env python3
"""
First connectivity test: acquires a token, resolves the AIMM-Center-CMMC
site ID, and lists the top level of "CMMC Preparation" if reachable.

Run this once AZURE_TENANT_ID and AZURE_CLIENT_ID are filled in .env, before
building anything else -- it's the smoke test that confirms the app
registration, permissions, and admin consent actually work end to end.

Usage:
    python3 src/resolve_site.py
"""

from __future__ import annotations

import os
import sys

import requests
from dotenv import load_dotenv

from auth import ConfigError, graph_headers

load_dotenv()

GRAPH_ROOT = "https://graph.microsoft.com/v1.0"


def resolve_site(hostname: str, site_path: str) -> dict:
    url = f"{GRAPH_ROOT}/sites/{hostname}:{site_path}"
    resp = requests.get(url, headers=graph_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def list_children(item_url: str) -> list[dict]:
    resp = requests.get(item_url, headers=graph_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json().get("value", [])


def main() -> int:
    hostname = os.environ.get("SHAREPOINT_SITE_HOSTNAME", "cicndt.sharepoint.com")
    site_path = os.environ.get("SHAREPOINT_SITE_PATH", "/sites/AIMM-Center-CMMC")

    print(f"Resolving site: {hostname}:{site_path}")
    try:
        site = resolve_site(hostname, site_path)
    except ConfigError as e:
        print(f"CONFIG ERROR: {e}")
        return 1
    except requests.HTTPError as e:
        print(f"GRAPH API ERROR: {e}")
        print(f"  Response body: {e.response.text}")
        print(
            "\n  If this is a 403/Forbidden or 401, the most likely causes are:\n"
            "  - Admin consent wasn't granted for the Application permissions\n"
            "  - Using Sites.Selected but this specific site hasn't been granted "
            "to the app yet (needs a separate Graph call by a site/tenant admin)\n"
            "  - AZURE_TENANT_ID or AZURE_CLIENT_ID is wrong"
        )
        return 1

    site_id = site["id"]
    print(f"OK — site resolved.")
    print(f"  displayName: {site.get('displayName')}")
    print(f"  id: {site_id}")
    print(f"  webUrl: {site.get('webUrl')}")
    print(f"\n  -> Save this into .env as SHAREPOINT_SITE_ID={site_id}")

    print(f"\nListing the site's default document library root...")
    try:
        drive_root_url = f"{GRAPH_ROOT}/sites/{site_id}/drive/root/children"
        items = list_children(drive_root_url)
    except requests.HTTPError as e:
        print(f"  Could not list drive root: {e}")
        return 1

    for item in items:
        kind = "folder" if "folder" in item else "file"
        print(f"  [{kind}] {item['name']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
