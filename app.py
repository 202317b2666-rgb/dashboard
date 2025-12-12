import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide")
st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click on a country in the map to see detailed indicators over time.")

# Load HEX map data
hex_df = pd.read_csv("Hex.csv")
hex_df.columns = hex_df.columns.str.strip()
hex_df['iso_alpha'] = hex_df['iso_alpha'].str.upper().str.strip()

# Load GeoJSON
with open("countries.geo.json") as f:
    geojson = json.load(f)

# Load socio-economic data
socio_df = pd.read_csv("final_with_socio_cleaned.csv")
socio_df.columns = socio_df.columns.str.strip()
socio_df['ISO3'] = socio_df['ISO3'].str.upper().str.strip()

# Choropleth map
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='hex',
    hover_name='country',
    featureidkey="id",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Render the map (single instance)
map_plot = st.plotly_chart(fig, use_container_width=True, key="world_map")

# Capture click
click_data = st.session_state.get("click_data", None)
if st.session_state.get("map_clicked", False):
    click_data = st.session_state["click_data"]

clicked_country = None
if map_plot:
    if st.session_state.get("map_clicked", False):
        clicked_country = st.session_state["click_data"]["points"][0]["hovertext"]  
    else:
        click_event = st.plotly_chart(fig, use_container_width=True, key="world_map_click")
        if click_event:
            try:
                clicked_country = click_event["points"][0]["hovertext"]
                st.session_state["map_clicked"] = True
                st.session_state["click_data"] = click_event
            except:
                clicked_country = None

# Modal display
def show_modal(df, country_name):
    if df.empty:
        st.warning(f"No data available for {country_name}")
        return

    st.markdown(
        f"""
        <style>
        .modal-bg {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            backdrop-filter: blur(5px);
            background-color: rgba(0,0,0,0.3);
            z-index: 999;
        }}
        .modal-box {{
            position: fixed;
            top: 5%; left: 5%;
            width: 90%; height: 90%;
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

# Show modal with charts if a country is clicked
if clicked_country:
    country_code = hex_df[hex_df["country"] == clicked_country]["iso_alpha"].values[0]
    country_data = socio_df[socio_df["ISO3"] == country_code]
    show_modal(country_data, clicked_country)
    
    st.plotly_chart(px.line(country_data, x="Year", y="GDP_per_capita", title="GDP per Capita"), key="GDP")
    st.plotly_chart(px.line(country_data, x="Year", y="HDI", title="HDI"), key="HDI")
    st.plotly_chart(px.line(country_data, x="Year", y="Life_Expectancy", title="Life Expectancy"), key="LifeExp")
    st.plotly_chart(px.line(country_data, x="Year", y="Gini_Index", title="Gini Index"), key="Gini")
    st.plotly_chart(px.line(country_data, x="Year", y="PM25", title="Air Pollution PM2.5"), key="PM25")
    st.plotly_chart(px.line(country_data, x="Year", y="Health_Insurance", title="Health Insurance Coverage"), key="Health")
