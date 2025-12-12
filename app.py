# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide")
st.title("🌍 Interactive World Map — Hover Highlight & Click Zoom")

# --- Load Data ---
# World GeoJSON
with open("countries.geo.json", "r") as f:
    geojson_data = json.load(f)

# Sample color/hex mapping CSV
hex_df = pd.read_csv("Hex.csv")  # columns: country, iso_alpha, junk, hex
hex_df['iso_alpha'] = hex_df['iso_alpha'].str.upper().str.strip()

# Merge color with geojson
color_map = dict(zip(hex_df['iso_alpha'], hex_df['hex']))

# --- Create Map ---
fig = px.choropleth(
    hex_df,
    geojson=geojson_data,
    locations='iso_alpha',
    color='hex',  # Use color as dummy
    color_discrete_map=color_map,
    hover_name='country',  # Country name on hover
)

fig.update_geos(
    showcountries=True,
    showcoastlines=False,
    showocean=True,
    oceancolor='lightblue',
    projection_type='natural earth'
)

# Remove colorbar, we only use colors as fill
fig.update_layout(coloraxis_showscale=False)

# --- Hover + Click style ---
fig.update_traces(
    marker_line_width=0.5,       # thin border normally
    marker_line_color='white',
    hoverinfo="location",        # show country name on hover
    hoverlabel=dict(bgcolor="yellow", font_size=14, font_family="Arial"),
)

# Streamlit chart
st.plotly_chart(fig, use_container_width=True)
