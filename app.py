import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🌍 World Map – Pop-up Hover Simulation")

# Base world (empty just to show map)
fig = go.Figure()

fig.add_trace(
    go.Choropleth(
        locations=[],
        z=[],
        locationmode="ISO-3",
        showscale=False
    )
)

# --- POP-UP COUNTRIES (3 ONLY) ---
popup_df = pd.DataFrame({
    "country": ["India", "United States", "Germany"],
    "lat": [20.5937, 37.0902, 51.1657],
    "lon": [78.9629, -95.7129, 10.4515],
    "Life Expectancy": [69.7, 78.9, 81.1],
    "HDI": [0.633, 0.921, 0.942]
})

fig.add_trace(
    go.Scattergeo(
        lat=popup_df["lat"],
        lon=popup_df["lon"],
        text=popup_df["country"],
        mode="markers",
        marker=dict(
            size=18,
            color="#2563EB",
            opacity=0.85
        ),
        hovertemplate=
        "<b>%{text}</b><br>" +
        "Life Expectancy: %{customdata[0]}<br>" +
        "HDI: %{customdata[1]}<extra></extra>",
        customdata=popup_df[["Life Expectancy", "HDI"]].values
    )
)

fig.update_layout(
    geo=dict(
        projection_type="natural earth",
        showland=True,
        landcolor="#E5E7EB",
        showcountries=True,
        countrycolor="white",
        bgcolor="#F9FAFB"
    ),
    height=550,
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig, use_container_width=True)
