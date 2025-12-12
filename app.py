import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Interactive Global Health & Socio-Economic Dashboard", layout="wide")

st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click on a country in the map to see detailed indicators over time.")

# -------------------------
# Load HEX CSV
# -------------------------
hex_df = pd.read_csv("HEX.csv")

# Clean column names (strip spaces, hidden characters)
hex_df.columns = hex_df.columns.str.strip().str.replace('\u200b','')

# Ensure ISO3 codes are uppercase
hex_df['ISO3'] = hex_df['ISO3'].str.upper().str.strip()

# -------------------------
# Load GeoJSON
# -------------------------
with open("countries.geo.json") as f:
    geojson = json.load(f)

# -------------------------
# Map
# -------------------------
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='ISO3',           # column in HEX.csv
    color='HDI',                # default color
    hover_name='Country',
    hover_data=['GDP_per_capita','Gini_Index','Life_Expectancy','PM25','Health_Insurance','Median_Age_Est','COVID_Deaths','COVID_Cases'],
    featureidkey="id",
    color_continuous_scale="Viridis"
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})

# -------------------------
# Clickable map in Streamlit
# -------------------------
click = st.plotly_chart(fig, use_container_width=True)

# Use st.plotly_events to get click event
from streamlit_plotly_events import plotly_events

selected_country_iso = plotly_events(fig, click_event=True, hover_event=False)

if selected_country_iso:
    iso = selected_country_iso[0]['location']  # get ISO3 from clicked country
    country_data = hex_df[hex_df['ISO3'] == iso].sort_values(by='Year')
    country_name = country_data['Country'].values[0]

    st.subheader(f"📊 {country_name} - Indicators over time")

    indicators = ['GDP_per_capita','Gini_Index','Life_Expectancy','PM25','Health_Insurance','Median_Age_Est','COVID_Deaths','COVID_Cases']

    for ind in indicators:
        fig_line = px.line(
            country_data,
            x='Year',
            y=ind,
            title=f"{ind} over time",
            markers=True
        )
        st.plotly_chart(fig_line, use_container_width=True)
else:
    st.info("Click on a country in the map to see its indicators below.")
