import streamlit as st
import pandas as pd
import plotly.express as px

# Set full width layout for a better dashboard experience
st.set_page_config(layout="wide", page_title="Country Zoom Dashboard")

st.title("Interactive World Map: Click to Zoom")

# Initialize session state for selected country if not already set
if 'selected_country_iso' not in st.session_state:
    st.session_state['selected_country_iso'] = None
if 'selected_country_name' not in st.session_state:
    st.session_state['selected_country_name'] = None
if 'selected_country_value' not in st.session_state:
    st.session_state['selected_country_value'] = None
if 'selected_country_img' not in st.session_state:
    st.session_state['selected_country_img'] = None


# Sample data including an extra country for variety
df = pd.DataFrame({
    "country": ["India", "United States", "China", "Brazil", "Germany"],
    "iso": ["IND", "USA", "CHN", "BRA", "DEU"],
    "value": [10, 25, 18, 5, 12], # Sample metric values
    "img": [
        "upload.wikimedia.org",
        "upload.wikimedia.org",
        "upload.wikimedia.org",
        "upload.wikimedia.org",
        "upload.wikimedia.org"
    ]
})

def update_selection(clicked_iso):
    """Callback function to update all session state variables."""
    # Retrieve all relevant data for the clicked ISO from the dataframe
    country_data = df[df['iso'] == clicked_iso].iloc[0] # Added .iloc[0] accessor
    
    st.session_state['selected_country_iso'] = clicked_iso
    st.session_state['selected_country_name'] = country_data['country']
    st.session_state['selected_country_value'] = country_data['value']
    st.session_state['selected_country_img'] = country_data['img']
    
    # Reruns the script to display the new sidebar content
    # st.rerun() # Removed rerun here, as on_select="rerun" already triggers it.

# --- Main Dashboard Layout ---

# Fixed: Use valid positive ratios for columns (60/40 split)
col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader("World Overview Map")

    # Create the main world choropleth map using Plotly
    fig = px.choropleth(
        df,
        locations="iso",
        color="value",
        hover_name="country",
        custom_data=["iso"], # Pass ISO code for identification after click
        color_continuous_scale="Viridis",
        title="Global Metrics"
    )

    fig.update_layout(
        geo=dict(
            showframe=False, 
            showcoastlines=True, 
            projection_type="equirectangular"
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=500
    )
    
    fig.update_traces(
        # Standard hover template for the world map
        hovertemplate="<b>%{hovertext}</b><br>Value: %{z}<extra></extra>"
    )

    # Display the map and capture the click event
    # `on_select="rerun"` makes the script re-execute instantly upon selection
    event_data = st.plotly_chart(
        fig, 
        use_container_width=True, 
        on_select="rerun", 
        selection_mode="points"
    )
    
    # Check if a selection event occurred (user clicked a point/country on the map)
    if event_data and event_data.get('selection'):
        # Get the selected points list
        points_data = event_data['selection']['points']
        if points_data:
            # Extract the ISO code from the *first* clicked point's custom data
            # points_data[0]['customdata'][0] extracts the value correctly
            clicked_iso = points_data[0]['customdata'][0]
            # Call the update function to handle state change
            update_selection(clicked_iso)

with col2:
    st.subheader("Country Focus View")
    
    if st.session_state['selected_country_iso']:
        # Filter dataframe for the selected country
        iso = st.session_state['selected_country_iso']
        name = st.session_state['selected_country_name']
        value = st.session_state['selected_country_value']
        img_url = st.session_state['selected_country_img']

        st.markdown(f"### {name}")
        st.image(img_url, width=100, caption=f"Flag of {name}")
        st.write(f"**Associated Value:** {value}")
        
        st.markdown("---")
        
        # Create a specific, zoomed map for only this country
        fig_zoom = px.choropleth(
            df[df['iso'] == iso],
            locations="iso",
            color="value",
            color_continuous_scale="Viridis",
            title=f"Zoomed view of {name}"
        )
        
        fig_zoom.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                # Automatically zoom to the selected country's bounds
                scope=iso.lower() 
            ),
            margin=dict(l=0, r=0, t=30, b=0),
            height=450
        )
        
        st.plotly_chart(fig_zoom, use_container_width=True)

    else:
        st.info("Click on a country in the map on the left to display its specific zoomed view and details here.")
