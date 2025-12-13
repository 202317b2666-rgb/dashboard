import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🌍 World Map – Hover Highlight (Pop Effect Simulation)")

# --- TEST DATA (3 COUNTRIES ONLY) ---
df = pd.DataFrame({
    "country": ["India", "United States", "Germany"],
    "iso_alpha": ["IND", "USA", "DEU"],
    "Life Expectancy": [69.7, 78.9, 81.1],
    "HDI": [0.633, 0.921, 0.942]
})

# --- CHOROPLETH MAP ---
fig = px.choropleth(
    df,
    locations="iso_alpha",
    color="Life Expectancy",
    hover_name="country",
    hover_data={
        "Life Expectancy": True,
        "HDI": True
    },
    color_continuous_scale="Blues"
)

# --- STRONG HOVER VISUAL EMPHASIS ---
fig.update_traces(
    marker_line_width=1.5,
    marker_line_color="black",
    hovertemplate=
        "<b>%{hovertext}</b><br>" +
        "Life Expectancy: %{customdata[0]}<br>" +
        "HDI: %{customdata[1]}<extra></extra>"
)

# --- MAP STYLING ---
fig.update_layout(
    geo=dict(
        projection_type="natural earth",
        showframe=False,
        showcoastlines=False,
        showcountries=True,
        countrycolor="white",
        bgcolor="#F9FAFB"
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=550
)

st.plotly_chart(fig, use_container_width=True)
