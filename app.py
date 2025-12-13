# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Interactive World Map - Click to show floating popup")

# ----------------------------
# Sample country data
# ----------------------------
map_df = pd.DataFrame({
    "lat": [21, 37, 35],
    "lon": [78, -95, 103],
    "country": ["India", "USA", "China"]
})

# ----------------------------
# Plot world map
# ----------------------------
fig = px.scatter_geo(
    map_df,
    lat="lat",
    lon="lon",
    hover_name="country",
    projection="natural earth",
    title="World Overview Map"
)
st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Simulate click for now (can replace with actual map click later)
# ----------------------------
country_selected = st.selectbox("Select country (simulate click)", map_df["country"])

# ----------------------------
# Show floating popup using HTML/CSS
# ----------------------------
if st.button(f"Show Popup for {country_selected}"):
    popup_html = f"""
    <div id="popup" style="
        position:fixed;
        top:50%;
        left:50%;
        transform:translate(-50%, -50%);
        width:500px;
        height:400px;
        background-color:white;
        border:2px solid #000;
        box-shadow:0 4px 20px rgba(0,0,0,0.3);
        z-index:999;
        padding:20px;
    ">
        <h2>{country_selected} Details</h2>
        <p>This is a floating popup window!</p>
        <p>You can later add charts and indicators here.</p>
        <button onclick="document.getElementById('popup').style.display='none'" 
                style="margin-top:20px;padding:5px 10px;">Close</button>
    </div>
    """
    st.components.v1.html(popup_html, height=0)
