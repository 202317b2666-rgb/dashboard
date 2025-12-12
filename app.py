import pandas as pd
import streamlit as st
import plotly.express as px
import json

st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click on a country in the map to see detailed indicators over time.")

# Load HEX.csv
hex_df = pd.read_csv("HEX.csv")

# Clean column names
hex_df.columns = hex_df.columns.str.strip()

# Make sure ISO codes are uppercase
hex_df['iso_alpha'] = hex_df['iso_alpha'].str.upper().str.strip()

# Load GeoJSON
with open("countries.geo.json") as f:
    geojson = json.load(f)

# Plot choropleth map
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='hex',  # or any dummy column just for color
    hover_name='country',
    hover_data=['iso_alpha'],
    featureidkey="id",
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)
