# 1️⃣ Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from streamlit_plotly_events import plotly_events

# 2️⃣ Load datasets
hex_df = pd.read_csv("HEX.csv")  # Columns: Country, iso_alpha, hex
with open("countries.geo.json") as f:
    geojson = json.load(f)

# 3️⃣ Add a numeric column for color (for testing)
hex_df['TestValue'] = range(len(hex_df))

# 4️⃣ Remove rows with missing data
hex_df = hex_df.dropna(subset=['iso_alpha', 'TestValue'])

# 5️⃣ Dummy line chart data for testing
line_data = pd.DataFrame({
    "Country": ["Afghanistan"]*5 + ["Albania"]*5,
    "Year": [2018,2019,2020,2021,2022]*2,
    "GDP": [500,520,540,560,580, 4000,4100,4200,4300,4400],
    "HDI": [0.5,0.51,0.52,0.53,0.54, 0.7,0.71,0.72,0.73,0.74]
})

# 6️⃣ Create choropleth map for testing
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='TestValue',  # numeric column
    hover_name='Country',
    hover_data=['iso_alpha']
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.header("Interactive Map Test")
st.write("Click on a country to see popup with metrics and line charts:")

# 7️⃣ Capture click events
selected_points = plotly_events(fig, click_event=True)
st.plotly_chart(fig, use_container_width=True)

# 8️⃣ Show popup modal if a country is clicked
if selected_points:
    country_iso = selected_points[0]['location']
    country_name = hex_df.loc[hex_df['iso_alpha']==country_iso, 'Country'].values[0]

    with st.modal(f"{country_name} Details", key=country_iso):
        st.subheader(f"{country_name} Indicators (Testing)")

        # Example metrics
        st.metric("GDP", "12345")
        st.metric("HDI", "0.72")
        st.metric("Gini Index", "35")

        # Line chart for trends
        country_data = line_data[line_data['Country']==country_name]
        if not country_data.empty:
            fig_line = px.line(country_data, x='Year', y=['GDP','HDI'], markers=True,
                               title=f"{country_name} Trends")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.write("No trend data available for this country.")

        # Optional tabs inside modal
        tab1, tab2 = st.tabs(["Overview", "Trends"])
        with tab1:
            st.write("Latest Year Data:")
            st.write(country_data.tail(1))
        with tab2:
            if not country_data.empty:
                st.plotly_chart(fig_line, use_container_width=True)
