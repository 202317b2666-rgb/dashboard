import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="World Map Clean View", layout="wide")

# Title
st.markdown("<h1 style='text-align:center;'>🌍 Clean World Map View</h1>", unsafe_allow_html=True)

# Load files
hex_df = pd.read_csv("Hex.csv")
with open("countries.geo.json", "r") as f:
    geojson_data = json.load(f)

# Merge HEX colors with geojson country codes
hex_df = hex_df.rename(columns={"iso_alpha": "ISO_A3"})

# Create map
fig = px.choropleth(
    hex_df,
    geojson=geojson_data,
    locations="ISO_A3",
    color="hex",
    color_discrete_map=hex_df.set_index("ISO_A3")["hex"].to_dict(),
    hover_name="country",
)

# Clean look settings
fig.update_geos(
    showcountries=True,
    showcoastlines=False,
    projection_type="natural earth",
    bgcolor="#87CEEB"  # light blue ocean
)

fig.update_layout(
    margin={"r":0, "t":0, "l":0, "b":0},
    height=700,
    paper_bgcolor="#87CEEB",  # blue background
    plot_bgcolor="#87CEEB",
)

st.plotly_chart(fig, use_container_width=True)
