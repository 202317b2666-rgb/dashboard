import streamlit as st
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    "country": ["India", "United States", "China"],
    "iso": ["IND", "USA", "CHN"],
    "value": [1, 2, 3],
    "img": [
        "https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
        "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_China.svg"
    ]
})

fig = px.choropleth(
    df,
    locations="iso",
    color="value",
    hover_name="country",
    custom_data=["img"],
    color_continuous_scale="Blues"
)

fig.update_traces(
    hovertemplate="""
    <b>%{hovertext}</b><br><br>
    <img src="%{customdata[0]}" width="120"><br>
    """
)

fig.update_layout(
    geo=dict(showframe=False, showcoastlines=False),
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig, use_container_width=True)
