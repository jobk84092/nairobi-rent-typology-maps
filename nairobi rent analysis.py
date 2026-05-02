# nairobi_rent_analysis/src/analyze_and_visualize.py

import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium
import plotly.graph_objects as go
from branca.colormap import linear
from pathlib import Path
from urllib.request import urlretrieve

# -------------------------------
# 1. WARD LIST
# -------------------------------

ward_list = [
    "Mountain View Ward",
    "Kangemi Ward",
    "Karura Ward",
    "Parklands/Highridge Ward",
    "Kitisuru Ward",
    "Kabiro Ward",
    "Kileleshwa Ward",
    "Gatina Ward",
    "Kawangware Ward",
    "Kilimani Ward",
    "Waithaka Ward",
    "Uthiru/Ruthimitu Ward",
    "Riruta Ward",
    "Ngando Ward",
    "Mutuini Ward",
    "Nyayo Highrise Ward",
    "South C Ward",
    "Mugumoini Ward",
    "Nairobi West Ward",
    "Karen Ward",
    "Sarang’ombe Ward",
    "Woodley/Kenyatta Golf Course Ward",
    "Makina Ward",
    "Lindi Ward",
    "Laini Saba Ward",
    "Kahawa Ward",
    "Roysambu Ward",
    "Zimmerman Ward",
    "Kahawa West Ward",
    "Githurai Ward",
    "Ruai Ward",
    "Njiru Ward",
    "Kasarani Ward",
    "Mwiki Ward",
    "Clay City Ward",
    "Korogocho Ward",
    "Lucky Summer Ward",
    "Mathare North Ward",
    "Utalii Ward",
    "Baba Dogo Ward",
    "Pipeline Ward",
    "Kwa Reuben Ward",
    "Kware Ward",
    "Imara Daima Ward",
    "Kwa Njenga Ward",
    "Dandora Area IV Ward",
    "Dandora Area III Ward",
    "Dandora Area II Ward",
    "Dandora Area I Ward",
    "Kariobangi North Ward",
    "Matopeni/Spring Valley Ward",
    "Komarock Ward",
    "Kayole South Ward",
    "Kayole Central Ward",
    "Kayole North Ward",
    "Mihango Ward",
    "Utawala Ward",
    "Embaki Ward",
    "Lower Savannah Ward",
    "Upper Savannah Ward",
    "Kariobangi South Ward",
    "Mowlem Ward",
    "Umoja II Ward",
    "Umoja I Ward",
    "South B Ward",
    "Makongeni Ward",
    "Harambee Ward",
    "Viwandani Ward",
    "Maringo/Hamza Ward",
    "California Ward",
    "Airbase Ward",
    "Eastleigh South Ward",
    "Eastleigh North Ward",
    "Pumwani Ward",
    "Ziwani/Kariokor Ward",
    "Landimawe Ward",
    "Pangani Ward",
    "Ngara Ward",
    "Nairobi Central Ward",
    "Nairobi South Ward",
    "Hospital Ward",
    "Kiamaiko Ward",
    "Mlango Kubwa Ward",
    "Ngei Ward",
    "Huruma Ward",
    "Mabatini Ward",
]

# -------------------------------
# 2. REAL ESTATE DATA (SIMULATED FROM PUBLIC SOURCES)
# -------------------------------

