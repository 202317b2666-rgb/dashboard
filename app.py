import pandas as pd
import streamlit as st
import plotly.express as px
import json

st.set_page_config(layout="wide")
st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click on a country in the map to see detailed indicators over time.")

# --------------------------
# Load HEX map data
# --------------------------
hex_df = pd.read_csv("HEX.csv")
hex_df.columns = hex_df.columns.str.strip()
hex_df['iso_alpha'] = hex_df['iso_alpha'].str.upper().str.strip()

with open("countries.geo.json") as f:
    geojson = json.load(f)

# --------------------------
# Load socio-economic dataset
# --------------------------
socio_df = pd.read_csv("final_socio_cleaned.csv")
socio_df.columns = socio_df.columns.str.strip()
socio_df['ISO3'] = socio_df['ISO3'].str.upper().str.strip()

# --------------------------
# Map
# --------------------------
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='hex',  # dummy color for map
    hover_name='country',
    featureidkey="id",
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Plot map
map_plot = st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Country selection
# --------------------------
country_clicked = st.selectbox(
    "Or select a country to view indicators:",
    options=hex_df['country'].sort_values()
)

# Filter data for selected country
country_code = hex_df[hex_df['country'] == country_clicked]['iso_alpha'].values[0]
country_data = socio_df[socio_df['ISO3'] == country_code]

if country_data.empty:
    st.warning(f"No socio-economic data found for {country_clicked}")
else:
    st.subheader(f"📊 Indicators for {country_clicked}")

    # Example line charts for GDP, HDI, Life Expectancy
    col1, col2 = st.columns(2)

    with col1:
        fig_gdp = px.line(country_data, x='Year', y='GDP_per_capita', title='GDP per Capita')
        st.plotly_chart(fig_gdp, use_container_width=True)

        fig_hdi = px.line(country_data, x='Year', y='HDI', title='Human Development Index')
        st.plotly_chart(fig_hdi, use_container_width=True)

    with col2:
        fig_life = px.line(country_data, x='Year', y='Life_Expectancy', title='Life Expectancy')
        st.plotly_chart(fig_life, use_container_width=True)

        fig_gini = px.line(country_data, x='Year', y='Gini_Index', title='Gini Index')
        st.plotly_chart(fig_gini, use_container_width=True)
