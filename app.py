import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🌍 World Map Hover Test (Figma-like Interaction)")

# ---- TEST DATA (ONLY 3 COUNTRIES) ----
df = pd.DataFrame({
    "country": ["India", "United States", "Germany"],
    "iso_alpha": ["IND", "USA", "DEU"],
    "Life Expectancy": [69.7, 78.9, 81.1],
    "HDI": [0.633, 0.921, 0.942]
})

# ---- CHOROPLETH MAP ----
fig = px.choropleth(
    df,
    locations="iso_alpha",
    color="Life Expectancy",
    hover_name="country",
    hover_data={
        "Life Expectancy": True,
        "HDI": True,
        "iso_alpha": False
    },
    color_continuous_scale="Blues",
)

# ---- MAP STYLING (IMPORTANT FOR CLEAN LOOK) ----
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type="natural earth",
        bgcolor="#F9FAFB"
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=500
)

st.plotly_chart(fig, use_container_width=True)
