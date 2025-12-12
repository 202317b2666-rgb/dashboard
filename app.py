# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Global Health & Socio-Economic Dashboard", layout="wide")

st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click on a country in the map to see detailed indicators over time.")

# 1️⃣ Load CSV data
hex_df = pd.read_csv("Hex.csv")
hex_df.columns = hex_df.columns.str.strip()  # Fix KeyError by stripping spaces
hex_df['ISO3'] = hex_df['ISO3'].str.upper().str.strip()  # Ensure uppercase ISO codes

# 2️⃣ Load GeoJSON
with open("countries.geo.json") as f:
    geojson = json.load(f)

# 3️⃣ Choropleth map
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations="ISO3",
    featureidkey="properties.iso_a3",  # Adjust depending on your geojson id path
    color="HDI",
    hover_name="Country",
    hover_data=["GDP_per_capita", "Gini_Index", "Life_Expectancy"],
    color_continuous_scale="Viridis",
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})

selected_country = st.plotly_chart(fig, use_container_width=True)

# 4️⃣ Country-specific indicators
st.markdown("---")
st.subheader("Country Indicators Over Time")

# Dropdown to select country
country_list = hex_df['Country'].sort_values().unique()
selected_country_name = st.selectbox("Select Country:", country_list)

# Filter data for selected country
country_data = hex_df[hex_df['Country'] == selected_country_name]

# Display line charts for multiple indicators
if not country_data.empty:
    st.write(f"### {selected_country_name} Indicators Over Time")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.line(
            country_data,
            x="Year",
            y="GDP_per_capita",
            title="GDP per Capita Over Time"
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = px.line(
            country_data,
            x="Year",
            y="Life_Expectancy",
            title="Life Expectancy Over Time"
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    with col2:
        fig3 = px.line(
            country_data,
            x="Year",
            y="Gini_Index",
            title="Gini Index Over Time"
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        fig4 = px.line(
            country_data,
            x="Year",
            y="PM25",
            title="Air Pollution PM2.5 Over Time"
        )
        st.plotly_chart(fig4, use_container_width=True)
else:
    st.write("No data available for this country.")
