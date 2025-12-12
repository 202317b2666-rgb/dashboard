import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(
    page_title="🌍 Interactive Global Health Demographics Dashboard",
    page_icon="world_map",
    layout="wide",
)

# ------------------------------------------------------------
# 1. LOAD GEOJSON
# ------------------------------------------------------------
with open("countries.geo.json", "r", encoding="utf-8") as f:
    world_geojson = json.load(f)

# ------------------------------------------------------------
# 2. LOAD HEX CSV + VALIDATE COLUMN 2 = ISO, COLUMN 3 = HEX
# ------------------------------------------------------------
df_hex = pd.read_csv("Hex.csv", dtype=str, keep_default_na=False)

def looks_like_iso3(s):
    return isinstance(s, str) and bool(re.fullmatch(r"[A-Za-z]{3}", s.strip()))

def looks_like_hex(s):
    return isinstance(s, str) and bool(re.fullmatch(r"#?[0-9A-Fa-f]{6}", s.strip()))

iso_col = df_hex.columns[1]
hex_col = df_hex.columns[3]

df_hex["ISO_Valid"] = df_hex[iso_col].apply(looks_like_iso3)
df_hex["HEX_Valid"] = df_hex[hex_col].apply(looks_like_hex)

invalid_rows = df_hex[(df_hex["ISO_Valid"] == False) | (df_hex["HEX_Valid"] == False)]
if not invalid_rows.empty:
    st.error("Invalid ISO3 or HEX values found in Hex.csv")
    st.dataframe(invalid_rows)

df_hex["iso3"] = df_hex[iso_col].str.extract(r"([A-Za-z]{3})")[0].str.upper()
df_hex["hex"] = df_hex[hex_col].apply(
    lambda h: ("#" + h.strip()) if looks_like_hex(h) and not h.startswith("#") else h
)

# ------------------------------------------------------------
# 3. BUILD DF OF ALL COUNTRIES FROM GEOJSON
# ------------------------------------------------------------
rows = []
for feature in world_geojson["features"]:
    iso3 = feature.get("id")
    props = feature.get("properties", {})
    name = props.get("name")
    if not iso3:
        continue
    rows.append({"iso3": iso3.upper(), "country": name})

df_countries = pd.DataFrame(rows).drop_duplicates(subset="iso3").reset_index(drop=True)

# ------------------------------------------------------------
# 4. MERGE COUNTRIES WITH HEX COLORS
# ------------------------------------------------------------
df = df_countries.merge(df_hex[["iso3", "hex"]], on="iso3", how="left")
df["hex"] = df["hex"].fillna("#cccccc")
color_map = {row.iso3: row.hex for row in df.itertuples(index=False)}

# ------------------------------------------------------------
# 5. LOAD FINAL MERGED DATASET
# ------------------------------------------------------------
data = pd.read_csv("final_with_socio_cleaned.csv")
data['ISO3'] = data['ISO3'].str.upper()

# ------------------------------------------------------------
# 6. WORLD MAP FUNCTION
# ------------------------------------------------------------
def build_world_map(df):
    fig = px.choropleth(
        df,
        geojson=world_geojson,
        locations="iso3",
        featureidkey="id",
        color="iso3",
        hover_name="country",
        projection="natural earth",
        color_discrete_map=color_map,
    )

    fig.update_traces(
        marker_line_width=0.8,
        marker_line_color="white",
        hovertemplate="<b>%{hovertext}</b><extra></extra>",
        hoverlabel=dict(bgcolor="white", font_size=16)
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#b9e6ff",
        geo=dict(
            bgcolor="#b9e6ff",
            showframe=False,
            showcoastlines=False,
            projection_scale=0.67,
            center=dict(lat=10, lon=0),
            lataxis=dict(range=[-90, 90])
        ),
        height=650,
        dragmode=False,
    )

    return fig

fig = build_world_map(df)

# ------------------------------------------------------------
# 7. REMOVE EXTRA PADDING
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding:0rem !important;
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 8. DISPLAY MAP
# ------------------------------------------------------------
clicked_iso = st.session_state.get("clicked_iso", "")

def handle_click():
    st.session_state.clicked_iso = st.session_state.country_select

# Country selector hidden (used for popup trigger)
st.selectbox(
    "Select country for popup (hidden, used internally)",
    [""] + sorted(data['ISO3'].unique()),
    key="country_select",
    on_change=handle_click
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# 9. POPUP OVERLAY CSS
# ------------------------------------------------------------
st.markdown("""
<style>
.popup-overlay {
    position: fixed;
    top:0; left:0;
    width:100%; height:100%;
    background: rgba(0,0,0,0.85);
    backdrop-filter: blur(6px);
    display:flex;
    justify-content:center;
    align-items:center;
    z-index:9999;
}
.popup-box {
    width: 85%;
    max-height: 90%;
    overflow-y:auto;
    background:#1a1a1a;
    color:white;
    padding:30px;
    border-radius:15px;
}
.line-chart {
    margin-top:20px;
}
.close-btn {
    background:#f44336;
    color:white;
    border:none;
    padding:10px 20px;
    font-size:16px;
    border-radius:5px;
    cursor:pointer;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 10. SHOW POPUP IF CLICKED
# ------------------------------------------------------------
if clicked_iso:
    country_data = data[data['ISO3'] == clicked_iso]
    if not country_data.empty:
        country_name = country_data['Country'].iloc[0]
        # Line chart for all metrics
        metrics = [
            'GDP_per_capita', 'Gini_Index', 'Life_Expectancy', 'PM25', 
            'Health_Insurance', 'Median_Age_Est', 'Median_Age_Mid',
            'COVID_Deaths','COVID_Cases','Population_Density','Total_Population'
        ]
        fig_line = go.Figure()
        for m in metrics:
            fig_line.add_trace(go.Scatter(
                x=country_data['Year'], y=country_data[m],
                mode='lines+markers', name=m
            ))
        fig_line.update_layout(
            template="plotly_dark",
            height=400, margin=dict(l=20,r=20,t=20,b=20)
        )
        
        st.markdown(f"""
        <div class="popup-overlay">
            <div class="popup-box">
                <h2>{country_name} ({clicked_iso})</h2>
                <div style="display:flex; gap:20px;">
                    <div style="flex:1">
                        <img src="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips/USA_counties_map.png" width="100%">
                        <!-- Replace with small map if needed -->
                    </div>
                    <div style="flex:2">
        """, unsafe_allow_html=True)

        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("""
                    </div>
                </div>
                <button class="close-btn" onclick="window.location.reload();">Close</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
