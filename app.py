import json
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Global Dashboard",
    layout="wide",
)

# Blur background using CSS
st.markdown("""
    <style>
        .blurred {
            filter: blur(5px);
            pointer-events: none;
        }
        .popup-container {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px;
            border-radius: 15px;
            width: 75%;
            height: 75%;
            overflow-y: auto;
            box-shadow: 0px 0px 40px rgba(0,0,0,0.4);
            z-index: 9999;
        }
        .close-btn {
            float: right;
            cursor: pointer;
            background: #333;
            color: white;
            padding: 6px 10px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD DATASETS
# -------------------------------
hex_df = pd.read_csv("Hex.csv")
hex_df.rename(columns={"iso_alpha": "ISO3"}, inplace=True)

main_df = pd.read_csv("final_with_socio_cleaned.csv")
main_df["ISO3"] = main_df["ISO3"].str.upper()

with open("countries.geo.json", "r") as f:
    geojson = json.load(f)

# -------------------------------
# MERGE HEX COLORS WITH GEOJSON
# -------------------------------
id_to_hex = dict(zip(hex_df["ISO3"], hex_df["hex"]))

for f in geojson["features"]:
    iso = f["id"]        # GeoJSON ID = AFG, IND, USA
    f["properties"]["hex"] = id_to_hex.get(iso, "#CCCCCC")

# -------------------------------
# BUILD MAP
# -------------------------------
fig = px.choropleth(
    main_df[main_df["Year"] == main_df["Year"].max()],
    geojson=geojson,
    locations="ISO3",
    color="ISO3",
    color_discrete_map=id_to_hex,
    hover_name="Country",
)

fig.update_geos(fitbounds="locations", visible=False)

click = st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# CLICK DETECTION
# -------------------------------
clicked_country = None

if click and hasattr(click, "selection") and click.selection:
    try:
        point = click.selection["points"][0]
        clicked_country = point.get("location")
    except:
        pass

# -------------------------------
# POPUP CONTENT
# -------------------------------
if clicked_country:
    country_data = main_df[main_df["ISO3"] == clicked_country]

    st.markdown('<div class="blurred">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="popup-container">', unsafe_allow_html=True)

    st.markdown(
        f"<div class='close-btn' onclick='window.location.reload()'>X</div>",
        unsafe_allow_html=True,
    )

    country_name = country_data["Country"].iloc[0]
    st.markdown(f"## 📊 {country_name} — Overview")

    # GDP Chart
    gdp_fig = px.line(country_data, x="Year", y="GDP_per_capita", title="GDP per Capita")
    st.plotly_chart(gdp_fig, use_container_width=True)

    # Life Expectancy Chart
    life_fig = px.line(country_data, x="Year", y="Life_Expectancy", title="Life Expectancy")
    st.plotly_chart(life_fig, use_container_width=True)

    # HDI Chart
    hdi_fig = px.line(country_data, x="Year", y="HDI", title="Human Development Index")
    st.plotly_chart(hdi_fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
