# app.py
# Streamlit + Plotly world map with hover highlight and click -> modal popup
# Uses files (place in same folder):
#   - HEX.csv
#   - countries.geo.json
#   - final_with_socio_cleaned.csv  <-- your merged dataset (confirmed)
#
# Required: pip install -r requirements.txt
import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide", page_title="World Map — Country Details (Popup)")

# ---------- Filenames ----------
HEX_CSV = "HEX.csv"
GEOJSON = "countries.geo.json"
MASTER_CSV = "final_with_socio_cleaned.csv"  # your merged dataset

# ---------- Utilities to load files ----------
@st.cache_data
def load_geojson(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_hex(path):
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

@st.cache_data
def load_master(path):
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            return df
        except Exception:
            return None
    return None

geojson = load_geojson(GEOJSON)
hex_df = load_hex(HEX_CSV)
master_df = load_master(MASTER_CSV)

# ---------- Basic checks ----------
if geojson is None:
    st.error(f"Missing or invalid geojson file: {GEOJSON}. Add it to the repo and try again.")
    st.stop()

if master_df is None:
    st.warning(f"Master CSV not found: {MASTER_CSV}. The app will still show the map but popup charts require the master CSV.")
else:
    # normalize column names
    master_df.columns = master_df.columns.str.strip()
    # attempt to standardize ISO3 column to 'iso_alpha'
    if "iso_alpha" not in master_df.columns:
        for alt in ["ISO_A3","ISO3","iso3","Country Code","ISO3_code","country_code","ISO_A3_CODE","iso_a3"]:
            if alt in master_df.columns:
                master_df = master_df.rename(columns={alt: "iso_alpha"})
                break
    # standardize Year col
    if "Year" not in master_df.columns:
        for alt in ["year","TIME","time"]:
            if alt in master_df.columns:
                master_df = master_df.rename(columns={alt: "Year"})
                break

# ---------- Determine featureidkey for geojson (where ISO3 lives) ----------
# Common places: feature['id'] or feature['properties']['ISO_A3'] / ['iso_a3'] / ['ISO3']
featureidkey = None
first_feature = geojson.get("features", [None])[0]
if first_feature is not None:
    # if features have top-level id
    if "id" in first_feature and first_feature["id"]:
        featureidkey = "id"
    else:
        props = first_feature.get("properties", {})
        for k in ["ISO_A3", "ISO3", "iso_a3", "iso3", "ADM0_A3", "ISO_A3E"]:
            if k in props:
                featureidkey = f"properties.{k}"
                break

# If we still don't have featureidkey, default to properties.ADM0_A3 (common)
if featureidkey is None:
    featureidkey = "properties.ADM0_A3"

# ---------- Helper to get latest snapshot for map colors ----------
def get_latest_snapshot(df):
    if df is None or "Year" not in df.columns:
        return df
    try:
        latest = int(df["Year"].max())
        return df[df["Year"] == latest]
    except Exception:
        return df

snapshot = get_latest_snapshot(master_df)

# ---------- Resolve metric column names (try common alias list) ----------
METRIC_ALIASES = {
    "GDP_per_capita": ["GDP_per_capita", "GDP per capita", "gdp_per_capita", "GDP_per_capita (current US$)"],
    "Life_expectancy": ["Life_expectancy", "Life expectancy", "Life expectancy at birth", "life_expectancy"],
    "Population_density": ["Population_density", "Population density", "PopDensity", "pop_density"],
    "Covid_cases_per_mil": ["Covid_cases_per_mil", "total_covid_cases_per_mil", "Total COVID Cases per mil", "covid_cases_per_mil"],
    "Covid_deaths_per_mil": ["Covid_deaths_per_mil", "total_covid_deaths_per_mil", "Total COVID Deaths per mil", "covid_deaths_per_mil"],
    "HDI": ["HDI", "Human Development Index", "hdi"],
    "GiniIndex": ["GiniIndex", "Gini", "gini_index", "Gini Index"],
    "Govt_Effectiveness": ["Govt_Effectiveness", "Govt Effectiveness Index", "Govt Effectiveness Index", "Govt_Effectiveness_Index"],
    "Median_Age": ["MedianAge","Median Age","median_age"],
    "Dependency_Ratio": ["Dependency Ratio", "Dependency_Ratio", "DependencyRatio"]
}

def find_col(df, aliases):
    if df is None:
        return None
    for a in aliases:
        if a in df.columns:
            return a
    return None

resolved = {}
for k, aliases in METRIC_ALIASES.items():
    resolved[k] = find_col(master_df, aliases) if master_df is not None else None

# fallback color metric for map
color_col = resolved.get("GDP_per_capita") or resolved.get("Life_expectancy") or resolved.get("Population_density")

# ---------- Build the map figure ----------
st.markdown("# World Map — Click a country to open details")

col_map, col_controls = st.columns([3, 1])
with col_map:
    if snapshot is None or snapshot.empty:
        # show plain choropleth with geojson only
        fig = px.choropleth_mapbox(
            pd.DataFrame({"dummy": []}),
            geojson=geojson,
            locations=[],
            center={"lat": 0, "lon": 0},
            zoom=0.8,
            mapbox_style="carto-positron",
            title="World map (no snapshot data)"
        )
        st.info("No snapshot data found in master CSV for the latest year. Add final_with_socio_cleaned.csv to enable map coloring.")
    else:
        plot_df = snapshot.copy()
        # merge HEX colors if provided
        if not hex_df.empty and "iso_alpha" in hex_df.columns and "iso_alpha" in plot_df.columns:
            plot_df = plot_df.merge(hex_df[["iso_alpha", "hex"]], on="iso_alpha", how="left")
        # create choropleth
        if color_col and color_col in plot_df.columns:
            fig = px.choropleth(
                plot_df,
                geojson=geojson,
                locations="iso_alpha",
                color=color_col,
                featureidkey=featureidkey,
                hover_name="Country Name" if "Country Name" in plot_df.columns else "iso_alpha",
                hover_data={color_col: True, "iso_alpha": False},
                projection="natural earth",
                title=f"World map — {int(plot_df['Year'].max())}"
            )
        else:
            fig = px.choropleth(
                plot_df,
                geojson=geojson,
                locations="iso_alpha",
                featureidkey=featureidkey,
                hover_name="Country Name" if "Country Name" in plot_df.columns else "iso_alpha",
                projection="natural earth",
                title="World map (snapshot)"
            )
    # layout tweaks
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, clickmode="event+select", height=720)
    # capture click events
    clicked = plotly_events(fig, click_event=True, hover_event=False, key="world_map_events")

