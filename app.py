import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

# ---------------- Load data ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("final_with_socio_cleaned.csv")
    hex_df = pd.read_csv("Hex.csv")
    with open("countries.geo.json", "r") as f:
        geojson = json.load(f)
    return df, hex_df, geojson

df, hex_df, geojson = load_data()
df = df.merge(hex_df[['iso_alpha','hex']], left_on='ISO3', right_on='iso_alpha', how='left')

# ---------------- Layout ----------------
st.set_page_config(page_title="Interactive World Map", layout="wide")
st.title("🌍 World Map — Click a country to open details")
st.markdown("""
Hover on a country to preview metrics. Click a country to see detailed popup with charts and country map.
""")

# ---------------- Choropleth map ----------------
fig = px.choropleth(
    df,
    geojson=geojson,
    locations='ISO3',
    color='hex',
    color_discrete_map="identity",
    hover_name='Country',
    hover_data={
        'GDP_per_capita': True,
        'Gini_Index': True,
        'Life_Expectancy': True,
        'PM25': True,
        'Health_Insurance': True,
        'Median_Age_Est': True,
        'COVID_Deaths': True,
        'COVID_Cases': True,
        'Total_Population': True
    }
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    clickmode='event+select'
)

# ---------------- Display map ----------------
clicked = st.plotly_chart(fig, use_container_width=True, key="world_map")

# ---------------- Session state for popup ----------------
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# ---------------- Popup container ----------------
selected = st.selectbox("Select country for popup", df['ISO3'].unique(), index=0)
st.session_state.selected_country = selected

if st.session_state.selected_country:
    country_data = df[df['ISO3'] == st.session_state.selected_country]

    # Popup styling
    st.markdown("""
    <style>
    .popup-container {
        position: relative;
        background: rgba(0,0,0,0.6);
        padding: 50px 0;
    }
    .popup-box {
        background: white;
        border-radius: 10px;
        width: 80%;
        max-width: 1000px;
        margin: 0 auto;
        display: flex;
        padding: 20px;
        backdrop-filter: blur(5px);
    }
    .popup-left {
        width: 40%;
        padding-right: 20px;
    }
    .popup-right {
        width: 60%;
    }
    </style>
    <div class="popup-container">
        <div class="popup-box">
            <div class="popup-left" id="map-container"></div>
            <div class="popup-right" id="charts-container"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Plot country map
    country_map = px.choropleth(
        country_data,
        geojson=geojson,
        locations='ISO3',
        color='hex',
        color_discrete_map="identity"
    )
    country_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(country_map, use_container_width=True, key="popup_map")

    # Plot line charts
    attributes = ['GDP_per_capita','Gini_Index','Life_Expectancy','PM25','Health_Insurance','Median_Age_Est','COVID_Deaths','COVID_Cases']
    chart_fig = go.Figure()
    for attr in attributes:
        chart_fig.add_trace(go.Scatter(
            x=country_data['Year'],
            y=country_data[attr],
            mode='lines+markers',
            name=attr
        ))
    chart_fig.update_layout(title=f"{country_data.iloc[0]['Country']} Metrics Over Time", xaxis_title="Year", yaxis_title="Value")
    st.plotly_chart(chart_fig, use_container_width=True, key="popup_charts")
