# Nairobi Rent Typology Mapping

![Project Banner](assets/banner.svg)

Interactive and static rent analytics for Nairobi using typology-based pricing and geospatial visualization.

## Live Demo

- GitHub Pages site: https://jobk84092.github.io/nairobi-rent-typology-maps/
- Local landing page: [index.html](index.html)
- Portfolio interactive map: [outputs/maps/nairobi_typology_portfolio_map.html](outputs/maps/nairobi_typology_portfolio_map.html)

## What This Project Shows

- Rent estimates by typology: studio, one bedroom, two bedroom, three bedroom, townhouse, bungalow.
- Ward-level tabular analytics for broad Nairobi coverage.
- Geo-enabled zone mapping from ArcGIS boundaries.
- Portfolio-grade interactive maps built with Folium and Plotly.

## Visual Highlights

### Static Choropleth

![Nairobi Two Bedroom Choropleth](outputs/maps/nairobi_choropleth_two_bedroom.png)

### Typology Summary

![Average Rent by Typology](outputs/maps/average_rent_by_typology.png)

### Top Two-Bedroom Areas

![Top Wards Two Bedroom Rent](outputs/maps/top_wards_two_bedroom_rent.png)

## Data Inputs

- ArcGIS boundary layer (downloaded automatically when missing):
  - https://www.arcgis.com/home/item.html?id=73393b8d209542b2a9f039caf05aca4e#visualize
  - Queried as GeoJSON from ArcGIS REST.

## Run Locally

1. Create and activate a virtual environment.
2. Install requirements.
3. Run the analysis script.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python "nairobi rent analysis.py"
```

## Methodology Notebook

- Short walkthrough notebook: [methodology_walkthrough.ipynb](methodology_walkthrough.ipynb)

## Generated Outputs

### Tables

- `outputs/nairobi_ward_typology_rent_summary.csv`
- `outputs/nairobi_ward_typology_rent_pivot.csv`
- `outputs/nairobi_mapped_ward_typology_rent_summary.csv`

### Visuals and Interactive Maps

- `outputs/maps/top_wards_two_bedroom_rent.png`
- `outputs/maps/average_rent_by_typology.png`
- `outputs/maps/nairobi_choropleth_two_bedroom.png`
- `outputs/maps/nairobi_typology_interactive_map.html`
- `outputs/maps/nairobi_typology_portfolio_map.html`

## Notes

- Rent values are modeled from simplified assumptions for analytics demonstration.
- This ArcGIS layer currently returns aggregated zones for mapping from the selected endpoint.
- The code is structured so a full ward polygon source can be swapped in later with minimal changes.

## License

See `License.md`.
