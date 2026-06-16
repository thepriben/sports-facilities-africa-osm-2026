"""Génère les cartes Folium (HTML) à partir de ``data/sports_facilities.csv``.

Trois modes, regroupant les anciens scripts dupliqués :

    # Carte de densité de tous les équipements (heatmap légère)
    python scripts/make_map.py heatmap

    # Carte d'un sport unique
    python scripts/make_map.py sport --sport netball --color "#1d3557" --name netball

    # Carte multi-sports "britanniques" (couleurs prédéfinies)
    python scripts/make_map.py british

Les fichiers sont écrits dans ``docs/maps/``.
"""

from __future__ import annotations

import argparse

import folium
import pandas as pd
from folium.plugins import HeatMap

from common import (
    BRITISH_SPORTS,
    DOCS_DIR,
    FACILITIES_CSV,
    SNAPSHOT_DATE,
    extract_point,
)

MAPS_DIR = DOCS_DIR / "maps"
AFRICA_CENTER = [2.0, 20.0]
AFRICA_ZOOM = 3


def load_points() -> pd.DataFrame:
    df = pd.read_csv(FACILITIES_CSV)
    df["sport"] = df["sport"].fillna("").str.strip()
    df["lat"], df["lon"] = zip(*df["geometry"].map(extract_point))
    return df.dropna(subset=["lat", "lon"])


def base_map() -> folium.Map:
    return folium.Map(
        location=AFRICA_CENTER,
        zoom_start=AFRICA_ZOOM,
        tiles="CartoDB positron",
        control_scale=True,
    )


def save(m: folium.Map, name: str) -> None:
    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    out = MAPS_DIR / f"{name}.html"
    m.save(str(out))
    print(f"✅ {out.relative_to(DOCS_DIR.parent)}")


def build_heatmap() -> None:
    df = load_points()
    m = base_map()
    HeatMap(
        list(zip(df["lat"], df["lon"])),
        radius=7,
        blur=9,
        min_opacity=0.3,
    ).add_to(m)
    print(f"Heatmap : {len(df):,} points".replace(",", " "))
    save(m, "africa_heatmap")


def build_sport(sport: str, color: str, name: str) -> None:
    df = load_points()
    sel = df[df["sport"].str.contains(sport, case=False, na=False)]
    m = base_map()
    for _, row in sel.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=3,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            weight=0,
            popup=row["sport"],
        ).add_to(m)
    print(f"{sport} : {len(sel):,} sites".replace(",", " "))
    save(m, name)


def build_british() -> None:
    df = load_points()
    pattern = "|".join(BRITISH_SPORTS)
    sel = df[df["sport"].str.contains(pattern, case=False, na=False)]
    m = base_map()
    for _, row in sel.iterrows():
        sport_lower = row["sport"].lower()
        main = next((s for s in BRITISH_SPORTS if s in sport_lower), None)
        color = BRITISH_SPORTS[main]["color"] if main else "#888888"
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=3,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            weight=0,
            popup=row["sport"],
        ).add_to(m)

    legend = "".join(
        f'<div><span style="background:{v["color"]}"></span>{v["label"]}</div>'
        for v in BRITISH_SPORTS.values()
    )
    html = f"""
    <div style="position:fixed;bottom:24px;left:24px;z-index:9999;background:#fff;
        padding:10px 14px;border-radius:8px;font:13px/1.5 system-ui;
        box-shadow:0 2px 10px rgba(0,0,0,.2)">
      <strong>Sports britanniques</strong>{legend}
      <small>OSM · {SNAPSHOT_DATE}</small>
    </div>
    <style>div span{{display:inline-block;width:11px;height:11px;border-radius:50%;
        margin-right:6px;vertical-align:middle}}</style>
    """
    m.get_root().html.add_child(folium.Element(html))
    print(f"Sports britanniques : {len(sel):,} sites".replace(",", " "))
    save(m, "british_sports")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)

    sub.add_parser("heatmap")

    p_sport = sub.add_parser("sport")
    p_sport.add_argument("--sport", required=True)
    p_sport.add_argument("--color", default="#1d3557")
    p_sport.add_argument("--name", required=True)

    sub.add_parser("british")

    args = parser.parse_args()
    if args.mode == "heatmap":
        build_heatmap()
    elif args.mode == "sport":
        build_sport(args.sport, args.color, args.name)
    elif args.mode == "british":
        build_british()


if __name__ == "__main__":
    main()
