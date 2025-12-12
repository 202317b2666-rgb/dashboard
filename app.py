# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events
import json

st.set_page_config(layout="wide")
st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click any country on the map to open the detailed popup window.")

# ---- Load data ----
hex_df = pd.read_csv("Hex.csv")
hex_df.columns = hex_df.columns.str.strip()
hex_df['iso_alpha'] = hex_df['iso_alpha'].astype(str).str.upper().str.strip()
hex_df['country'] = hex_df['country'].astype(str).str.strip()

with open("countries.geo.json") as f:
    geojson = json.load(f)

df = pd.read_csv("final_with_socio_cleaned.csv")
df.columns = df.columns.str.strip()
df['ISO3'] = df['ISO3'].astype(str).str.upper().str.strip()

# ---- Build map ----
fig = px.choropleth(
    hex_df,
    geojson=geojson,
    locations='iso_alpha',
    color='hex',
    hover_name='country',
    featureidkey="id",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(r=0, t=0, l=0, b=0), height=600)

# ---- Capture click event (single map) ----
clicked = plotly_events(fig, click_event=True, hover_event=False)

# Helper to open modal
def show_modal(country_name, country_data):
    st.markdown("""
    <style>
    .modal-bg { position: fixed; top:0; left:0; width:100%; height:100%; backdrop-filter: blur(5px);
                background-color: rgba(0,0,0,0.45); z-index: 999; }
    .modal-box { position: fixed; top:4%; left:6%; width:88%; height:92%; background:white;
                 padding:18px; border-radius:12px; overflow-y: auto; z-index:1000; }
    .close-btn { float: right; background:#e74c3c; color:white; padding:6px 10px; border-radius:6px; text-decoration:none; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="modal-bg"></div><div class="modal-box">', unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col1:
        st.header(f"{country_name} — Detailed Indicators")
    with col2:
        if st.button("Close"):
            st.experimental_rerun()

    if country_data.empty:
        st.warning("No socio-economic data available for this country.")
    else:
        # Example charts (add/remove as needed)
        st.subheader("Trends")
        st.plotly_chart(px.line(country_data, x="Year", y="GDP_per_capita", title="GDP per Capita"), use_container_width=True)
        st.plotly_chart(px.line(country_data, x="Year", y="HDI", title="Human Development Index"), use_container_width=True)
        st.plotly_chart(px.line(country_data, x="Year", y="Life_Expectancy", title="Life Expectancy"), use_container_width=True)
        st.plotly_chart(px.line(country_data, x="Year", y="Gini_Index", title="Gini Index"), use_container_width=True)
        st.plotly_chart(px.line(country_data, x="Year", y="PM25", title="Air Pollution (PM2.5)"), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---- Interpret click payload robustly ----
if clicked:
    info = clicked[0]  # dict with event details
    # try several possible keys
    iso_clicked = None
    country_clicked = None

    # Common: choropleth returns 'location' (the iso code)
    if 'location' in info and info['location']:
        iso_clicked = info['location']

    # Some Plotly versions return hovertext or text with country name
    if not iso_clicked:
        if 'hovertext' in info and info['hovertext']:
            country_clicked = info['hovertext']
        elif 'text' in info and info['text']:
            country_clicked = info['text']

    # customdata sometimes contains arrays you set - try to extract iso if present
    if not iso_clicked and 'customdata' in info and info['customdata']:
        # attempt common positions
        cd = info['customdata']
        if isinstance(cd, (list, tuple)) and len(cd) > 0:
            # try to find an entry that looks like ISO3 (3 letters)
            for entry in cd:
                if isinstance(entry, str) and len(entry) == 3:
                    iso_clicked = entry.upper()
                    break

    # Map iso -> country if iso known
    if iso_clicked:
        row = hex_df[hex_df['iso_alpha'] == iso_clicked]
        if not row.empty:
            country_clicked = row.iloc[0]['country']
    # If still unknown, show debug info
    if not country_clicked:
        st.error("Could not determine clicked country from the event payload. Showing payload keys to help debug.")
        st.write("Event payload keys:", list(info.keys()))
        st.write("Full payload (first item):", info)
    else:
        iso3 = hex_df.loc[hex_df['country'] == country_clicked, 'iso_alpha'].values[0]
        country_data = df[df['ISO3'] == iso3].sort_values('Year')
        show_modal(country_clicked, country_data)
else:
    st.info("Click a country on the map to open the detailed popup.")
