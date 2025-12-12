import streamlit as st
import pandas as pd
import json
import plotly.express as px

# --- Load Data ---
hex_df = pd.read_csv("Hex.csv")  # country, iso_alpha, hex
with open("countries.geo.json") as f:
    geojson = json.load(f)

# --- Map Figure ---
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='hex',
    color_discrete_map="identity",
    hover_name='country'
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_traces(marker_line_width=0.5, marker_line_color="white")

st.title("World Map")
st.plotly_chart(fig, use_container_width=True)

# --- Country Selection ---
selected_country = st.selectbox("Select country to view details", [""] + list(hex_df['country']))

# --- Show Modal with Figma design ---
if selected_country:
    with st.modal("Country Details"):
        st.markdown(f"### {selected_country}")
        # Embed your Figma SVG/PNG
        st.image(f"figma_designs/{selected_country}.png", use_column_width=True)
        # Add any data/info here
        st.write("Here you can display stats, charts, or text info for the selected country.")
        st.button("Close")
