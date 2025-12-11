# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Load datasets
data = pd.read_csv("final_with_socio_cleaned.csv")
hex_colors = pd.read_csv("Hex.csv")
geojson = "countries.geo.json"  # path to geojson

# Map country codes to HEX colors
color_map = dict(zip(hex_colors['iso_alpha'], hex_colors['hex']))

# Title
st.title("🌍 World Map — Click a country to open details")
st.markdown("""
Hover over countries for quick preview. Click a country to open detailed popup.
""")

# Create choropleth map
fig = px.choropleth(
    data_frame=data[data['Year'] == data['Year'].max()],  # show latest year initially
    locations='ISO3',
    color='HDI',  # any metric to color the map
    hover_name='Country',
    color_continuous_scale='Viridis',
    geojson=geojson,
    featureidkey="properties.id",
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})

# Display the map and capture clicked country
clicked_country = st.plotly_chart(fig, use_container_width=True)

# Sidebar for popup simulation
if 'popup_country' not in st.session_state:
    st.session_state.popup_country = None

# Select country for popup
country_selected = st.selectbox("Select country for popup", [""] + sorted(data['ISO3'].unique()))

if country_selected:
    st.session_state.popup_country = country_selected

if st.session_state.popup_country:
    country_code = st.session_state.popup_country
    country_data = data[data['ISO3'] == country_code].sort_values('Year')

    # Simulate dark overlay container
    st.markdown(
        """
        <style>
        .popup-container {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background-color: rgba(0,0,0,0.8);
            backdrop-filter: blur(5px);
            z-index: 9999;
            padding: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .popup-content {
            background-color: #111;
            color: white;
            padding: 20px;
            border-radius: 10px;
            width: 90%;
            max-width: 1200px;
            display: flex;
        }
        .popup-left {
            flex: 1;
            margin-right: 20px;
        }
        .popup-right {
            flex: 2;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Render popup
    st.markdown('<div class="popup-container">', unsafe_allow_html=True)
    st.markdown('<div class="popup-content">', unsafe_allow_html=True)

    # Left side: country map (highlighted country)
    st.markdown('<div class="popup-left">', unsafe_allow_html=True)
    fig_country = px.choropleth(
        data_frame=data[data['ISO3'] == country_code],
        locations='ISO3',
        color='HDI',
        geojson=geojson,
        featureidkey="properties.id",
    )
    fig_country.update_geos(fitbounds="locations", visible=False)
    fig_country.update_layout(height=400, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_country, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Right side: line charts + year slider
    st.markdown('<div class="popup-right">', unsafe_allow_html=True)

    years = country_data['Year'].unique()
    year_selected = st.slider("Select Year", int(years.min()), int(years.max()), int(years.max()))

    # Filter data by year if needed
    data_year = country_data[country_data['Year'] <= year_selected]

    # Line charts for multiple metrics
    metrics = ['GDP_per_capita', 'Life_Expectancy', 'HDI', 'PM25', 'Health_Insurance', 'Median_Age_Est', 'COVID_Deaths', 'COVID_Cases']
    for metric in metrics:
        if metric in data_year.columns:
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(x=data_year['Year'], y=data_year[metric], mode='lines+markers', name=metric))
            fig_line.update_layout(title=metric, height=250, plot_bgcolor="#111", paper_bgcolor="#111", font_color="white")
            st.plotly_chart(fig_line, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Close button
    if st.button("Close"):
        st.session_state.popup_country = None

    st.markdown('</div>', unsafe_allow_html=True)
