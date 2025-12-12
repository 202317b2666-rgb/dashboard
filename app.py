# app.py
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------
# 1️⃣ Load CSV and GeoJSON
# -------------------------------
hex_df = pd.read_csv("Hex.csv")

# Rename ISO column to match code
hex_df = hex_df.rename(columns={'ISO3': 'iso_alpha'})

# Clean ISO codes
hex_df['iso_alpha'] = hex_df['iso_alpha'].str.strip().str.upper()

# Load GeoJSON
with open("countries.geo.json") as f:
    geojson = json.load(f)

# Filter CSV for only countries present in GeoJSON
geo_ids = [feature['id'] for feature in geojson['features']]
hex_df = hex_df[hex_df['iso_alpha'].isin(geo_ids)]

# -------------------------------
# 2️⃣ Streamlit UI
# -------------------------------
st.set_page_config(layout="wide")
st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click on a country to see detailed indicators over time.")

# -------------------------------
# 3️⃣ Choropleth Map
# -------------------------------
hex_df['Value'] = 1  # dummy value for coloring

fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='Value',
    hover_name='Country',
    featureidkey="id",
    color_continuous_scale="Viridis"
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

selected = st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 4️⃣ Country Selection
# -------------------------------
country_list = hex_df['Country'].sort_values().tolist()
selected_country = st.selectbox("Or select a country from the list:", country_list)

country_data = hex_df[hex_df['Country'] == selected_country]

if not country_data.empty:
    st.subheader(f"📊 Indicators for {selected_country}")

    # -------------------------------
    # Line charts for multiple indicators
    # -------------------------------
    indicators = [
        'GDP_per_capita', 'Gini_Index', 'Life_Expectancy',
        'PM25', 'Health_Insurance', 'Median_Age_Est',
        'COVID_Deaths', 'COVID_Cases', 'Population_Density', 'HDI'
    ]

    for ind in indicators:
        if ind in country_data.columns:
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=country_data['Year'],
                y=country_data[ind],
                mode='lines+markers',
                name=ind
            ))
            fig_line.update_layout(
                title=ind,
                xaxis_title="Year",
                yaxis_title=ind,
                height=300,
                margin={"r":10,"t":30,"l":10,"b":10}
            )
            st.plotly_chart(fig_line, use_container_width=True)
