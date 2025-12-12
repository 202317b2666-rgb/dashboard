import json
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Global Dashboard", layout="wide")

# -------------------------
# LOAD FILES
# -------------------------
hex_df = pd.read_csv("Hex.csv")
hex_df.rename(columns={"iso_alpha": "ISO3"}, inplace=True)

main_df = pd.read_csv("final_with_socio_cleaned.csv")
main_df["ISO3"] = main_df["ISO3"].str.upper()

with open("countries.geo.json") as f:
    geojson = json.load(f)

# -------------------------
# MERGE HEX COLORS
# -------------------------
id_to_hex = dict(zip(hex_df["ISO3"], hex_df["hex"]))

for f in geojson["features"]:
    iso = f["id"]
    f["properties"]["hex"] = id_to_hex.get(iso, "#d3d3d3")

# -------------------------
# BUILD CLEAN MAP (NO HOVERBOX)
# -------------------------
latest_year = main_df["Year"].max()
df_latest = main_df[main_df["Year"] == latest_year]

fig = px.choropleth(
    df_latest,
    geojson=geojson,
    locations="ISO3",
    color="ISO3",
    color_discrete_map=id_to_hex,
    hoverinfo="skip",
)

# REMOVE mini black hover boxes
fig.update_traces(hovertemplate=None, hoverinfo="skip")
fig.update_geos(fitbounds="locations", visible=False)

# Disable map margin
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

# -------------------------
# CLICK EVENT USING STREAMLIT SESSION STATE
# -------------------------
if "clicked_country" not in st.session_state:
    st.session_state.clicked_country = None

def country_clicked(trace, points, selector):
    if points.point_inds:
        idx = points.point_inds[0]
        st.session_state.clicked_country = df_latest.iloc[idx]["ISO3"]

fig.data[0].on_click(country_clicked)

# Show Map
st.plotly_chart(fig, use_container_width=True)

clicked = st.session_state.clicked_country

# -------------------------
# POPUP UI
# -------------------------
if clicked:

    country_df = main_df[main_df["ISO3"] == clicked]
    country_name = country_df["Country"].iloc[0]

    # POPUP WHITE BOX
    popup_css = """
    <style>
        #popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 75%;
            height: 75%;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0px 0px 40px rgba(0,0,0,0.4);
            z-index: 10000;
            overflow-y: auto;
        }
        body {
            filter: blur(5px);
        }
        #close-btn {
            float: right;
            background: black;
            color: white;
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
    """

    st.markdown(popup_css, unsafe_allow_html=True)
    st.markdown('<div id="popup">', unsafe_allow_html=True)
    st.markdown('<div id="close-btn" onclick="window.location.reload()">X</div>', unsafe_allow_html=True)

    st.markdown(f"## 📌 {country_name} — Country Insights")

    # GDP CHART
    st.plotly_chart(
        px.line(country_df, x="Year", y="GDP_per_capita", title="GDP per Capita"),
        use_container_width=True
    )

    # Life Expectancy CHART
    st.plotly_chart(
        px.line(country_df, x="Year", y="Life_Expectancy", title="Life Expectancy"),
        use_container_width=True
    )

    # HDI CHART
    st.plotly_chart(
        px.line(country_df, x="Year", y="HDI", title="HDI Trend"),
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)
