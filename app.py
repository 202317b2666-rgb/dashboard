import json
import streamlit as st
import pandas as pd
import plotly.express as px
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

# Force 2nd and 4th columns
iso_col = df_hex.columns[1]     # 2nd column
hex_col = df_hex.columns[3]     # 4th column

# Add validation flags
df_hex["ISO_Valid"] = df_hex[iso_col].apply(looks_like_iso3)
df_hex["HEX_Valid"] = df_hex[hex_col].apply(looks_like_hex)

# Show errors in UI if any
invalid_rows = df_hex[(df_hex["ISO_Valid"] == False) | (df_hex["HEX_Valid"] == False)]

if not invalid_rows.empty:
    st.error("Invalid ISO3 or HEX values found in Hex.csv")
    st.dataframe(invalid_rows)

# Clean and standardize
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

df_countries = (
    pd.DataFrame(rows)
    .drop_duplicates(subset="iso3")
    .reset_index(drop=True)
)

# ------------------------------------------------------------
# 4. MERGE COUNTRIES WITH HEX COLORS
# ------------------------------------------------------------
df = df_countries.merge(df_hex[["iso3", "hex"]], on="iso3", how="left")
df["hex"] = df["hex"].fillna("#cccccc")     # default grey

# Build Plotly discrete color map
color_map = {row.iso3: row.hex for row in df.itertuples(index=False)}

# ------------------------------------------------------------
# 5. WORLD MAP FUNCTION (your original structure)
# ------------------------------------------------------------
def build_world_map(df):
    fig = px.choropleth(
        df,
        geojson=world_geojson, 
        locations="iso3",
        featureidkey="id",
        color="iso3",                     # <= use ISO3 for discrete mapping
        hover_name="country",
        projection="natural earth",
        color_discrete_map=color_map,     # <= apply HEX colors
    )

    fig.update_traces(
        marker_line_width=0.8,
        marker_line_color="white",
        hovertemplate="<b>%{hovertext}</b><extra></extra>",
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

# ------------------------------------------------------------
# 6. BUILD FINAL MAP
# ------------------------------------------------------------
fig = build_world_map(df)

# ------------------------------------------------------------
# 7. REMOVE EXTRA PADDING (your original CSS)
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 8. DISPLAY MAP
# ------------------------------------------------------------
st.plotly_chart(fig, use_container_width=True)
