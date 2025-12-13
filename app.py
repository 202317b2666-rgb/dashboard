import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(layout="wide", page_title="Country Metrics Dashboard")
st.title("Interactive World Map with Country Details Popup")

# --- 1. Load Data ---

@st.cache_data
def load_data():
    """Load and merge all necessary data files."""
    
    # Assumes files are in the same directory as app.py or accessible online
    hex_path = "Hex.csv" 
    metrics_path = "country_metrics.csv"
    geojson_path = "country.geo.json"
    
    # Load DataFrames
    df_hex = pd.read_csv(hex_path)
    df_metrics = pd.read_csv(metrics_path)
    
    # Load GeoJSON data
    try:
        with open(geojson_path, 'r') as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        st.error(f"Error: {geojson_path} not found. Please check file paths.")
        st.stop()
        
    # Merge dataframes (ensure common key 'Country' or 'ISO' exists and is consistent)
    # Merging on 'Country' for the example metrics file structure
    merged_df = pd.merge(df_hex, df_metrics, on="Country", how="inner")
    
    return merged_df, geojson_data

df_merged, world_geojson = load_data()

# Ensure we have data to display, picking a default year if available
if not df_merged.empty:
    default_year = df_merged['Year'].max() # Latest year
    df_display = df_merged[df_merged['Year'] == default_year].copy()
else:
    st.error("No merged data available for display.")
    st.stop()

# --- 2. Define the Popup (Dialog) Function ---
@st.dialog("Country Details", width="medium")
def show_details_dialog(country_name, data_row_series):
    """
    Displays all indicator details for a selected country in a modal window.
    data_row_series is a single-row DataFrame slice or Series.
    """
    st.markdown(f"## {country_name}")

    # Use st.columns within the dialog for organized display of metrics
    colA, colB, colC = st.columns(3)
    
    # Displaying metrics using st.metric for clear visual indicators
    with colA:
        st.metric("GDP", f"${data_row_series['GDP'].iloc:,.0f}", delta_color="off")
        st.metric("Life Expectancy", f"{data_row_series['LifeExpectancy'].iloc} yrs", delta_color="off")
        
    with colB:
        st.metric("HDI", f"{data_row_series['HDI'].iloc:.2f}", delta_color="off")
        st.metric("Median Age", f"{data_row_series['MedianAge'].iloc} yrs", delta_color="off")

    with colC:
        st.metric("Pop. Density", f"{data_row_series['PopulationDensity'].iloc}", "per sq km")
        st.metric("PM25", f"{data_row_series['PM25'].iloc}", "avg exposure")

    st.markdown("---")
    st.write(f"**Government Effectiveness Score:** {data_row_series['GovernmentEffectiveness'].iloc}")
    st.write(f"**COVID Deaths Per Million:** {data_row_series['COVIDDeathsPerMillion'].iloc:,.0f}")
    
    if st.button("Close Window", key="close_dialog_button"):
        # st.rerun() closes the dialog and clears the event selection state
        st.rerun() 

# --- 3. Main Dashboard Layout and Map ---

st.subheader(f"Global Indicator Map (Year: {default_year})")

# Create the main world map
fig = px.choropleth(
    df_display,
    geojson=world_geojson,
    locations="iso_alpha",  # Match the ID field in the GeoJSON file
    color="GDP",            # Color the map by a primary indicator
    hover_name="Country",
    custom_data=["iso_alpha"], # Pass ISO code for identification after click
    color_continuous_scale="Viridis",
    scope="world",
    height=600,
    title="Color indicates GDP (Click for more details)"
)

fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>GDP: %{z}<extra>Click for details</extra>")


# Display the map and capture the click event using `on_select="rerun"`
event_data = st.plotly_chart(
    fig, 
    use_container_width=True, 
    on_select="rerun", 
    selection_mode="points" # Captures the specific country clicked
)

# --- 4. Handle Click Event and Show Dialog ---
if event_data and event_data.get('selection'):
    points_data = event_data['selection']['points']
    if points_data:
        # Get the ISO code from the clicked point
        clicked_iso = points_data['customdata']
        
        # Filter the dataframe for the *specific row* needed for the dialog
        country_data_row = df_display[df_display['iso_alpha'] == clicked_iso]

        # Check if we successfully found data and open the dialog
        if not country_data_row.empty:
            country_name = country_data_row['Country'].iloc
            # Pass the single-row dataframe slice to the dialog function
            show_details_dialog(country_name, country_data_row)
        else:
            st.warning("Data not found for the selected country in the current year.")