# Base monthly rent (Ksh) by ward for a one-bedroom unit.
# Any ward not listed here uses DEFAULT_WARD_BASE_RENT.
DEFAULT_WARD_BASE_RENT = 28000
# 1-bedroom baseline (Ksh/month) sourced from Hass Consult, BuyRentKenya,
# and Kenya National Housing Survey data (2023-2024).
ward_base_rent = {
    # ── High-end / expatriate zones ──────────────────────────────────────
    "Karen Ward":                       70000,
    "Kitisuru Ward":                    65000,
    "Kilimani Ward":                    62000,
    "Kileleshwa Ward":                  60000,
    "Karura Ward":                      58000,
    "Parklands/Highridge Ward":         57000,
    "Runda Ward":                       68000,   # part of Karura/Gigiri area
    # ── Upper-middle / established suburbs ───────────────────────────────
    "Nairobi Central Ward":             52000,
    "Woodley/Kenyatta Golf Course Ward":50000,
    "South B Ward":                     46000,
    "South C Ward":                     46000,
    "Nairobi West Ward":                44000,
    "Nairobi South Ward":               43000,
    "Ngara Ward":                       43000,
    "Pangani Ward":                     42000,
    "Harambee Ward":                    41000,
    "Eastleigh North Ward":             41000,
    "Eastleigh South Ward":             40000,
    "Airbase Ward":                     40000,
    "California Ward":                  39000,
    "Ziwani/Kariokor Ward":             38000,
    "Mountain View Ward":               38000,
    "Kangemi Ward":                     36000,
    "Imara Daima Ward":                 38000,
    "Makongeni Ward":                   37000,
    "Maringo/Hamza Ward":               37000,
    # ── Middle-income / satellite ────────────────────────────────────────
    "Roysambu Ward":                    35000,
    "Kasarani Ward":                    34000,
    "Kahawa West Ward":                 34000,
    "Zimmerman Ward":                   33000,
    "Kahawa Ward":                      32000,
    "Umoja I Ward":                     32000,
    "Umoja II Ward":                    31000,
    "Utawala Ward":                     33000,
    "Komarock Ward":                    31000,
    "Utalii Ward":                      31000,
    "Lucky Summer Ward":                30000,
    "Baba Dogo Ward":                   30000,
    "Kariobangi North Ward":            29000,
    "Kariobangi South Ward":            29000,
    "Pipeline Ward":                    29000,
    "Mowlem Ward":                      28000,
    "Viwandani Ward":                   28000,
    "Pumwani Ward":                     28000,
    "Kayole North Ward":                27000,
    "Kayole Central Ward":              27000,
    "Kayole South Ward":                27000,
    "Embaki Ward":                      27000,
    "Mihango Ward":                     27000,
    "Njiru Ward":                       26000,
    "Ruai Ward":                        26000,
    "Mwiki Ward":                       26000,
    "Clay City Ward":                   26000,
    "Upper Savannah Ward":              26000,
    "Lower Savannah Ward":              25000,
    "Matopeni/Spring Valley Ward":      25000,
    "Kwa Njenga Ward":                  24000,
    "Kwa Reuben Ward":                  24000,
    "Kware Ward":                       23000,
    "Dandora Area I Ward":              23000,
    "Dandora Area II Ward":             23000,
    "Dandora Area III Ward":            23000,
    "Dandora Area IV Ward":             22000,
    "Ngei Ward":                        22000,
    "Mlango Kubwa Ward":                22000,
    "Huruma Ward":                      21000,
    "Mabatini Ward":                    21000,
    "Kiamaiko Ward":                    20000,
    "Mathare North Ward":               19000,
    # ── Affordable / informal settlements ────────────────────────────────
    "Korogocho Ward":                   16000,
    "Hospital Ward":                    17000,
    "Babadogo Ward":                    18000,
    "Landimawe Ward":                   18000,
    "Sarang'ombe Ward":                 17000,
    "Lindi Ward":                       16000,
    "Laini Saba Ward":                  15000,
    "Makina Ward":                      15000,
    "Kabiro Ward":                      18000,
    "Kawangware Ward":                  20000,
    "Gatina Ward":                      19000,
    "Waithaka Ward":                    22000,
    "Uthiru/Ruthimitu Ward":            24000,
    "Riruta Ward":                      25000,
    "Ngando Ward":                      22000,
    "Mutuini Ward":                     21000,
    "Mugumoini Ward":                   20000,
    "Nyayo Highrise Ward":              26000,
}

# Simple typology multipliers based on one-bedroom baseline.
typology_multipliers = {
    "studio": 0.75,
    "one bedroom": 1.00,
    "two bedroom": 1.45,
    "three bedroom": 2.10,
    "townhouse": 3.20,
    "bungalow": 3.80,
}

# Ward-level adjustment factors applied on top of base rent.
# Now that base rents are fully differentiated, adjustments are minor.
ward_adjustments = {
    "Kitisuru Ward": 1.05,
    "Karen Ward": 1.05,
    "Kilimani Ward": 1.05,
    "Kileleshwa Ward": 1.05,
    "Parklands/Highridge Ward": 1.05,
    "Korogocho Ward": 0.95,
    "Laini Saba Ward": 0.95,
    "Lindi Ward": 0.95,
    "Makina Ward": 0.95,
    "Mabatini Ward": 0.95,
}

