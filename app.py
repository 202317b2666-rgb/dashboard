import streamlit as st
import pandas as pd
import plotly.express as px
import json
import base64

st.set_page_config(layout="wide")
st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click on a country in the map to see detailed indicators over time.")

# Load map HEX data
hex_df = pd.read_csv("Hex.csv")
hex_df.columns = hex_df.columns.str.strip()
hex_df['iso_alpha'] = hex_df['iso_alpha'].str.upper().str.strip()

with open("countries.geo.json") as f:
    geojson = json.load(f)

# Load socio-economic dataset
socio_df = pd.read_csv("final_with_socio_cleaned.csv")
socio_df.columns = socio_df.columns.str.strip()
socio_df['ISO3'] = socio_df['ISO3'].str.upper().str.strip()

# Create choropleth map
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='hex',  # dummy color
    hover_name='country',
    featureidkey="id",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Display map
map_plot = st.plotly_chart(fig, use_container_width=True)

# Capture click
click_data = st.session_state.get("click_data", None)
if st.session_state.get("map_clicked", False):
    click_data = st.session_state["click_data"]

# Use Streamlit events
clicked_country = None
click_event = st.plotly_chart(fig, use_container_width=True)
if click_event:
    try:
        clicked_country = click_event["points"][0]["hovertext"]
        st.session_state["map_clicked"] = True
        st.session_state["click_data"] = click_event
    except:
        clicked_country = None

# Modal function
def show_modal(df, country_name):
    if df.empty:
        st.warning(f"No data available for {country_name}")
        return
    
    st.markdown(
        f"""
        <style>
        /* Blurred background */
        .modal-bg {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            backdrop-filter: blur(5px);
            background-color: rgba(0,0,0,0.3);
            z-index: 999;
        }}
        /* Modal box */
        .modal-box {{
            position: fixed;
            top: 10%; left: 10%;
            width: 80%; height: 80%;
            background-color: white;
            z-index: 1000;
            padding: 20px;
            border-radius: 10px;
            overflow-y: scroll;
        }}
        </style>
        <div class="modal-bg"></div>
        <div class="modal-box">
        <h2>{country_name} - Detailed Indicators</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# Show modal if country clicked
if clicked_country:
    country_code = hex_df[hex_df["country"] == clicked_country]["iso_alpha"].values[0]
    country_data = socio_df[socio_df["ISO3"] == country_code]
    show_modal(country_data, clicked_country)
    
    # Render charts inside modal
    st.plotly_chart(px.line(country_data, x="Year", y="GDP_per_capita", title="GDP per Capita"))
    st.plotly_chart(px.line(country_data, x="Year", y="HDI", title="HDI"))
    st.plotly_chart(px.line(country_data, x="Year", y="Life_Expectancy", title="Life Expectancy"))
    st.plotly_chart(px.line(country_data, x="Year", y="Gini_Index", title="Gini Index"))
    st.plotly_chart(px.line(country_data, x="Year", y="PM25", title="Air Pollution PM2.5"))
    st.plotly_chart(px.line(country_data, x="Year", y="Health_Insurance", title="Health Insurance Coverage"))
