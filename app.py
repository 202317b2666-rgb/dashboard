# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Interactive World Map with Floating Popup")

# Sample data for 3 countries
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

# Create choropleth map
fig = px.choropleth(
    df,
    locations="iso",
    color="value",
    hover_name="country",
    custom_data=["img"],
    color_continuous_scale="Blues"
)

fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br><img src='%{customdata[0]}' width='100'>"
)
fig.update_layout(
    geo=dict(showframe=False, showcoastlines=False),
    margin=dict(l=0, r=0, t=0, b=0)
)

# Display the map
selected = st.plotly_chart(fig, use_container_width=True)

# HTML + CSS popup overlay
html_code = """
<div id="popup" style="
    display:none;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    z-index: 999;
">
    <h3 id="country-name"></h3>
    <img id="country-img" src="" width="200">
</div>

<script>
const mapDiv = document.querySelector('[data-testid="stPlotlyChart"]');
mapDiv.on('plotly_click', function(data){
    const point = data.points[0];
    document.getElementById('country-name').innerText = point.hovertext;
    document.getElementById('country-img').src = point.customdata[0];
    document.getElementById('popup').style.display = 'block';
});
</script>
"""

st.components.v1.html(html_code, height=0)
