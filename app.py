# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="World Map — Country Details", layout="wide")

# 1️⃣ Load datasets
socio_df = pd.read_csv("final_with_socio_cleaned.csv")
hex_df = pd.read_csv("Hex.csv")
with open("countries.geo.json") as f:
    geojson = json.load(f)

# 2️⃣ Merge HEX colors with main data
hex_map = dict(zip(hex_df['iso_alpha'], hex_df['hex']))

# 3️⃣ Streamlit title and instructions
st.title("World Map — Click a country to open details")
st.markdown("""
**Controls**  
Hover shows preview. Click a country to open a popup with time-series and details.  
Tip: Hover on countries for quick preview. Click to open detailed popup.
""")

# 4️⃣ Plot the world map
fig = px.choropleth(
    socio_df,
    geojson=geojson,
    locations="ISO3",
    color="ISO3",
    color_discrete_map=hex_map,
    hover_name="Country",
    hover_data={
        "GDP_per_capita": True,
        "HDI": True,
        "Life_Expectancy": True,
        "Gini_Index": True,
        "PM25": True,
        "Health_Insurance": True,
        "Median_Age_Est": True,
        "Median_Age_Mid": True,
        "COVID_Deaths": True,
        "COVID_Cases": True,
        "Total_Population": True
    },
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    clickmode="event+select"
)

# 5️⃣ Show the map
selected = st.plotly_chart(fig, use_container_width=True)

# 6️⃣ Capture click event
clicked_country = st.session_state.get("clicked_country", None)

if "clicked_country" not in st.session_state:
    st.session_state.clicked_country = None

clicked = st.plotly_chart(fig, use_container_width=True)

# Streamlit cannot directly catch Plotly click in a variable without callbacks,
# so we use a workaround using Plotly's 'selectedpoints' or user manual select.
# For simplicity, provide a selectbox to mimic click popup:
country_list = socio_df['Country'].unique()
selected_country_name = st.selectbox("Select a country to see details:", [""] + list(country_list))

if selected_country_name:
    country_data = socio_df[socio_df['Country'] == selected_country_name].iloc[0]
    st.markdown("### Country Details")
    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown(f"**Map Preview for {selected_country_name}**")
        mini_fig = px.choropleth(
            pd.DataFrame([country_data]),
            geojson=geojson,
            locations=["ISO3"],
            color=["ISO3"],
            color_discrete_map=hex_map,
        )
        mini_fig.update_geos(fitbounds="locations", visible=False)
        mini_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=300)
        st.plotly_chart(mini_fig, use_container_width=True)
    with col2:
        st.markdown("**Metrics**")
        st.write({
            "GDP per Capita": country_data['GDP_per_capita'],
            "HDI": country_data['HDI'],
            "Life Expectancy": country_data['Life_Expectancy'],
            "Gini Index": country_data['Gini_Index'],
            "PM2.5 Air Pollution": country_data['PM25'],
            "Health Insurance Coverage": country_data['Health_Insurance'],
            "Median Age Estimate": country_data['Median_Age_Est'],
            "Median Age Mid": country_data['Median_Age_Mid'],
            "COVID Deaths": country_data['COVID_Deaths'],
            "COVID Cases": country_data['COVID_Cases'],
            "Population": country_data['Total_Population']
        })
