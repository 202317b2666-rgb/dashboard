# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

st.set_page_config(page_title="Global Health & Socio-Economic Dashboard", layout="wide")

st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.markdown("Click on a country in the map to see detailed indicators over time.")

# 1️⃣ Load HEX data
hex_df = pd.read_csv("Hex.csv")
hex_df.columns = hex_df.columns.str.strip()  # Remove extra spaces
hex_df['ISO3'] = hex_df['ISO3'].str.upper().str.strip()  # Ensure uppercase ISO codes

# 2️⃣ Load GeoJSON
with open("countries.geo.json") as f:
    geojson = json.load(f)

# 3️⃣ Choropleth Map
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations="ISO3",             # ISO alpha-3 codes
    color="HDI",                  # Color by HDI initially
    hover_name="Country",
    hover_data=["Year", "GDP_per_capita", "Gini_Index", "Life_Expectancy", "PM25", "Health_Insurance"],
    color_continuous_scale="Viridis",
    featureidkey="properties.id"  # Match the GeoJSON 'id' property
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})

# 4️⃣ Streamlit map
selected_country = st.plotly_chart(fig, use_container_width=True)

# 5️⃣ Sidebar for country selection (optional)
country_list = hex_df['Country'].sort_values().unique()
selected_country_name = st.sidebar.selectbox("Or select a country:", country_list)

# 6️⃣ Filter data for the selected country
country_data = hex_df[hex_df['Country'] == selected_country_name].sort_values('Year')

# 7️⃣ Line charts for indicators
st.subheader(f"📊 Indicators over time: {selected_country_name}")

indicators = ["GDP_per_capita", "Gini_Index", "Life_Expectancy", "PM25", "Health_Insurance", "Median_Age_Est"]

for indicator in indicators:
    fig_line = px.line(
        country_data,
        x="Year",
        y=indicator,
        markers=True,
        title=indicator.replace("_", " "),
        labels={indicator: indicator.replace("_", " "), "Year": "Year"}
    )
    st.plotly_chart(fig_line, use_container_width=True)
