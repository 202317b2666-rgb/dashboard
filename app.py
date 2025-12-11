# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import json

# ------------------------------
# Load data
# ------------------------------
data = pd.read_csv("final_with_socio_cleaned.csv")
hex_colors = pd.read_csv("Hex.csv")
with open("countries.geo.json") as f:
    geojson = json.load(f)

# Merge HEX colors into main data (latest year per country)
latest_data = data.groupby('ISO3').apply(lambda x: x.sort_values('Year', ascending=False).iloc[0])
latest_data = latest_data.reset_index(drop=True)
latest_data = latest_data.merge(hex_colors[['iso_alpha', 'hex']], left_on='ISO3', right_on='iso_alpha', how='left')

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="World Map Dashboard", layout="wide")
st.title("🌍 World Map — Click a country to open details")
st.write("Hover over countries for quick preview. Click a country to open detailed popup.")

# ------------------------------
# Plotly choropleth map
# ------------------------------
fig = px.choropleth(
    latest_data,
    locations="ISO3",
    color="HDI",
    hover_name="Country",
    hover_data={
        "GDP_per_capita": True,
        "Life_Expectancy": True,
        "HDI": True,
        "ISO3": False,
        "hex": False
    },
    color_continuous_scale="Viridis",
    geojson=geojson,
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})

# ------------------------------
# Click handling
# ------------------------------
st.write("Click on a country in the map below to open the detailed view:")
clicked = st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Country selection (simulate click)
# ------------------------------
country_selected = st.selectbox(
    "Select country for popup",
    [""] + sorted(data['ISO3'].unique())
)

if country_selected:
    country_data = data[data['ISO3'] == country_selected]
    country_color = hex_colors[hex_colors['iso_alpha'] == country_selected]['hex'].values[0]
    country_name = country_data['Country'].iloc[0]

    # Modal simulation
    with st.expander(f"Details for {country_name}", expanded=True):
        st.markdown(
            f"<div style='background-color: rgba(0,0,0,0.85); padding:20px; border-radius:10px;'>",
            unsafe_allow_html=True
        )

        # Two-column layout inside modal
        col1, col2 = st.columns([1, 2])

        with col1:
            # Mini-map for the country
            fig_map = px.choropleth(
                country_data,
                locations="ISO3",
                color="HDI",
                geojson=geojson,
                hover_name="Country",
                color_continuous_scale="Viridis"
            )
            fig_map.update_geos(fitbounds="locations", visible=False)
            fig_map.update_layout(height=400, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

        with col2:
            # Year slider
            min_year = int(country_data['Year'].min())
            max_year = int(country_data['Year'].max())
            year_selected = st.slider(
                "Select Year",
                min_year,
                max_year,
                min_year
            )

            # Filter for selected year
            year_data = country_data[country_data['Year'] == year_selected]

            # Line charts for key metrics
            metrics = ['GDP_per_capita', 'Life_Expectancy', 'HDI', 'PM25', 'Health_Insurance', 'Median_Age_Est', 'Median_Age_Mid', 'COVID_Deaths', 'COVID_Cases', 'Population_Density']
            for metric in metrics:
                if metric in year_data.columns:
                    st.line_chart(country_data.set_index('Year')[metric])

        st.markdown("</div>", unsafe_allow_html=True)
