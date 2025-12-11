# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Load datasets
# -----------------------------
@st.cache_data
def load_data():
    world_df = pd.read_csv("final_with_socio_cleaned.csv")
    hex_df = pd.read_csv("Hex.csv")
    geojson = "countries.geo.json"
    return world_df, hex_df, geojson

world_df, hex_df, geojson_path = load_data()

# -----------------------------
# Merge colors
# -----------------------------
world_df = world_df.merge(hex_df[['iso_alpha', 'hex']], left_on='ISO3', right_on='iso_alpha', how='left')

# -----------------------------
# App Title
# -----------------------------
st.title("🌍 Interactive World Map — Click a country to view details")
st.markdown("""
Hover on countries for quick preview. Click a country to open detailed popup.
""")

# -----------------------------
# Session state for popup
# -----------------------------
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = None

# -----------------------------
# World Map
# -----------------------------
fig = px.choropleth(
    world_df,
    locations="ISO3",
    color="hex",
    hover_name="Country",
    hover_data=["GDP_per_capita","Gini_Index","Life_Expectancy"],
    color_discrete_map="identity",
    geojson=geojson_path,
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})

# Detect click
click_data = st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Country selector (to simulate click)
# -----------------------------
country_options = world_df['ISO3'].unique()
selected_iso = st.selectbox("Select country for popup", country_options, index=0)

if st.button("Open Country Details"):
    st.session_state.selected_country = selected_iso

# -----------------------------
# Popup Overlay
# -----------------------------
if st.session_state.selected_country:
    country_iso = st.session_state.selected_country
    country_data = world_df[world_df['ISO3'] == country_iso]
    country_name = country_data['Country'].iloc[0]

    # Darkened overlay
    overlay = st.container()
    with overlay:
        st.markdown(
            """
            <style>
            .overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.8);
                z-index: 100;
                padding: 30px;
            }
            .popup-content {
                background-color: #111;
                padding: 20px;
                border-radius: 10px;
                color: white;
            }
            </style>
            """, unsafe_allow_html=True
        )
        st.markdown(f'<div class="overlay"><div class="popup-content">', unsafe_allow_html=True)

        st.markdown(f"## {country_name} ({country_iso})")

        # Columns for map + charts
        col1, col2 = st.columns([1,2])

        # -----------------------------
        # Left column: mini country map
        # -----------------------------
        with col1:
            mini_map = px.choropleth(
                country_data,
                locations="ISO3",
                color="hex",
                color_discrete_map="identity",
                geojson=geojson_path,
                hover_name="Country"
            )
            mini_map.update_geos(fitbounds="locations", visible=False)
            mini_map.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(mini_map)

        # -----------------------------
        # Right column: line charts
        # -----------------------------
        with col2:
            min_year = int(country_data['Year'].min())
            max_year = int(country_data['Year'].max())
            selected_year = st.slider("Select Year Range", min_year, max_year, (min_year,max_year))

            filtered_data = country_data[(country_data['Year'] >= selected_year[0]) & 
                                         (country_data['Year'] <= selected_year[1])]

            metrics = ["GDP_per_capita", "Gini_Index", "Life_Expectancy", "PM25", "Health_Insurance"]
            for metric in metrics:
                fig_metric = px.line(filtered_data, x="Year", y=metric, title=metric)
                st.plotly_chart(fig_metric, use_container_width=True)

        # Close button
        if st.button("Close"):
            st.session_state.selected_country = None

        st.markdown("</div></div>", unsafe_allow_html=True)
