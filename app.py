import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.title("🌍 World Map — Interactive Highlight")

# Load Hex / map data
hex_df = pd.read_csv("Hex.csv")  # country, iso_alpha, hex
with open("countries.geo.json") as f:
    geojson = json.load(f)

# Base Choropleth map
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations="iso_alpha",
    color="hex",  # dummy color, just for visualization
    color_continuous_scale="Blues",
    hover_name="country",
    labels={"iso_alpha": "ISO3"},
)

# Map styling
fig.update_geos(
    visible=False,
    showcountries=True,
    countrycolor="white",
    showland=True,
    landcolor="rgb(28, 107, 160)",  # ocean-blue background
)

# Hover + click effect
fig.update_traces(
    marker_line_width=0.5,
    marker_line_color="rgb(0,0,0)",
    hovertemplate="<b>%{hovertext}</b>",  # shows country name only
    hoverlabel=dict(bgcolor="white", font_size=12),
    selector=dict(type="choropleth")
)

# Optional: simulate pop-out on hover by changing opacity/color
fig.update_traces(
    hoverinfo="location+text",
    marker=dict(line=dict(width=0.5)),
    selector=dict(type="choropleth")
)

# Show map in Streamlit
clicked = st.plotly_chart(fig, use_container_width=True)

# Future: we can add a Streamlit event listener to detect clicks and highlight
st.info("Hover over a country to highlight. Click effect coming next.")