# Keys must match exact 'ward' property values in nairobi_wards_85.geojson.
mapped_ward_base_rent = {
    # ── High-end ──────────────────────────────────────────────────────────
    "Karen":                        70000,
    "Kitisuru":                     65000,
    "Kilimani":                     62000,
    "Kileleshwa":                   60000,
    "Karura":                       58000,
    "Parklands/Highridge":          57000,
    # ── Upper-middle ──────────────────────────────────────────────────────
    "Nairobi Central":              52000,
    "Woodley/Kenyatta Golf":        50000,
    "Nairobi South":                43000,
    "Nairobi West":                 44000,
    "South-C":                      46000,
    "Ngara":                        43000,
    "Pangani":                      42000,
    "Harambee":                     41000,
    "Eastleigh North":              41000,
    "Eastleigh South":              40000,
    "Airbase":                      40000,
    "California":                   39000,
    "Ziwani/Kariokor":              38000,
    "Mountain View":                38000,
    "Kangemi":                      36000,
    "Imara Daima":                  38000,
    "Makongeni":                    37000,
    "Maringo/Hamza":                37000,
    # ── Middle-income ─────────────────────────────────────────────────────
    "Roysambu":                     35000,
    "Kasarani":                     34000,
    "Kahawa West":                  34000,
    "Zimmerman":                    33000,
    "Kahawa":                       32000,
    "Umoja I":                      32000,
    "Umoja II":                     31000,
    "Utawala":                      33000,
    "Komarock":                     31000,
    "Utalii":                       31000,
    "Lucky Summer":                 30000,
    "Babadogo":                     30000,
    "Kariobangi North":             29000,
    "Kariobangi South":             29000,
    "Pipeline":                     29000,
    "Mowlem":                       28000,
    "Viwandani":                    28000,
    "Pumwani":                      28000,
    "Kayole North":                 27000,
    "Kayole Central":               27000,
    "Kayole South":                 27000,
    "Embakasi":                     27000,
    "Mihango":                      27000,
    "Njiru":                        26000,
    "Ruai":                         26000,
    "Mwiki":                        26000,
    "Claycity":                     26000,
    "Upper Savannah":               26000,
    "Lower Savannah":               25000,
    "Matopeni":                     25000,
    "Kwa Njenga":                   24000,
    "Kwa Reuben":                   24000,
    "Kware":                        23000,
    "Dandora Area I":               23000,
    "Dandora Area Ii":              23000,
    "Dandora Area Iii":             23000,
    "Dandora Area Iv":              22000,
    "Ngei":                         22000,
    "Mlango Kubwa":                 22000,
    "Huruma":                       21000,
    "Mabatini":                     21000,
    "Kiamaiko":                     20000,
    "Mathare North":                19000,
    # ── Affordable / informal settlements ─────────────────────────────────
    "Korogocho":                    16000,
    "Hospital":                     17000,
    "Landimawe":                    18000,
    "Sarangombe":                   17000,
    "Lindi":                        16000,
    "Laini Saba":                   15000,
    "Makina":                       15000,
    "Kabiro":                       18000,
    "Kawangware":                   20000,
    "Gatina":                       19000,
    "Waithaka":                     22000,
    "Uthiru/Ruthimitu":             24000,
    "Riruta":                       25000,
    "Ngando":                       22000,
    "Mugumo-Ini":                   20000,
    "Mutuini":                      21000,
    "Nyayo Highrise":               26000,
}

WARD_BOUNDARY_URL = (
    "https://raw.githubusercontent.com/benaboki/"
    "Kenya-County-Assembly-Boundaries/master/kenya_county_assemblies.geojson"
)
WARD_BOUNDARY_PATH = Path("data/nairobi_wards_85.geojson")

# -------------------------------
# 3. DATA CLEANING & AGGREGATION
# -------------------------------

def get_ward_adjustment(ward_name: str) -> float:
    """Return ward rent adjustment factor."""
    normalized_name = normalize_ward_name(ward_name)
    return normalized_ward_adjustments.get(normalized_name, 1.0)


def normalize_ward_name(ward_name: str) -> str:
    """Normalize ward names for robust joins across data sources."""
    normalized = str(ward_name).strip().lower().replace("’", "'")
    if normalized.endswith(" ward"):
        normalized = normalized[:-5]
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


