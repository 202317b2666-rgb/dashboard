# 1️⃣ Import libraries
import streamlit as st
import pandas as pd
import json
import plotly.express as px
from streamlit_plotly_events import plotly_events

# 2️⃣ Load datasets
hex_df = pd.read_csv("HEX.csv")  # Columns: Country, iso_alpha, hex
with open("countries.geo.json") as f:
    geojson = json.load(f)

# 3️⃣ Clean hex_df
hex_df = hex_df.dropna(subset=['iso_alpha'])
hex_df['iso_alpha'] = hex_df['iso_alpha'].astype(str).str.strip()
hex_df['TestValue'] = range(len(hex_df))  # Dummy numeric column for coloring

# Filter only valid countries present in geojson
geo_ids = [feature['id'] for feature in geojson['features']]
hex_df = hex_df[hex_df['iso_alpha'].isin(geo_ids)]

# 4️⃣ Dummy line chart data
line_data = pd.DataFrame({
    "Country": ["Afghanistan"]*5 + ["Albania"]*5,
    "Year": [2018,2019,2020,2021,2022]*2,
    "GDP": [500,520,540,560,580, 4000,4100,4200,4300,4400],
    "HDI": [0.5,0.51,0.52,0.53,0.54, 0.7,0.71,0.72,0.73,0.74]
})

# 5️⃣ Create choropleth map
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='TestValue',
    hover_name='Country',
    hover_data=['iso_alpha'],
    featureidkey="id"  # Ensures ISO-3 codes match GeoJSON
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# 6️⃣ Streamlit UI
st.title("Interactive World Map with Country Details")
st.write("Click on a country to see metrics and trend line charts:")

# 7️⃣ Capture clicks
selected_points = plotly_events(fig, click_event=True)
st.plotly_chart(fig, use_container_width=True)

# 8️⃣ Show popup for selected country
if selected_points:
    country_iso = selected_points[0]['location']
    country_name = hex_df.loc[hex_df['iso_alpha']==country_iso, 'Country'].values[0]

    with st.expander(f"{country_name} - Indicators & Trends", expanded=True):
        st.subheader(f"{country_name} Metrics")
        
        # Example metrics (replace with your real indicators)
        st.metric("GDP per Capita", "$12,345")
        st.metric("Human Development Index (HDI)", "0.72")
        st.metric("Gini Index", "35")
        st.metric("Life Expectancy", "72.5")
        st.metric("Median Age", "31.2")
        
        # Line chart for trends
        country_data = line_data[line_data['Country']==country_name]
        if not country_data.empty:
            fig_line = px.line(
                country_data,
                x='Year',
                y=['GDP','HDI'],
                markers=True,
                title=f"{country_name} Trends Over Years"
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.write("No trend data available for this country.")
