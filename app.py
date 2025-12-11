# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Interactive World Map")

# 1️⃣ Load datasets
@st.cache_data
def load_data():
    data = pd.read_csv("final_with_socio_cleaned.csv")
    colors = pd.read_csv("Hex.csv")
    return data, colors

data, colors = load_data()

# Ensure ISO3 is string and drop missing
iso3_list = data['ISO3'].dropna().astype(str).unique()
country_selected = st.selectbox("Select country for popup", [""] + sorted(iso3_list))

# 2️⃣ World Map
# Merge color info
data_color = data.merge(colors[['iso_alpha', 'hex']], left_on='ISO3', right_on='iso_alpha', how='left')
latest_year = data['Year'].max()
map_data = data_color[data_color['Year'] == latest_year]

fig = px.choropleth(
    map_data,
    locations="ISO3",
    color="HDI",
    hover_name="Country",
    hover_data=["GDP_per_capita", "Life_Expectancy", "PM25", "Health_Insurance", "Median_Age_Est"],
    color_continuous_scale="Viridis",
    labels={"HDI": "Human Development Index"},
)

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    height=600,
)

st.plotly_chart(fig, use_container_width=True)

# 3️⃣ Country Popup Modal
if country_selected:
    country_data = data[data['ISO3'] == country_selected].sort_values("Year")
    
    # Year slider
    year_min = int(country_data['Year'].min())
    year_max = int(country_data['Year'].max())
    selected_year = st.slider("Select Year", year_min, year_max, year_max)

    # Filter by slider year
    year_data = country_data[country_data['Year'] <= selected_year]

    # Use st.modal for dark overlay popup
    with st.modal(f"{country_selected} Details", key="modal_popup"):
        st.markdown("<style>div[data-testid='stModal'] {background-color: rgba(0,0,0,0.8); color: white;}</style>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        
        # Left: Mini Map
        with col1:
            fig_map = px.choropleth(
                year_data,
                locations="ISO3",
                color="HDI",
                hover_name="Country",
                color_continuous_scale="Viridis"
            )
            fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300)
            st.plotly_chart(fig_map, use_container_width=True)
        
        # Right: Line Charts
        with col2:
            metrics = ["GDP_per_capita", "Life_Expectancy", "PM25", "Health_Insurance", "Median_Age_Est", "COVID_Deaths", "COVID_Cases"]
            for metric in metrics:
                fig_line = px.line(year_data, x="Year", y=metric, title=metric)
                st.plotly_chart(fig_line, use_container_width=True)
