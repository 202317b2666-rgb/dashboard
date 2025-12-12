# 1️⃣ Import libraries
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

# 2️⃣ Load datasets
hex_df = pd.read_csv("Hex.csv")  # your main data
with open("countries.geo.json") as f:
    geojson = json.load(f)

# 3️⃣ Data cleaning
hex_df = hex_df.dropna(subset=['iso_alpha'])
hex_df['iso_alpha'] = hex_df['iso_alpha'].astype(str).str.strip()
hex_df = hex_df.drop_duplicates(subset=['iso_alpha'])

# Optional: create a numeric column for choropleth coloring
hex_df['Value'] = range(len(hex_df))

# Filter only countries present in GeoJSON
geo_ids = [feature['id'] for feature in geojson['features']]
hex_df = hex_df[hex_df['iso_alpha'].isin(geo_ids)]

# 4️⃣ Streamlit UI
st.title("Interactive Global Map Dashboard")
st.write("Click on a country to see its indicators.")

# 5️⃣ Choropleth map
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='Value',
    hover_name='Country',
    featureidkey="id",  # matches GeoJSON
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# 6️⃣ Display map
selected_country = st.plotly_chart(fig, use_container_width=True)

# 7️⃣ Country selection
country_list = hex_df['Country'].tolist()
selected = st.selectbox("Or select a country from dropdown:", country_list)

if selected:
    st.subheader(f"Indicators for {selected}")

    # Example line chart (replace with your real metrics)
    country_data = hex_df[hex_df['Country'] == selected]
    metrics = ['Value']  # Add your actual metric columns here

    for metric in metrics:
        st.line_chart(country_data[metric])
