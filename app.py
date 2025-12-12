# app.py
import streamlit as st
import pandas as pd
import json
import plotly.express as px

# --- 1️⃣ Load HEX color data ---
hex_df = pd.read_csv("Hex.csv")  # columns: country, iso_alpha, hex

# --- 2️⃣ Load GeoJSON data ---
with open("countries.geo.json") as f:
    geojson = json.load(f)

# --- 3️⃣ Plotly Choropleth Map ---
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='hex',
    color_discrete_map="identity",  # use exact HEX colors
    hover_name='country',
)

# --- 4️⃣ Update layout for hover & click effect ---
fig.update_geos(fitbounds="locations", visible=False)
fig.update_traces(
    marker_line_width=0.5,
    marker_line_color="white",
    hoverinfo="location+text",
    selector=dict(type="choropleth"),
)

# Add click effect: highlight selected country
selected_country = st.session_state.get("selected_country", None)

# Streamlit interaction
st.title("Interactive World Map")
st.write("Click a country to highlight it!")

clicked = st.plotly_chart(fig, use_container_width=True)

# Optional: Display selected country name (Plotly click in Streamlit is limited)
# For full click interactivity, Dash or JS integration is better.
