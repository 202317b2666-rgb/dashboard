import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Interactive World Map Dashboard")

# Initialize session state for selected country if not already set
if 'selected_country_iso' not in st.session_state:
    st.session_state['selected_country_iso'] = None

# Sample data for 3 countries
df = pd.DataFrame({
    "country": ["India", "United States", "China"],
    "iso": ["IND", "USA", "CHN"],
    "value": [1, 2, 3],
    "img": [
        "https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
        "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_China.svg"
    ]
})

def update_selection(selected_iso):
    """Callback function to update the selected country in the session state."""
    st.session_state['selected_country_iso'] = selected_iso
    st.rerun() # Reruns the script to display the new sidebar content

# --- Main Dashboard Layout ---

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("World Map Overview")
    # Create choropleth map using Plotly
    fig = px.choropleth(
        df,
        locations="iso",
        color="value",
        hover_name="country",
        custom_data=["iso"], # Use ISO in custom data for the click event
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False, projection_type="equirectangular"),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    # Display the map using st.plotly_chart and configure the click event handling
    # Streamlit automatically handles the click event with the selection parameter
    event_data = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
    
    # Check if a selection event occurred (user clicked a point on the map)
    if event_data and event_data.get('selection'):
        points = event_data['selection']['points']
        if points:
            # Extract the ISO code from the custom_data of the clicked point
            # custom_data is a list: custom_data=[iso, ...] -> points[0]['customdata'][0]
            clicked_iso = points[0]['customdata'][0] 
            # Call the update function to handle state change
            update_selection(clicked_iso)

with col2:
    st.subheader("Selected Country Details")
    
    if st.session_state['selected_country_iso']:
        # Filter dataframe for the selected country
        selected_iso = st.session_state['selected_country_iso']
        country_data = df[df['iso'] == selected_iso].iloc[0]

        st.markdown(f"### {country_data['country']}")
        st.image(country_data['img'], width=150)
        st.write(f"**Data Value:** {country_data['value']}")

        # Optional: Add a specific map for just this country
        st.markdown("---")
        st.write("Zoomed Map View:")
        fig_zoom = px.choropleth(
            df[df['iso'] == selected_iso],
            locations="iso",
            color="value",
            color_continuous_scale="Blues"
        )
        fig_zoom.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=False,
                # Automatically zoom to the selected country's bounds
                scope=selected_iso.lower() 
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )
        st.plotly_chart(fig_zoom, use_container_width=True)

    else:
        st.info("Click on a country in the map to see details here.")

