"""Calcule le nombre d'équipements par sport et exporte les résultats.

Produit :
  - ``data/sport_counts.csv``        : comptage complet (sport, count) ;
  - ``docs/data/sport_counts.json``  : top sports + métadonnées pour le site.

Usage :
    python scripts/build_counts.py
"""

from __future__ import annotations

import json

import pandas as pd

from common import (
    DATA_DIR,
    DOCS_DIR,
    FACILITIES_CSV,
    SNAPSHOT_DATE,
    SPORT_LABELS,
    explode_sports,
)

TOP_N = 25


def main() -> None:
    df = pd.read_csv(FACILITIES_CSV)
    total_sites = len(df)

    sports = explode_sports(df["sport"])
    counts = sports.value_counts()

    # CSV complet.
    out_csv = DATA_DIR / "sport_counts.csv"
    counts.rename_axis("sport").to_frame("count").to_csv(out_csv)
    print(f"✅ {out_csv.relative_to(DATA_DIR.parent)} : {len(counts)} sports")

    # JSON pour le site (top N + total).
    top = counts.head(TOP_N)
    payload = {
        "snapshot_date": SNAPSHOT_DATE,
        "total_sites": int(total_sites),
        "total_records": int(counts.sum()),
        "distinct_sports": int(len(counts)),
        "top": [
            {
                "tag": tag,
                "label": SPORT_LABELS.get(tag, tag),
                "count": int(n),
            }
            for tag, n in top.items()
        ],
    }
    out_json = DOCS_DIR / "data" / "sport_counts.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {out_json.relative_to(DOCS_DIR.parent)} : top {len(top)}")

    print(f"\nSites totaux : {total_sites:,}".replace(",", " "))
    print(f"Sports distincts : {len(counts)}")
    print("\nTop 10 :")
    for tag, n in counts.head(10).items():
        print(f"  {tag:<14} {n:>7}")


if __name__ == "__main__":
    main()
