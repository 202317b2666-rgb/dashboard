# app.py
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

# --- 1️⃣ Load HEX color data ---
hex_df = pd.read_csv("Hex.csv")  # columns: country, iso_alpha, hex

# --- 2️⃣ Load GeoJSON data ---
with open("countries.geo.json") as f:
    geojson = json.load(f)

# --- 3️⃣ Initialize session state for selected country ---
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# --- 4️⃣ Function to create figure ---
def create_fig(selected=None):
    fig = px.choropleth(
        hex_df,
        geojson=geojson,
        locations='iso_alpha',
        color='hex',
        color_discrete_map="identity",
        hover_name='country',
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_traces(marker_line_width=0.5, marker_line_color="white")

    # Highlight selected country
    if selected:
        for i, iso in enumerate(hex_df['iso_alpha']):
            if iso == selected:
                fig.data[0].marker.line.width = [3 if x == i else 0.5 for x in range(len(hex_df))]
                fig.data[0].marker.line.color = ["black" if x == i else "white" for x in range(len(hex_df))]
    
    return fig

# --- 5️⃣ Streamlit UI ---
st.title("Interactive World Map")
st.write("Click a country to highlight it!")

# Display the map
fig = create_fig(st.session_state.selected_country)
chart = st.plotly_chart(fig, use_container_width=True)

# --- 6️⃣ Handle click ---
clicked = st.session_state.get("clicked_country")
st.write("Selected country:", st.session_state.selected_country)

# Note: Streamlit cannot natively detect Plotly click events directly.
# Workaround: Use a selectbox or dropdown for now:
country_list = [""] + list(hex_df['country'])
selected = st.selectbox("Select a country to highlight (for demo click effect):", country_list)

if selected:
    iso_selected = hex_df[hex_df['country'] == selected]['iso_alpha'].values[0]
    st.session_state.selected_country = iso_selected
    st.experimental_rerun()
