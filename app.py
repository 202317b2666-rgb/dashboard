import streamlit as st
import pandas as pd
import json
import plotly.express as px
from streamlit_plotly_events import plotly_events

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="🌍 Global Health Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌍 Global Health Dashboard")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("final_with_socio_cleaned.csv")
    hex_df = pd.read_csv("Hex.csv")
    with open("countries.geo.json") as f:
        geo = json.load(f)
    return df, hex_df, geo

df, hex_df, geojson = load_data()

# ----------------------------
# CLEAN + MERGE
# ----------------------------
df["ISO3"] = df["ISO3"].astype(str)
hex_df["iso_alpha"] = hex_df["iso_alpha"].astype(str)

merged = df.merge(
    hex_df,
    left_on="ISO3",
    right_on="iso_alpha",
    how="left"
)

merged["hex"] = merged["hex"].fillna("#444444")

# ----------------------------
# YEAR SLIDER
# ----------------------------
min_year = int(merged["Year"].min())
max_year = int(merged["Year"].max())

year = st.slider(
    "📅 Select Year",
    min_year,
    max_year,
    max_year
)

year_df = merged[merged["Year"] == year]

# ----------------------------
# WORLD MAP
# ----------------------------
fig = px.choropleth(
    year_df,
    geojson=geojson,
    locations="ISO3",
    featureidkey="properties.ISO_A3",
    color="hex",
    color_discrete_map="identity",
    hover_name="Country",
)

fig.update_geos(
    showcoastlines=False,
    showcountries=False,
    bgcolor="black"
)

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="black",
    plot_bgcolor="black",
)

# ----------------------------
# CLICK EVENTS
# ----------------------------
selected = plotly_events(
    fig,
    click_event=True,
    hover_event=False,
    select_event=False,
    override_height=600,
    override_width="100%"
)

# ----------------------------
# STORE CLICKED COUNTRY
# ----------------------------
if selected:
    iso = selected[0]["location"]

    row = year_df[year_df["ISO3"] == iso]
    if not row.empty:
        r = row.iloc[0]
        st.session_state["popup"] = {
            "Country": r["Country"],
            "HDI": r["HDI"],
            "GDP": r["GDP_per_capita"],
            "Gini": r["Gini_Index"],
            "Life": r["Life_Expectancy"],
            "Median": r["Median_Age_Est"],
            "COVID_D": r["COVID_Deaths"],
            "COVID_C": r["COVID_Cases"]
        }

# ----------------------------
# FLOATING POPUP
# ----------------------------
if "popup" in st.session_state:
    p = st.session_state["popup"]

    st.markdown(
        f"""
        <div style="
            position:fixed;
            top:90px;
            right:40px;
            width:320px;
            background:#0b1c2d;
            padding:20px;
            border-radius:14px;
            color:white;
            z-index:9999;
            box-shadow:0 0 25px rgba(0,0,0,0.7);
            font-size:14px;
        ">
        <h4 style="margin-top:0;">📊 {p['Country']}</h4>
        <hr style="border:1px solid #333;">
        <b>HDI:</b> {p['HDI']}<br>
        <b>GDP / Capita:</b> {p['GDP']}<br>
        <b>Gini Index:</b> {p['Gini']}<br>
        <b>Life Expectancy:</b> {p['Life']}<br>
        <b>Median Age:</b> {p['Median']}<br>
        <b>COVID Deaths / mil:</b> {p['COVID_D']}<br>
        <b>COVID Cases / mil:</b> {p['COVID_C']}
        </div>
        """,
        unsafe_allow_html=True
    )
