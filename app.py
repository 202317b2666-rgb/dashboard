import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os # Helps with local file paths

st.set_page_config(layout="wide", page_title="Country Metrics Dashboard")
st.title("Interactive World Map with Country Details Popup")

# --- 1. Load Data ---

@st.cache_data
def load_data():
    """Load and merge all necessary data files."""
    
    # Define file paths (adjust if your files are in subdirectories or online URLs)
    hex_path = "Hex.csv" 
    metrics_path = "country_metrics.csv"
    geojson_path = "country.geo.json"
    
    # Load DataFrames
    df_hex = pd.read_csv(hex_path)
    df_metrics = pd.read_csv(metrics_path)
    
    # Load GeoJSON data
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
        
    # Merge dataframes on ISO code/Country name (requires cleaning/standardizing names if needed)
    # Assuming 'iso_alpha' in Hex.csv corresponds to 'id' in GeoJSON and 'Country' needs mapping if different
    # For this example, let's merge metrics onto the hex data using 'Country' column (may need careful alignment in real data)
    merged_df = pd.merge(df_hex, df_metrics, on="Country", how="inner")
    
    return merged_df, geojson_data

df_merged, world_geojson = load_data()

# Ensure we are using 2021 data for a consistent map view as an example
df_display = df_merged[df_merged['Year'] == 2021]

# --- 2. Define the Popup (Dialog) Function ---

@st.dialog("Country Details", width="small")
def show_details_dialog(country_name, data_row):
    st.markdown(f"## {country_name}")
    
    # Display the flag (assuming an 'img' column or similar URL can be added to the DF)
    # Since your provided CSVs don't have an 'img' URL, we'll skip the flag image for now.

    st.markdown("**Key Metrics (2021 Data):**")
    st.markdown(f"* **GDP (per capita):** ${data_row['GDP'].iloc[0]:,.0f}")
    st.markdown(f"* **HDI:** {data_row['HDI'].iloc[0]:.2f}")
    st.markdown(f"* **Life Expectancy:** {data_row['LifeExpectancy'].iloc[0]} years")
    st.markdown(f"* **Population Density:** {data_row['PopulationDensity'].iloc[0]} per sq km")
    st.markdown(f"* **COVID Deaths/Million:** {data_row['COVIDDeathsPerMillion'].iloc[0]:,.0f}")

    if st.button("Close"):
        st.session_state['selected_country_iso'] = None # Clear selection on close
        st.rerun() # Closes the dialog by rerunning the main script

# --- 3. Main Dashboard Layout and Map ---

st.subheader("Global GDP Distribution (2021)")

# Create the main world map
fig = px.choropleth(
    df_display,
    geojson=world_geojson,
    locations="iso_alpha",  # Match the ID field in the GeoJSON file
    color="GDP",            # Color the map by GDP
    hover_name="Country",
    custom_data=["iso_alpha"],
    color_continuous_scale="Plasma",
    scope="world",
    height=600
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Display the map and capture the click event using `on_select`
event_data = st.plotly_chart(
    fig, 
    use_container_width=True, 
    on_select="rerun", 
    selection_mode="points" # Captures the specific country clicked
)

# --- 4. Handle Click Event and Show Dialog ---

# Check if a selection event occurred
if event_data and event_data.get('selection'):
    points_data = event_data['selection']['points']
    if points_data:
        # Get the ISO code from the *first* clicked point
        clicked_iso = points_data[0]['customdata'][0]
        
        # Filter the full dataframe (not just the display one) for the clicked country
        # This makes sure we have all metrics for that specific country across all years if needed
        country_data_filtered = df_merged[df_merged['iso_alpha'] == clicked_iso]

        # Use the st.dialog function to open the modal window with the data
        if not country_data_filtered.empty:
            country_name = country_data_filtered.iloc[0]['Country']
            # Pass the filtered data row to the dialog function
            show_details_dialog(country_name, country_data_filtered)
        else:
            st.warning("Data not found for the selected country.")