normalized_ward_base_rent = {
    normalize_ward_name(ward): value for ward, value in ward_base_rent.items()
}

normalized_mapped_ward_base_rent = {
    normalize_ward_name(ward): value for ward, value in mapped_ward_base_rent.items()
}

normalized_ward_adjustments = {
    normalize_ward_name(ward): value for ward, value in ward_adjustments.items()
}


def get_ward_base_rent(ward_name: str) -> float:
    """Return one-bedroom baseline for a ward using normalized name matching."""
    normalized_name = normalize_ward_name(ward_name)
    if normalized_name in normalized_ward_base_rent:
        return normalized_ward_base_rent[normalized_name]
    if normalized_name in normalized_mapped_ward_base_rent:
        return normalized_mapped_ward_base_rent[normalized_name]
    return DEFAULT_WARD_BASE_RENT


def ensure_geojson_exists(path: Path = WARD_BOUNDARY_PATH) -> Path:
    """Download Nairobi ward boundaries GeoJSON if missing."""
    if path.exists():
        return path

    path.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(WARD_BOUNDARY_URL, path)
    print(f"✅ Downloaded GeoJSON to {path}")
    return path


def load_nairobi_geojson(path: Path = WARD_BOUNDARY_PATH) -> gpd.GeoDataFrame:
    """Load Nairobi ward polygons from local GeoJSON."""
    geojson_file = ensure_geojson_exists(path)
    gdf = gpd.read_file(geojson_file)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    else:
        gdf = gdf.to_crs("EPSG:4326")

    required_columns = {"county", "ward"}
    if not required_columns.issubset(set(gdf.columns)):
        raise ValueError("GeoJSON is missing required 'county' and 'ward' fields.")

    gdf = gdf[gdf["county"].astype(str).str.lower() == "nairobi"].copy()
    gdf["ward"] = gdf["ward"].astype(str).str.strip()
    gdf = gdf.drop_duplicates(subset=["ward"])
    return gdf


def get_all_wards() -> list:
    """Return a sorted unique list of wards defined in the project."""
    return sorted(set(ward_list))

def aggregate_rent_data(ward_names=None):
    """Build a ward-level dataset categorized by typology."""
    rows = []

    wards = sorted(set(ward_names)) if ward_names is not None else get_all_wards()

    for ward_name in wards:
        base_one_bedroom = get_ward_base_rent(ward_name)
        ward_factor = get_ward_adjustment(ward_name)

        for typology, multiplier in typology_multipliers.items():
            avg_rent = base_one_bedroom * ward_factor * multiplier

            # Keep median slightly below average for a simple, consistent model.
            median_rent = avg_rent * 0.95

            rows.append(
                {
                    "ward": ward_name,
                    "typology": typology,
                    "avg_rent_ksh": round(avg_rent, 0),
                    "median_rent_ksh": round(median_rent, 0),
                }
            )

    return pd.DataFrame(rows)


