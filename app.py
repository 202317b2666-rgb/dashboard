# app.py
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Global Health & Socio-Economic Dashboard", layout="wide")

st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.markdown("Click on a country in the map to see detailed indicators over time.")

# -----------------------------
# 1️⃣ Load Data
# -----------------------------
hex_df = pd.read_csv("Hex.csv")

with open("countries.geo.json") as f:
    geojson = json.load(f)

# Ensure consistent ISO codes
hex_df['ISO3'] = hex_df['ISO3'].str.upper().str.strip()

# -----------------------------
# 2️⃣ Choropleth Map
# -----------------------------
# We'll use a dummy 'Value' column for color
hex_df['Value'] = 1  

fig_map = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='ISO3',          # Column in CSV
    color='Value',
    hover_name='Country',
    hover_data=['ISO3'],
    color_continuous_scale="Viridis",
    featureidkey="id"          # matches GeoJSON 'id' field
)

fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

selected = st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------
# 3️⃣ Country selection for popup
# -----------------------------
country_list = hex_df['Country'].sort_values().unique()
selected_country = st.selectbox("Or select a country:", country_list)

country_data = hex_df[hex_df['Country'] == selected_country].sort_values('Year')

# -----------------------------
# 4️⃣ Line Charts for indicators
# -----------------------------
st.subheader(f"📊 {selected_country} Indicators Over Time")

cols = st.columns(2)

with cols[0]:
    fig_gdp = px.line(country_data, x='Year', y='GDP_per_capita', markers=True, title="GDP per Capita")
    st.plotly_chart(fig_gdp, use_container_width=True)

with cols[1]:
    fig_hdi = px.line(country_data, x='Year', y='HDI', markers=True, title="HDI")
    st.plotly_chart(fig_hdi, use_container_width=True)

cols2 = st.columns(2)

with cols2[0]:
    fig_life = px.line(country_data, x='Year', y='Life_Expectancy', markers=True, title="Life Expectancy")
    st.plotly_chart(fig_life, use_container_width=True)

with cols2[1]:
    fig_gini = px.line(country_data, x='Year', y='Gini_Index', markers=True, title="Gini Index")
    st.plotly_chart(fig_gini, use_container_width=True)

st.subheader("Other Indicators")
other_cols = st.columns(3)

with other_cols[0]:
    fig_pm25 = px.line(country_data, x='Year', y='PM25', markers=True, title="Air Pollution PM2.5")
    st.plotly_chart(fig_pm25, use_container_width=True)

with other_cols[1]:
    fig_health = px.line(country_data, x='Year', y='Health_Insurance', markers=True, title="Health Insurance Share")
    st.plotly_chart(fig_health, use_container_width=True)

with other_cols[2]:
    fig_age = px.line(country_data, x='Year', y='Median_Age_Est', markers=True, title="Median Age")
    st.plotly_chart(fig_age, use_container_width=True)
