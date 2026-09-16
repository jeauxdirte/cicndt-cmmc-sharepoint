#!/usr/bin/env python3
"""
Computes a kebab-case rename plan from a SharePoint folder listing.

Doesn't call SharePoint itself -- feed it a listing (e.g. exported as CSV
from sharepoint_search / sharepoint_folder_search results), and it produces
old-name -> new-name pairs with collision detection, in the same spirit as
the local corpus rename scripts in ../python-cleanup-project/docs/.

Usage:
    python3 src/rename_plan.py --listing folder_listing.csv --out rename_plan.csv

Input CSV must have at least a "name" column (one row per file/folder).
"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import Counter
from pathlib import Path


def kebab(name: str, keep_ext: bool = True) -> str:
    stem, ext = (name.rsplit(".", 1) + [""])[:2] if keep_ext and "." in name else (name, "")
    stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode()
    stem = re.sub(r"[^A-Za-z0-9]+", "-", stem)
    stem = re.sub(r"-+", "-", stem).strip("-").lower()
    return f"{stem}.{ext.lower()}" if ext else stem


def build_plan(rows: list[dict]) -> list[dict]:
    plan = []
    for row in rows:
        old = row["name"]
        new = kebab(old)
        plan.append({"old": old, "new": new, "changed": old != new})

    counts = Counter(p["new"] for p in plan)
    collisions = {name for name, c in counts.items() if c > 1}
    for p in plan:
        p["collision"] = p["new"] in collisions

    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--listing", required=True, help="CSV with a 'name' column")
    parser.add_argument("--out", default="rename_plan.csv")
    args = parser.parse_args()

    with open(args.listing, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    plan = build_plan(rows)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["old", "new", "changed", "collision"])
        writer.writeheader()
        writer.writerows(plan)

    changed = sum(1 for p in plan if p["changed"])
    collisions = sum(1 for p in plan if p["collision"])
    print(f"{len(plan)} items, {changed} would change, {collisions} collisions -> {args.out}")
    if collisions:
        print("Resolve collisions before executing any renames.")


if __name__ == "__main__":
    main()
