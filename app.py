# 1️⃣ Import libraries
import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

# 2️⃣ Load datasets
@st.cache_data
def load_data():
    df = pd.read_csv("final_with_socio_cleaned.csv")
    hex_df = pd.read_csv("Hex.csv")
    with open("countries.geo.json", "r") as f:
        geojson = json.load(f)
    return df, hex_df, geojson

df, hex_df, geojson = load_data()

# 3️⃣ Merge color hex
df = df.merge(hex_df[['iso_alpha','hex']], left_on='ISO3', right_on='iso_alpha', how='left')

# 4️⃣ Streamlit app layout
st.set_page_config(page_title="World Map — Click a country", layout="wide")
st.title("🌍 World Map — Click a country to open details")
st.markdown("""
**Controls:** Hover shows preview. Click a country to open a popup with time-series and details.  
**Tip:** Hover on countries for quick preview. Click to open detailed popup.
""")

# 5️⃣ Create choropleth map
fig = px.choropleth(
    df,
    geojson=geojson,
    locations='ISO3',
    color='hex',
    color_discrete_map="identity",
    hover_name='Country',
    hover_data={
        'GDP_per_capita': True,
        'Gini_Index': True,
        'Life_Expectancy': True,
        'PM25': True,
        'Health_Insurance': True,
        'Median_Age_Est': True,
        'COVID_Deaths': True,
        'COVID_Cases': True,
        'Total_Population': True
    }
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    clickmode='event+select'
)

# 6️⃣ Show map in Streamlit
st.plotly_chart(fig, use_container_width=True, key="world_map")

# 7️⃣ Capture click events
selected = st.session_state.get("selected_country", None)

click_data = st.plotly_chart(fig, use_container_width=True, key="dummy")  # needed for capturing clicks

# 8️⃣ Use Plotly's relayout_data to detect click
clicked = st.plotly_chart(fig, use_container_width=True, key="click_map")  # unique key

# 9️⃣ Capture clicks using Plotly events
click = st.session_state.get("click_data", None)
if click:
    iso_clicked = click['points'][0]['location']
    country_data = df[df['ISO3'] == iso_clicked].iloc[0]

    #  🔹 Popup-like info
    st.markdown(f"### 📍 {country_data['Country']} Details")
    col1, col2 = st.columns([1,2])
    with col1:
        st.map(pd.DataFrame({
            "lat": [0], "lon": [0]
        }))  # Placeholder for small map, can be improved
    with col2:
        st.write(f"**GDP per Capita:** {country_data['GDP_per_capita']}")
        st.write(f"**Gini Index:** {country_data['Gini_Index']}")
        st.write(f"**Life Expectancy:** {country_data['Life_Expectancy']}")
        st.write(f"**PM2.5:** {country_data['PM25']}")
        st.write(f"**Health Insurance:** {country_data['Health_Insurance']}")
        st.write(f"**Median Age:** {country_data['Median_Age_Est']}")
        st.write(f"**COVID Deaths:** {country_data['COVID_Deaths']}")
        st.write(f"**COVID Cases:** {country_data['COVID_Cases']}")
        st.write(f"**Population:** {country_data['Total_Population']}")
