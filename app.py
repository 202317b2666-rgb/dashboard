# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Interactive World Map Dashboard")

# ----------------------------
# Sample country data
# ----------------------------
countries = ["India", "USA", "China"]
indicators = {
    "India": {"Population": "1.4B", "GDP": "$3T", "Life Expectancy": 70},
    "USA": {"Population": "331M", "GDP": "$25T", "Life Expectancy": 78},
    "China": {"Population": "1.4B", "GDP": "$17T", "Life Expectancy": 76},
}

# Sample GDP data for line chart
gdp_data = {
    "India": [2.5, 2.7, 2.6, 3.0, 3.2],
    "USA": [21, 22, 20, 23, 24],
    "China": [13, 14, 14.5, 15, 16]
}

# ----------------------------
# Country selection
# ----------------------------
country_selected = st.selectbox("Select Country", countries)

# ----------------------------
# Show modal popup
# ----------------------------
if st.button(f"Show {country_selected} Details"):
    with st.modal(f"{country_selected} Details"):
        st.subheader(f"{country_selected} Indicators")

        # Display indicators
        for key, value in indicators[country_selected].items():
            st.write(f"**{key}:** {value}")

        # Display line chart for GDP trend
        df = pd.DataFrame({
            "Year": [2018, 2019, 2020, 2021, 2022],
            "GDP (Trillions USD)": gdp_data[country_selected]
        })
        fig = px.line(df, x="Year", y="GDP (Trillions USD)", 
                      title=f"{country_selected} GDP Trend", markers=True)
        st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Display a simple world map (optional)
# ----------------------------
st.subheader("World Overview Map")
map_df = pd.DataFrame({
    "lat": [21, 37, 35],
    "lon": [78, -95, 103],
    "country": countries
})
fig_map = px.scatter_geo(map_df, lat="lat", lon="lon", hover_name="country",
                         projection="natural earth")
st.plotly_chart(fig_map, use_container_width=True)
