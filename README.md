# Creating the Missing Data — Sports Facilities in Africa via OpenStreetMap

> **The general idea:** in many domains there is *no reliable open data at all*.
> One response is to **build it yourself** from citizen sources — with explicit
> limits, but real upsides. This repo applies that method to a concrete case:
> mapping sports facilities across Africa with **OpenStreetMap**, where the
> spatial data reveals patterns (e.g. the footprint of British sports in former
> Commonwealth colonies) that no aggregate statistic would show — and can be
> re-run every year to *track evolution*.

🌍 **Live site:** https://thepriben.github.io/sports-facilities-africa-osm-2025/
📄 **Preprint (FR):** [`preprint/preprint_fr.md`](preprint/preprint_fr.md)
🗓️ **Snapshot:** Geofabrik *Africa* extract, **20 March 2025**

---

## Why this project

Official statistics on sports infrastructure in Africa are scattered, heterogeneous,
rarely geolocated, and often missing. Rather than waiting for a reference dataset
that does not exist, we use what is already there: **OpenStreetMap (OSM)**, a global
citizen mapping project.

The result is **not exhaustive and not representative** — OSM coverage depends on
local communities. But it is:

- **Open** — anyone can reproduce or extend it (data under ODbL).
- **Geolocated** — every site is a point on the map.
- **Reproducible** — the whole pipeline can be re-run on next year's extract (or on
  past dumps from 2015, 2020…) to turn a single snapshot into a **time series**.

## Key findings (2025 snapshot)

- **113,685** geolocated sports sites · **183** distinct sports.
- **Football** dominates (≈ 55,500 sites, nearly half of all tagged facilities).
- **Netball** ranks 5th (3,405 sites) — a discreet sport with a major footprint,
  concentrated in East and Southern Africa.
- **British sports** (cricket, rugby union, field hockey, bowls) map closely onto
  former Commonwealth territories, and are nearly absent from francophone countries.

Full analysis in the [preprint](preprint/preprint_fr.md).

<p align="center">
  <img src="images/soccer_zoom_map.png" width="420" alt="Football facilities, zoomed map" />
  <img src="images/netball_maps.png" width="420" alt="Netball facilities map" />
</p>

## Repository structure

```
.
├── data/
│   ├── sports_facilities.csv   # raw extract (geometry, sport) — ~113k rows
│   └── sport_counts.csv        # cleaned per-sport counts (regenerated)
├── scripts/
│   ├── common.py               # shared helpers (geometry, sport normalization)
│   ├── build_counts.py         # counts CSV + docs/data/sport_counts.json
│   └── make_map.py             # Folium maps: heatmap / single sport / British sports
├── docs/                       # GitHub Pages site (served from /docs)
│   ├── index.html
│   ├── assets/                 # css, js, images
│   ├── data/sport_counts.json
│   └── maps/                   # interactive Folium HTML maps
├── preprint/preprint_fr.md     # the article (French)
├── images/                     # static figures
├── requirements.txt
└── LICENSE
```

## Reproduce it

### 1. Extract from OpenStreetMap (one-off, heavy)

```bash
# Download the Africa extract (~5 GB)
wget -c -O africa-latest.osm.pbf https://download.geofabrik.de/africa-latest.osm.pbf

# Filter relevant features
osmium tags-filter africa-latest.osm.pbf \
  nwr/leisure=pitch nwr/leisure=stadium nwr/building=stadium \
  --overwrite -o filtered_data.osm

# Export to GeoJSON, then keep (geometry, sport) → data/sports_facilities.csv
osmium export filtered_data.osm -f geojson --overwrite -o temp.geojson
```

### 2. Analyze & map (Python)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python scripts/build_counts.py                 # counts + JSON for the site
python scripts/make_map.py heatmap             # density heatmap
python scripts/make_map.py sport --sport netball --color "#1d3557" --name netball
python scripts/make_map.py british             # cricket / rugby / hockey / bowls
```

Maps are written to `docs/maps/`, ready to be served by GitHub Pages.

### 3. Refresh next year

Re-run the same steps on a newer extract (or a historical dump) and commit the
regenerated `data/` and `docs/maps/`. Comparing snapshots reveals how OSM coverage
and the sporting landscape change over time.

## Data & license

- **Code:** MIT (see [`LICENSE`](LICENSE)).
- **Data:** derived from OpenStreetMap, © OpenStreetMap contributors, under the
  [Open Database License (ODbL)](https://www.openstreetmap.org/copyright).

## Author

[**thepriben**](https://github.com/thepriben) (Benoît Prieur).
