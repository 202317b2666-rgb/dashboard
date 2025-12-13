import streamlit as st
import plotly.express as px
import pandas as pd

# Page config
st.set_page_config(page_title="Interactive Demo", layout="wide")

# Sample dataset
df = pd.DataFrame({
    "Country": ["India", "United States", "China", "Brazil", "Germany"],
    "ISO3": ["IND", "USA", "CHN", "BRA", "DEU"],
    "GDP": [2100, 23000, 18000, 1800, 4200],
    "Life Expectancy": [69, 79, 77, 75, 81]
})

st.title("🌍 Interactive Country Dashboard (Streamlit + Plotly)")

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    fig = px.scatter(
        df,
        x="GDP",
        y="Life Expectancy",
        size="GDP",
        color="Country",
        hover_name="Country",
        hover_data={
            "GDP": True,
            "Life Expectancy": True
        },
        title="Hover on points to see details"
    )

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📌 Country Details")

    country = st.selectbox("Select a country", df["Country"])

    row = df[df["Country"] == country].iloc[0]

    st.metric("GDP (Billion USD)", row["GDP"])
    st.metric("Life Expectancy", row["Life Expectancy"])
