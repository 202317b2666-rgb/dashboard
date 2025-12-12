# app.py
import json
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events

st.set_page_config(page_title="Global Dashboard", layout="wide")

# -------------------------
# Load files
# -------------------------
hex_df = pd.read_csv("Hex.csv", dtype=str)
hex_df.columns = hex_df.columns.str.strip()
# make sure iso code column name and values are correct
hex_df['ISO3'] = hex_df['iso_alpha'].str.upper().str.strip()
hex_df['hex'] = hex_df['hex'].str.strip().fillna('#d3d3d3')

main_df = pd.read_csv("final_with_socio_cleaned.csv", dtype=str)
main_df.columns = main_df.columns.str.strip()
# normalize Year as int, numeric columns as float as needed
main_df['ISO3'] = main_df['ISO3'].str.upper().str.strip()
main_df['Year'] = main_df['Year'].astype(int)
# convert numeric columns to numeric (coerce errors -> NaN)
num_cols = ['GDP_per_capita','Gini_Index','Life_Expectancy','PM25','Health_Insurance','HDI']
for c in num_cols:
    if c in main_df.columns:
        main_df[c] = pd.to_numeric(main_df[c], errors='coerce')

with open("countries.geo.json") as f:
    geojson = json.load(f)

# -------------------------
# Build color mapping from hex.csv
# -------------------------
id_to_hex = dict(zip(hex_df['ISO3'], hex_df['hex']))

# Ensure geojson features have ids as ISO3 (your file uses top-level 'id' as ISO3)
# We'll add the hex to properties for clarity
for feat in geojson['features']:
    iso = feat.get('id')
    feat['properties']['hex'] = id_to_hex.get(iso, '#d3d3d3')

# -------------------------
# Plot choropleth (single map)
# -------------------------
latest_year = main_df['Year'].max()
df_latest = main_df[main_df['Year'] == latest_year]

# Use a dummy categorical color mapped by ISO->hex (Plotly Express expects category values)
df_latest = df_latest.copy()
df_latest['COLOR_KEY'] = df_latest['ISO3']  # each ISO3 is a category

fig = px.choropleth(
    df_latest,
    geojson=geojson,
    locations='ISO3',
    color='COLOR_KEY',
    color_discrete_map=id_to_hex,
    hover_name='Country',
    featureidkey='id',
)

# remove hover template and small tooltip
fig.update_traces(hovertemplate=None, marker_line_width=0.2)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=650)

# Render map and capture click events using streamlit-plotly-events
st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click on any country to open detailed indicators (popup).")

clicked = plotly_events(fig, click_event=True, hover_event=False, key="world_map_events")

# -------------------------
# Modal helpers
# -------------------------
def open_modal_for_iso(iso3):
    st.session_state.show_modal = True
    st.session_state.modal_iso = iso3

def close_modal():
    st.session_state.show_modal = False
    st.session_state.modal_iso = None
    st.experimental_rerun()

if "show_modal" not in st.session_state:
    st.session_state.show_modal = False
    st.session_state.modal_iso = None

# If user clicked a country, try to resolve iso
if clicked:
    info = clicked[0]
    iso_clicked = None
    # common key for choropleth is 'location'
    if 'location' in info and info['location']:
        iso_clicked = info['location']
    # fallback: look for customdata / pointNumber mapping
    if not iso_clicked:
        # try to find by comparing lat/lon or hovertext keys if available
        if 'hovertext' in info and info['hovertext']:
            # hovertext sometimes contains country name; try to map
            country_name = info['hovertext']
            row = hex_df[hex_df['country'].str.strip() == country_name.strip()]
            if not row.empty:
                iso_clicked = row.iloc[0]['ISO3']
    # if resolved, open modal
    if iso_clicked:
        open_modal_for_iso(iso_clicked)

# -------------------------
# Popup modal rendering
# -------------------------
if st.session_state.show_modal and st.session_state.modal_iso:
    iso = st.session_state.modal_iso
    # fetch country name and data
    row = df_latest[df_latest['ISO3'] == iso]
    country_name = row['Country'].iloc[0] if not row.empty else iso
    country_data = main_df[main_df['ISO3'] == iso].sort_values('Year')

    # CSS for modal + blurred background
    st.markdown("""
    <style>
    .modal-bg {
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.45);
        backdrop-filter: blur(4px);
        z-index: 1000;
    }
    .modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-50%);
        width: 85%;
        height: 85%;
        background: #fff;
        z-index: 1001;
        border-radius: 12px;
        padding: 18px;
        overflow: auto;
        box-shadow: 0 8px 40px rgba(0,0,0,0.3);
    }
    .modal .close {
        float: right;
        background: #333;
        color: #fff;
        padding: 6px 10px;
        border-radius: 6px;
        cursor: pointer;
    }
    </style>
    <div class="modal-bg"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="modal">', unsafe_allow_html=True)
    st.markdown(f'<div class="close" onclick="window.parent.postMessage({{"streamlitCloseModal": true}}, \"*\")">Close</div>', unsafe_allow_html=True)
    st.markdown(f"## 📊 {country_name} — Detailed Indicators")

    # Charts (only if data exists)
    if country_data.empty:
        st.warning("No socio-economic time-series data available for this country.")
    else:
        # Example charts; add more indicators if present
        if 'GDP_per_capita' in country_data.columns:
            st.plotly_chart(px.line(country_data, x='Year', y='GDP_per_capita', title='GDP per Capita'), use_container_width=True)
        if 'Life_Expectancy' in country_data.columns:
            st.plotly_chart(px.line(country_data, x='Year', y='Life_Expectancy', title='Life Expectancy'), use_container_width=True)
        if 'HDI' in country_data.columns:
            st.plotly_chart(px.line(country_data, x='Year', y='HDI', title='Human Development Index (HDI)'), use_container_width=True)
        # additional small panels
        cols = st.columns(3)
        for i, key in enumerate(['Gini_Index','PM25','Health_Insurance']):
            if key in country_data.columns:
                with cols[i]:
                    latest_val = country_data[key].dropna().astype(float).iloc[-1] if any(~country_data[key].isna()) else "N/A"
                    st.metric(key.replace("_"," "), f"{latest_val}")

    st.markdown('</div>', unsafe_allow_html=True)

    # JS bridge to close modal (since postMessage used above)
    st.components.v1.html("""
    <script>
    window.addEventListener("message", event => {
        if (event.data && event.data.streamlitCloseModal) {
            // call Streamlit to set a small element we can detect (no direct)
            // we use window.location.reload() as fallback to close modal
            window.location.reload();
        }
    });
    </script>
    """, height=0)

# If no modal shown, show hint
if not st.session_state.show_modal:
    st.info("Click a country on the map (single click) to open the detailed popup.")
