import streamlit as st
import plotly.express as px
import json
import pandas as pd

st.set_page_config(layout="wide")

st.markdown(
    """
    <h2 style='text-align:center; margin-bottom:0px;'>🌍 World Map — Clean View</h2>
    <p style='text-align:center; color:#444;'>A clean, presentation-style world map with smooth hover effect.</p>
    """,
    unsafe_allow_html=True,
)

# --------------------
# Load HEX + GeoJSON
# --------------------
hex_df = pd.read_csv("HEX.csv")   # your file
geojson = json.load(open("countries.geo.json", "r"))

# Prepare Data
hex_df["iso_alpha"] = hex_df["iso_alpha"].str.strip().str.upper()
hex_df["hex"] = hex_df["hex"].fillna("#CCCCCC")

df = hex_df.rename(columns={"iso_alpha": "ISO3", "country": "Country"})
df["COLOR_KEY"] = df["hex"]

color_map = dict(zip(df["ISO3"], df["COLOR_KEY"]))

# --------------------
# Base World Map
# --------------------
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="ISO3",
    color="COLOR_KEY",
    color_discrete_map=color_map,
    featureidkey="id",
    projection="natural earth"
)

# --------------------
# Hover-Lift EFFECT
# --------------------
fig.update_traces(
    hovertemplate="<b>%{location}</b>",
    marker_line_width=0.8,
    marker_line_color="white",
    marker_opacity=0.95,
)

# When hovering → country brightens and border thickens (lift illusion)
fig.update_traces(
    selector=dict(),
    hoverlabel=dict(bgcolor="white", font_size=14, font_color="black")
)

# This makes hover country stand out strongly
fig.update_traces(
    marker=dict(line=dict(width=1.8, color="black"))
)

# --------------------
# Clean Layout + Ocean Blue
# --------------------
fig.update_geos(
    showcountries=False,
    showcoastlines=False,
    showland=True,
    landcolor="rgba(255,255,255,0.97)",  # light white
    bgcolor="#BEE9FF",                   # ocean blue background
)

fig.update_layout(
    paper_bgcolor="#BEE9FF",
    plot_bgcolor="#BEE9FF",
    margin=dict(r=0, t=10, l=0, b=0),
    height=680,
    coloraxis_showscale=False,
)

# --------------------
# Display Map
# --------------------
st.plotly_chart(fig, use_container_width=True)