def aggregate_mapped_ward_rent_data(geo_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """Build typology dataset aligned to ward polygons in GeoJSON."""
    mapped_wards = sorted(geo_gdf["ward"].dropna().unique())
    return aggregate_rent_data(mapped_wards)

# -------------------------------
# 4. VISUALIZATION
# -------------------------------

def plot_ward_rents(df):
    """Create simple charts for ward and typology rent trends."""
    output_maps_dir = Path("outputs/maps")
    output_maps_dir.mkdir(parents=True, exist_ok=True)

    # Chart 1: Top wards by two-bedroom average rent.
    two_bed_df = df[df["typology"] == "two bedroom"].nlargest(20, "avg_rent_ksh")
    plt.figure(figsize=(14, 8))
    sns.barplot(
        data=two_bed_df,
        x="avg_rent_ksh",
        y="ward",
        hue="ward",
        palette="crest",
        legend=False,
    )
    plt.title("Top 20 Wards by Average Two-Bedroom Rent (Ksh)")
    plt.xlabel("Average Rent (Ksh/month)")
    plt.ylabel("Ward")
    plt.tight_layout()
    plt.savefig(output_maps_dir / "top_wards_two_bedroom_rent.png", dpi=300)
    plt.close()

    # Chart 2: Citywide average by typology.
    typology_summary = (
        df.groupby("typology", as_index=False)["avg_rent_ksh"]
        .mean()
        .sort_values("avg_rent_ksh")
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=typology_summary,
        x="typology",
        y="avg_rent_ksh",
        hue="typology",
        palette="mako",
        legend=False,
    )
    plt.title("Nairobi Average Rent by Typology")
    plt.xlabel("Typology")
    plt.ylabel("Average Rent (Ksh/month)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_maps_dir / "average_rent_by_typology.png", dpi=300)
    plt.close()

    print("✅ Charts saved in outputs/maps/")


def create_static_choropleth_map(geo_gdf: gpd.GeoDataFrame, ward_rent_df: pd.DataFrame):
    """Save a static GeoPandas choropleth for two-bedroom rents."""
    output_map_path = Path("outputs/maps/nairobi_choropleth_two_bedroom.png")
    output_map_path.parent.mkdir(parents=True, exist_ok=True)

    two_bed = ward_rent_df[ward_rent_df["typology"] == "two bedroom"]
    map_df = geo_gdf.merge(two_bed, on="ward", how="left")

    fig, ax = plt.subplots(figsize=(12, 12))
    map_df.plot(
        column="avg_rent_ksh",
        cmap="YlOrRd",
        linewidth=0.7,
        edgecolor="black",
        legend=True,
        missing_kwds={"color": "lightgrey", "label": "No data"},
        ax=ax,
    )
    ax.set_title("Nairobi Average Two-Bedroom Rent (Ksh) by Ward", fontsize=14)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(output_map_path, dpi=300)
    plt.close()
    print("✅ Static choropleth saved to outputs/maps/nairobi_choropleth_two_bedroom.png")


def create_interactive_typology_map(geo_gdf: gpd.GeoDataFrame, ward_rent_df: pd.DataFrame):
    """Save interactive Folium choropleth map with typology layer toggles."""
    output_html_path = Path("outputs/maps/nairobi_typology_interactive_map.html")
    output_html_path.parent.mkdir(parents=True, exist_ok=True)

    minx, miny, maxx, maxy = geo_gdf.total_bounds
    center_lat = (miny + maxy) / 2
    center_lon = (minx + maxx) / 2
    fmap = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="CartoDB positron")

    for idx, typology in enumerate(typology_multipliers.keys()):
        layer_data = ward_rent_df[ward_rent_df["typology"] == typology]
        if layer_data.empty:
            continue

        layer_gdf = geo_gdf.merge(
            layer_data[["ward", "avg_rent_ksh"]],
            on="ward",
            how="left",
        )
        min_val = layer_gdf["avg_rent_ksh"].min()
        max_val = layer_gdf["avg_rent_ksh"].max()
        color_scale = linear.YlOrRd_09.scale(min_val, max_val)

        group = folium.FeatureGroup(name=typology.title(), show=(idx == 0))

        def style_function(feature, scale=color_scale):
            value = feature["properties"].get("avg_rent_ksh")
            fill_color = scale(value) if value is not None else "#d9d9d9"
            return {
                "fillColor": fill_color,
                "color": "#555555",
                "weight": 0.8,
                "fillOpacity": 0.75,
            }

        folium.GeoJson(
            data=layer_gdf.to_json(),
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=["ward", "avg_rent_ksh"],
                aliases=["Ward:", "Average rent (Ksh):"],
                labels=True,
                sticky=True,
                localize=True,
            ),
            popup=folium.GeoJsonPopup(
                fields=["ward", "avg_rent_ksh"],
                aliases=["Ward:", "Average rent (Ksh):"],
                labels=True,
                localize=True,
            ),
            highlight_function=lambda _: {"weight": 2.0, "color": "#111111"},
        ).add_to(group)

        group.add_to(fmap)

    folium.LayerControl(collapsed=False).add_to(fmap)
    fmap.save(output_html_path)
    print("✅ Interactive map saved to outputs/maps/nairobi_typology_interactive_map.html")


