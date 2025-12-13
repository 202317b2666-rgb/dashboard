import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="🌍 Global Health Dashboard",
    layout="wide"
)

# -------------------------------
# Session state (CRITICAL FIX)
# -------------------------------
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

# -------------------------------
# Load data
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("final_with_socio_cleaned.csv")

df = load_data()

# -------------------------------
# Sidebar controls
# -------------------------------
st.sidebar.header("📅 Year Selection")

year = st.sidebar.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    int(df["Year"].max())
)

df_year = df[df["Year"] == year]

# -------------------------------
# Title
# -------------------------------
st.title("🌍 Global Health Dashboard")
st.caption(f"Showing data for year **{year}**")

# -------------------------------
# Choropleth Map
# -------------------------------
fig = px.choropleth(
    df_year,
    locations="ISO3",
    color="HDI",
    hover_name="Country",
    color_continuous_scale="Viridis",
    title="Human Development Index (HDI)",
)

fig.update_layout(
    margin=dict(l=0, r=0, t=50, b=0),
    height=600
)

# -------------------------------
# Capture click event
# -------------------------------
click_data = st.plotly_chart(
    fig,
    use_container_width=True,
    key="map",
    on_select="rerun"
)

if click_data and "points" in click_data:
    st.session_state.selected_country = click_data["points"][0]["location"]

# -------------------------------
# Floating popup
# -------------------------------
if st.session_state.selected_country:
    country_code = st.session_state.selected_country
    row = df_year[df_year["ISO3"] == country_code].iloc[0]

    st.markdown(
        f"""
        <style>
        .popup {{
            position: fixed;
            right: 30px;
            top: 120px;
            background-color: #111;
            color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,0,0,0.6);
            width: 300px;
            z-index: 9999;
        }}
        </style>

        <div class="popup">
            <h3>📊 {row['Country']}</h3>
            <p><b>HDI:</b> {row['HDI']}</p>
            <p><b>GDP per Capita:</b> {row['GDP_per_capita']}</p>
            <p><b>Gini Index:</b> {row['Gini_Index']}</p>
            <p><b>Life Expectancy:</b> {row['Life_Expectancy']}</p>
            <p><b>Median Age (Est):</b> {row['Median_Age_Est']}</p>
            <p><b>COVID Deaths / mil:</b> {row['COVID_Deaths']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 🔥 MOST IMPORTANT LINE (BUG FIX)
    st.session_state.selected_country = None