with col_controls:
    st.markdown("### Controls")
    st.write("Hover shows preview. Click a country to open a popup with time-series and details.")
    if os.path.exists(MASTER_CSV):
        st.write(f"Data: {MASTER_CSV}")
    else:
        st.write("Data: (master CSV not found)")

# ---------- If a click event happened, open the modal popup ----------
clicked_iso = None
if clicked:
    try:
        evt = clicked[0]
        clicked_iso = evt.get("location") or evt.get("properties", {}).get("location") or None
    except Exception:
        clicked_iso = None

if clicked_iso:
    # find country rows in master_df
    country_rows = None
    if master_df is not None and "iso_alpha" in master_df.columns:
        country_rows = master_df[master_df["iso_alpha"] == clicked_iso]

    # determine country display name
    display_name = clicked_iso
    if country_rows is not None and not country_rows.empty:
        if "Country Name" in country_rows.columns:
            display_name = country_rows["Country Name"].iloc[0]
        elif "Country" in country_rows.columns:
            display_name = country_rows["Country"].iloc[0]

    # open modal popup
    with st.modal(f"{display_name} — Details", expanded=True):
        left, right = st.columns([1, 2])
        with left:
            st.markdown(f"### {display_name}")
            st.markdown(f"**ISO3:** {clicked_iso}")
            # small zoomed map
            try:
                mini_df = snapshot.copy() if (snapshot is not None) else pd.DataFrame()
                mini_df = mini_df[mini_df.get("iso_alpha") == clicked_iso]
                if mini_df is None or mini_df.empty:
                    st.info("No snapshot available for mini map.")
                else:
                    mini_map = px.choropleth(mini_df, geojson=geojson, locations="iso_alpha",
                                            featureidkey=featureidkey,
                                            color=color_col if (color_col in mini_df.columns) else None,
                                            projection="natural earth")
                    mini_map.update_geos(fitbounds="locations", visible=False)
                    mini_map.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=240)
                    st.plotly_chart(mini_map, use_container_width=True)
            except Exception as e:
                st.info("Mini-map render issue: " + str(e))

            # show latest values (if available)
            if country_rows is not None and not country_rows.empty:
                latest_row = country_rows.sort_values("Year", ascending=False).iloc[0]
                st.markdown("### Latest values")
                for key, col in resolved.items():
                    if col and col in latest_row.index:
                        val = latest_row[col]
                        st.write(f"**{key.replace('_', ' ')}:** {val}")

        with right:
            if master_df is None or "Year" not in master_df.columns:
                st.info("No time-series master CSV found. Add final_with_socio_cleaned.csv with time-series data to enable charts.")
            else:
                years = sorted(master_df["Year"].dropna().unique().astype(int).tolist())
                min_y, max_y = years[0], years[-1]
                yr_range = st.slider("Select year range", min_y, max_y, (min_y, max_y))

                # filter for country + year range
                ts = master_df[(master_df["iso_alpha"] == clicked_iso) & (master_df["Year"].between(yr_range[0], yr_range[1]))].sort_values("Year")
                if ts.empty:
                    st.info("No time-series rows for this country in selected range.")
                else:
                    # plotting helper
                    def plot_ts(column, title):
                        try:
                            fig = px.line(ts, x="Year", y=column, markers=True, title=title)
                            fig.update_layout(margin={"r":10,"t":30,"l":0,"b":0}, height=220)
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.info(f"Could not plot {title}: {e}")

                    # order of charts to render
                    chart_order = [
                        ("GDP_per_capita", resolved.get("GDP_per_capita")),
                        ("Life expectancy", resolved.get("Life_expectancy")),
                        ("Population density", resolved.get("Population_density")),
                        ("COVID cases per mil", resolved.get("Covid_cases_per_mil")),
                        ("COVID deaths per mil", resolved.get("Covid_deaths_per_mil")),
                        ("HDI", resolved.get("HDI")),
                        ("Gini index", resolved.get("GiniIndex")),
                        ("Govt effectiveness", resolved.get("Govt_Effectiveness")),
                        ("Median age", resolved.get("Median_Age")),
                        ("Dependency ratio", resolved.get("Dependency_Ratio")),
                    ]
                    for title, col in chart_order:
                        if col and col in ts.columns:
                            plot_ts(col, title)

        st.divider()
        st.write("Close popup to go back to the map.")

st.caption("Tip: Hover on countries for quick preview. Click to open detailed popup. Files expected: HEX.csv, countries.geo.json, final_with_socio_cleaned.csv")
