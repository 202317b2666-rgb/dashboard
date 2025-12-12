# 1️⃣ Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import json

# 2️⃣ Load datasets
hex_df = pd.read_csv("HEX.csv")  # Columns: Country, iso_alpha, hex
with open("countries.geo.json") as f:
    geojson = json.load(f)

# Example line chart data
# Replace this with your real dataset
line_data = pd.DataFrame({
    "Country": ["Afghanistan"]*5 + ["Albania"]*5,
    "Year": [2018,2019,2020,2021,2022]*2,
    "GDP": [500,520,540,560,580, 4000,4100,4200,4300,4400],
    "HDI": [0.5,0.51,0.52,0.53,0.54, 0.7,0.71,0.72,0.73,0.74]
})

# 3️⃣ Create choropleth map
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='hex',  # just to give some color
    hover_name='Country',
    hover_data=['iso_alpha']
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)

# 4️⃣ Capture click
st.write("Click on a country to see detailed popup.")

click_data = st.session_state.get('click_data', None)
# Use plotly_events if you want real-time click capture
from streamlit_plotly_events import plotly_events

selected_points = plotly_events(fig, click_event=True)
if selected_points:
    country_iso = selected_points[0]['location']
    country_name = hex_df.loc[hex_df['iso_alpha']==country_iso, 'Country'].values[0]

    # 5️⃣ Show big modal with indicators + line charts
    with st.modal(f"{country_name} Details", key=country_iso):
        st.subheader(f"{country_name} Indicators")
        st.write("Current Year Indicators:")
        
        # Example indicators
        st.metric("GDP", "12345")
        st.metric("HDI", "0.72")
        st.metric("Gini Index", "35")

        # Line chart for trends
        country_data = line_data[line_data['Country']==country_name]
        fig_line = px.line(country_data, x='Year', y=['GDP','HDI'], markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

        # Optional: More tabs for extra indicators
        tab1, tab2 = st.tabs(["Overview", "Trends"])
        with tab1:
            st.write(country_data.tail(1))  # Latest values
        with tab2:
            st.plotly_chart(fig_line, use_container_width=True)
