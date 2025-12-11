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

# Display main map
clicked = st.plotly_chart(fig, use_container_width=True, key="world_map")

# ---------------- Capture click ----------------
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

click = st.session_state.get("click_data", None)

# For Streamlit, we capture click with plotly events
clicked_country = st.session_state.get("clicked_country", None)
if clicked_country is None:
    # Use a workaround: user clicks in Plotly map
    click_data = st.plotly_chart(fig, use_container_width=True, key="click_map")
    # Normally Streamlit doesn't give event callback, so we simulate via selection
    selected_points = fig.data[0].selectedpoints
    if selected_points:
        iso_clicked = df.iloc[selected_points[0]]['ISO3']
        st.session_state.selected_country = iso_clicked

# ---------------- Popup simulation ----------------
if st.session_state.selected_country:
    country_data = df[df['ISO3'] == st.session_state.selected_country]

    # Full-screen container with blurred background
    st.markdown(
        """
        <style>
        .popup {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(5px);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .popup-content {
            background: white;
            border-radius: 10px;
            width: 90%;
            max-width: 1200px;
            height: 80%;
            display: flex;
            padding: 20px;
        }
        .popup-left {
            width: 40%;
            padding-right: 20px;
        }
        .popup-right {
            width: 60%;
        }
        .close-btn {
            position: absolute;
            top: 10px;
            right: 20px;
            font-size: 25px;
            font-weight: bold;
            cursor: pointer;
            color: white;
        }
        </style>
        <div class="popup">
            <div class="close-btn" onclick="document.querySelector('.popup').style.display='none';">×</div>
            <div class="popup-content">
                <div class="popup-left" id="map-container"></div>
                <div class="popup-right" id="charts-container"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Plot country map in left
    country_map = px.choropleth(
        country_data,
        geojson=geojson,
        locations='ISO3',
        color='hex',
        color_discrete_map="identity"
    )
    country_map.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(country_map, use_container_width=True, key="popup_map")

    # Plot line charts in right
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
