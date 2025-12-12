# app.py
import streamlit as st
import pandas as pd
import pydeck as pdk
import json

st.title("Interactive World Map - 2D")

# 1️⃣ Load your HEX color CSV
hex_df = pd.read_csv("Hex.csv")  # Columns: country, iso_alpha, hex

# Convert HEX to RGB for PyDeck
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

hex_df['rgb'] = hex_df['hex'].apply(hex_to_rgb)

# 2️⃣ Load GeoJSON
with open("countries.geo.json", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# 3️⃣ Merge colors into GeoJSON
for feature in geojson['features']:
    iso_code = feature['properties'].get('ISO_A3')
    match = hex_df[hex_df['iso_alpha'] == iso_code]
    if not match.empty:
        feature['properties']['rgb'] = match.iloc[0]['rgb']
    else:
        feature['properties']['rgb'] = [200, 200, 200]  # default gray

# 4️⃣ Define PyDeck Layer
geo_layer = pdk.Layer(
    "GeoJsonLayer",
    geojson,
    get_fill_color="properties.rgb",
    pickable=True,
    auto_highlight=True,
    stroked=True,
    get_line_color=[255, 255, 255],
    line_width_min_pixels=1,
)

# 5️⃣ Set viewport
view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=1.5,
    pitch=0,
)

# 6️⃣ Render the map
r = pdk.Deck(
    layers=[geo_layer],
    initial_view_state=view_state,
    tooltip={"text": "{NAME}"},
)

st.pydeck_chart(r)
