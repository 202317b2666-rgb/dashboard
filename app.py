import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# Load data
df = pd.read_csv("final_with_socio_cleaned.csv")
hex_df = pd.read_csv("Hex.csv")
df = df.merge(hex_df[['iso_alpha','hex']], left_on='ISO3', right_on='iso_alpha', how='left')
with open("countries.geo.json") as f:
    geojson = json.load(f)

# Page layout
st.set_page_config(layout="wide")
st.title("🌍 World Map — Click a country to open details")
st.markdown("Hover on a country for preview. Click to open detailed popup.")

# Choropleth map
fig = px.choropleth(
    df,
    geojson=geojson,
    locations='ISO3',
    color='hex',
    color_discrete_map="identity",
    hover_name='Country',
    hover_data={'GDP_per_capita': True, 'Life_Expectancy': True}
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, clickmode='event+select')
st.plotly_chart(fig, use_container_width=True)

# ---------------- Popup Simulation ----------------
if "popup_country" not in st.session_state:
    st.session_state.popup_country = None

# Select country to simulate click (replace later with real click event)
country_iso = st.selectbox("Select country for popup", df['ISO3'].unique())
st.session_state.popup_country = country_iso

if st.session_state.popup_country:
    country_data = df[df['ISO3'] == st.session_state.popup_country]

    # Year slider
    min_year = int(country_data['Year'].min())
    max_year = int(country_data['Year'].max())
    year = st.slider("Select Year", min_value=min_year, max_value=max_year, value=max_year)

    # Popup box HTML
    st.markdown(f"""
    <style>
    .popup-container {{
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.5);
        backdrop-filter: blur(5px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }}
    .popup-box {{
        background: white;
        border-radius: 10px;
        width: 80%;
        max-width: 1000px;
        display: flex;
        padding: 20px;
    }}
    .popup-left {{ width: 40%; padding-right: 20px; }}
    .popup-right {{ width: 60%; }}
    </style>
    <div class="popup-container">
        <div class="popup-box">
            <div class="popup-left">MAP GOES HERE</div>
            <div class="popup-right">CHARTS GO HERE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Country map
    c_map = px.choropleth(
        country_data,
        geojson=geojson,
        locations='ISO3',
        color='hex',
        color_discrete_map="identity"
    )
    c_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(c_map, use_container_width=True)

    # Line charts
    attributes = ['GDP_per_capita','Gini_Index','Life_Expectancy','PM25','Health_Insurance','Median_Age_Est','COVID_Deaths','COVID_Cases']
    chart_fig = go.Figure()
    for attr in attributes:
        filtered = country_data[country_data['Year'] <= year]
        chart_fig.add_trace(go.Scatter(x=filtered['Year'], y=filtered[attr], mode='lines+markers', name=attr))
    chart_fig.update_layout(title=f"{country_data.iloc[0]['Country']} Metrics Over Time", xaxis_title="Year", yaxis_title="Value")
    st.plotly_chart(chart_fig, use_container_width=True)
