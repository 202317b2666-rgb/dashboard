# app.py - Clean World Map (step 1)
import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="World Map — Clean View", layout="wide")
st.title("🌍 World Map — Clean View")
st.markdown("A clean, presentation-style world map. Background = ocean-blue, crisp country borders, no hover clutter.")

# ---- load hex colors (your file: hex.csv) ----
hex_df = pd.read_csv("Hex.csv", dtype=str)
hex_df.columns = hex_df.columns.str.strip()
# ensure iso column is uppercase and named ISO3 for mapping
hex_df["ISO3"] = hex_df["iso_alpha"].astype(str).str.upper().str.strip()
hex_df["hex"] = hex_df["hex"].astype(str).str.strip().replace({"": "#d3d3d3", None: "#d3d3d3"})

# ---- load geojson ----
with open("countries.geo.json", "r") as f:
    geojson = json.load(f)

# ---- build a color map from ISO3 -> hex ----
color_map = dict(zip(hex_df["ISO3"], hex_df["hex"]))

# ---- prepare a small dataframe of unique countries to feed px.choropleth ----
map_df = pd.DataFrame({"ISO3": list(color_map.keys())})
map_df["COLOR_KEY"] = map_df["ISO3"]  # categorical key for color mapping

# ---- create choropleth ----
fig = px.choropleth(
    map_df,
    geojson=geojson,
    locations="ISO3",
    color="COLOR_KEY",
    color_discrete_map=color_map,
    featureidkey="id",           # IMPORTANT: matches geojson feature['id']
    projection="natural earth",  # pleasant projection
)

# ---- style tweaks for a clean look ----
# remove hover popups / templates
fig.update_traces(hovertemplate=None, marker_line_width=0.4, marker_line_color="white")

# set ocean/land/background colors
fig.update_geos(
    showcountries=False,
    showcoastlines=False,
    showland=True,
    landcolor="rgba(255,255,255,0.98)",   # very slight off-white for land
    lakecolor="rgba(0,0,0,0)",
    bgcolor="rgba(0,0,0,0)",               # keep underlying geo transparent
    projection_scale=1
)

# set overall figure background to ocean-blue and remove margins
fig.update_layout(
    paper_bgcolor="#BEE9FF",   # page background (light sea-blue)
    plot_bgcolor="#BEE9FF",
    margin={"r":0, "t":10, "l":0, "b":0},
    coloraxis_showscale=False,  # hide colorbar/legend (we use direct colors)
    height=700,
)

# a thin subtle frame/shadow can be added via layout shapes if needed (optional)

# ---- render in Streamlit ----
st.plotly_chart(fig, use_container_width=True)
