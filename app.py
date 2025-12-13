import streamlit as st
import pandas as pd
import plotly.express as px

# Set full width layout for a better dashboard experience
st.set_page_config(layout="wide", page_title="Country Zoom Dashboard")

st.title("Interactive World Map: Click to Zoom")

# Initialize session state variables
if 'selected_country_iso' not in st.session_state:
    st.session_state['selected_country_iso'] = None
# ... other session state initializations ...


# Sample data
df = pd.DataFrame({
    "country": ["India", "United States", "China", "Brazil", "Germany"],
    "iso": ["IND", "USA", "CHN", "BRA", "DEU"],
    "value": [10, 50, 30, 20, 40], # Added values back in
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
    # Retrieve the ROW for the clicked ISO
    country_row = df[df['iso'] == clicked_iso].iloc[0] # <<--- Use .iloc[0] to get the single row

    st.session_state['selected_country_iso'] = clicked_iso
    # Access values directly from the single row object
    st.session_state['selected_country_name'] = country_row['country']
    st.session_state['selected_country_value'] = country_row['value']
    st.session_state['selected_country_img'] = country_row['img']
    
    # st.rerun() # on_select="rerun" handles the rerun


# --- Main Dashboard Layout ---
col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader("World Overview Map")

    fig = px.choropleth(
        df,
        locations="iso",
        color="value",
        hover_name="country",
        custom_data=["iso"], 
        color_continuous_scale="Viridis",
        title="Global Metrics"
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type="equirectangular"),
        margin=dict(l=0, r=0, t=30, b=0),
        height=500
    )
    
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Value: %{z}<extra></extra>")

    event_data = st.plotly_chart(
        fig, 
        use_container_width=True, 
        on_select="rerun", 
        selection_mode="points"
    )
    
    if event_data and event_data.get('selection'):
        points_data = event_data['selection']['points']
        if points_data:
            # Extract the ISO code (points_data['customdata'] is already a simple list/value)
            clicked_iso = points_data['customdata']
            update_selection(clicked_iso)

with col2:
    st.subheader("Country Focus View")
    
    if st.session_state['selected_country_iso']:
        # Retrieve simple string/int values from session state
        iso = st.session_state['selected_country_iso']
        name = st.session_state['selected_country_name']
        value = st.session_state['selected_country_value']
        img_url = st.session_state['selected_country_img'] # This is now guaranteed to be a single string

        st.markdown(f"### {name}")
        # The error occurred here, but is now fixed by ensuring img_url is a string
        st.image(img_url, width=100, caption=f"Flag of {name}") 
        st.write(f"**Associated Value:** {value}")
        
        st.markdown("---")
        
        # ... (rest of the zoom map code remains the same)
        fig_zoom = px.choropleth(
            df[df['iso'] == iso],
            locations="iso",
            color="value",
            color_continuous_scale="Viridis",
            title=f"Zoomed view of {name}"
        )
        # ... (update layout for fig_zoom)
        st.plotly_chart(fig_zoom, use_container_width=True)

    else:
        st.info("Click on a country in the map on the left to display its specific zoomed view and details here.")

