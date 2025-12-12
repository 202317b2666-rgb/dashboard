# app.py
import streamlit as st
import pandas as pd
import pydeck as pdk
import json

st.set_page_config(layout="wide")
st.title("Interactive World Map (2D Highlight)")

# 1️⃣ Load your datasets
countries_gdf = json.load(open("countries.geo.json", "r"))
hex_df = pd.read_csv("Hex.csv")  # columns: country, iso_alpha, hex

# 2️⃣ Prepare data for PyDeck
# Map GeoJSON features to a list of dicts for PyDeck
country_polygons = []
for feature in countries_gdf['features']:
    iso = feature['properties']['ISO_A3']
    country_name = feature['properties']['ADMIN']
    coords = feature['geometry']['coordinates']
    hex_color = hex_df.loc[hex_df['iso_alpha'] == iso, 'hex'].values
    color = [0, 0, 0] if len(hex_color) == 0 else [int(hex_color[0][1:3],16),
                                                   int(hex_color[0][3:5],16),
                                                   int(hex_color[0][5:7],16)]
    country_polygons.append({
        "name": country_name,
        "iso": iso,
        "coordinates": coords,
        "color": color
    })

# 3️⃣ Flatten coordinates for PolygonLayer (PyDeck expects a list of [lng, lat])
def flatten_coords(coords):
    # Handles multipolygon vs polygon
    if isinstance(coords[0][0], list):
        # MultiPolygon
        return [c for part in coords for c in part]
    else:
        return coords

for country in country_polygons:
    country["coordinates"] = flatten_coords(country["coordinates"])

# 4️⃣ Prepare PyDeck Layer
selected_country = st.session_state.get("selected_country", None)

def get_fill_color(country):
    if selected_country and country["iso"] == selected_country:
        # Highlighted country in brighter color
        return [255, 0, 0]
    return country["color"]

polygon_layer = pdk.Layer(
    "PolygonLayer",
    data=country_polygons,
    get_polygon="coordinates",
    get_fill_color=get_fill_color,
    get_line_color=[0,0,0],
    pickable=True,
    auto_highlight=True
)

# 5️⃣ Deck object
deck = pdk.Deck(
    layers=[polygon_layer],
    initial_view_state=pdk.ViewState(
        latitude=10,
        longitude=0,
        zoom=1.5,
        pitch=0,
    ),
    tooltip={"text": "{name}"},
)

# 6️⃣ Show PyDeck chart and capture click
event = st.pydeck_chart(deck, use_container_width=True, selection_mode="single-object", on_select="rerun")

if event is not None and len(event.selection) > 0:
    st.session_state.selected_country = event.selection[0]["object"]["iso"]

# 7️⃣ Sidebar info
if selected_country:
    country_name = next(c["name"] for c in country_polygons if c["iso"] == selected_country)
    st.sidebar.markdown(f"### Selected Country: {country_name}")