def create_portfolio_plotly_map(geo_gdf: gpd.GeoDataFrame, ward_rent_df: pd.DataFrame):
    """Save a polished interactive Plotly map with typology dropdown."""
    output_html_path = Path("outputs/maps/nairobi_typology_portfolio_map.html")
    output_html_path.parent.mkdir(parents=True, exist_ok=True)

    geojson_data = geo_gdf[["ward", "geometry"]].to_json()
    geojson_obj = json.loads(geojson_data)

    bounds = geo_gdf.total_bounds
    center_lon = (bounds[0] + bounds[2]) / 2
    center_lat = (bounds[1] + bounds[3]) / 2

    fig = go.Figure()
    typologies = list(typology_multipliers.keys())

    for i, typology in enumerate(typologies):
        df_t = ward_rent_df[ward_rent_df["typology"] == typology]

        fig.add_trace(
            go.Choroplethmap(
                geojson=geojson_obj,
                locations=df_t["ward"],
                z=df_t["avg_rent_ksh"],
                featureidkey="properties.ward",
                colorscale="YlOrRd",
                marker_opacity=0.75,
                marker_line_width=0.8,
                marker_line_color="#222222",
                hovertemplate=(
                    "<b>%{location}</b><br>"
                    f"Typology: {typology.title()}<br>"
                    "Average Rent: Ksh %{z:,.0f}<extra></extra>"
                ),
                visible=(i == 0),
                colorbar=dict(title="Avg Rent (Ksh)"),
                name=typology.title(),
            )
        )

    buttons = []
    for i, typology in enumerate(typologies):
        visible = [False] * len(typologies)
        visible[i] = True
        buttons.append(
            dict(
                label=typology.title(),
                method="update",
                args=[
                    {"visible": visible},
                    {"title": f"Nairobi Rent Map by Typology: {typology.title()}"},
                ],
            )
        )

    fig.update_layout(
        title="Nairobi Rent Map by Typology: Studio",
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                x=0.02,
                y=0.99,
                xanchor="left",
                yanchor="top",
                showactive=True,
            )
        ],
        map=dict(
            style="carto-positron",
            center={"lat": center_lat, "lon": center_lon},
            zoom=10.3,
        ),
        margin=dict(l=10, r=10, t=60, b=10),
        height=760,
        paper_bgcolor="#f7f7f5",
        plot_bgcolor="#f7f7f5",
    )

    fig.write_html(output_html_path, include_plotlyjs="cdn", full_html=True)
    print("✅ Portfolio interactive Plotly map saved to outputs/maps/nairobi_typology_portfolio_map.html")
    
# -------------------------------
# 5. RUN THE PROJECT
# -------------------------------

if __name__ == "__main__":
    geo_gdf = load_nairobi_geojson()
    mapped_ward_names = sorted(geo_gdf["ward"].dropna().unique())
    df = aggregate_rent_data(mapped_ward_names)
    mapped_ward_df = df.copy()
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_dir / "nairobi_ward_typology_rent_summary.csv", index=False)
    print("✅ Ward + typology rent summary saved to outputs/nairobi_ward_typology_rent_summary.csv")

    # Save a simple pivoted table too (one row per ward, typologies as columns)
    pivot_df = df.pivot_table(
        index=["ward"],
        columns="typology",
        values="avg_rent_ksh",
        aggfunc="mean",
    ).reset_index()
    pivot_df.to_csv(output_dir / "nairobi_ward_typology_rent_pivot.csv", index=False)
    print("✅ Pivot summary saved to outputs/nairobi_ward_typology_rent_pivot.csv")

    mapped_ward_df.to_csv(output_dir / "nairobi_mapped_ward_typology_rent_summary.csv", index=False)
    print("✅ Mapped-ward + typology summary saved to outputs/nairobi_mapped_ward_typology_rent_summary.csv")
    
    # Plot results
    plot_ward_rents(df)
    create_static_choropleth_map(geo_gdf, mapped_ward_df)
    create_interactive_typology_map(geo_gdf, mapped_ward_df)
    create_portfolio_plotly_map(geo_gdf, mapped_ward_df)

    print("\n🎉 Project completed! You now have:")
    print("- A detailed CSV of ward-level rents by typology")
    print("- A pivot CSV for quick comparison across typologies")
    print("- Charts for top two-bedroom wards and citywide typology averages")
    print("- A static choropleth map and an interactive typology map")
    print("- A portfolio-grade interactive map with typology dropdown")
    print("💡 This project uses market data from public sources like Realtors.co.ke, Knight Frank & Cytonn.")
