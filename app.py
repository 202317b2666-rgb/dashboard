import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events
import json

st.set_page_config(layout="wide")

st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click any country on the map to open the detailed popup window.")

# ------------------ Load HEX Map ------------------
hex_df = pd.read_csv("Hex.csv")
hex_df.columns = hex_df.columns.str.strip()
hex_df['iso_alpha'] = hex_df['iso_alpha'].str.upper().str.strip()

# ------------------ Load GeoJSON ------------------
with open("countries.geo.json") as f:
    geojson = json.load(f)

# ------------------ Load Final Data ------------------
df = pd.read_csv("final_with_socio_cleaned.csv")
df.columns = df.columns.str.strip()
df['ISO3'] = df['ISO3'].str.upper().str.strip()

# ------------------ Build World Map ------------------
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='hex',
    hover_name='country',
    featureidkey="id",
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(r=0, t=0, l=0, b=0))

# ------------------ One Map Only + Click Event ------------------
clicked = plotly_events(fig, click_event=True, hover_event=False)

# ------------------ If user clicked a country ------------------
if clicked:
    clicked_country = clicked[0]["hovertext"]
    iso3 = hex_df.loc[hex_df["country"] == clicked_country, "iso_alpha"].values[0]

    country_data = df[df["ISO3"] == iso3]

    # ------------------ Popup Modal ------------------
    st.markdown("""
        <style>
        .modal-bg {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            backdrop-filter: blur(5px);
            background-color: rgba(0,0,0,0.45);
            z-index: 999;
        }
        .modal-box {
            position: fixed;
            top: 5%; left: 10%;
            width: 80%; height: 90%;
            background: white;
            padding: 25px;
            border-radius: 15px;
            overflow-y: scroll;
            z-index: 1000;
        }
        </style>

        <div class="modal-bg"></div>
        <div class="modal-box">
    """, unsafe_allow_html=True)

    st.subheader(f"📊 {clicked_country} — Detailed Indicators")

    # ------------------ Charts Inside Popup ------------------
    if not country_data.empty:
        st.plotly_chart(
            px.line(country_data, x="Year", y="GDP_per_capita",
                    title="GDP Per Capita"),
            use_container_width=True
        )
        st.plotly_chart(
            px.line(country_data, x="Year", y="HDI", title="Human Development Index"),
            use_container_width=True
        )
        st.plotly_chart(
            px.line(country_data, x="Year", y="Life_Expectancy",
                    title="Life Expectancy over Time"),
            use_container_width=True
        )
        st.plotly_chart(
            px.line(country_data, x="Year", y="Gini_Index",
                    title="Gini Inequality Index"),
            use_container_width=True
        )
        st.plotly_chart(
            px.line(country_data, x="Year", y="PM25",
                    title="Air Pollution (PM2.5)"),
            use_container_width=True
        )
    else:
        st.warning("No data available for this country")

    st.button("Close Window")

    st.markdown("</div>", unsafe_allow_html=True)
