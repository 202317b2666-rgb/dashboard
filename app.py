import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Interactive World Map - Click to show popup")

# Sample country data
map_df = pd.DataFrame({
    "lat": [21, 37, 35],
    "lon": [78, -95, 103],
    "country": ["India", "USA", "China"]
})

# Plotly scatter geo map
fig = px.scatter_geo(map_df, lat="lat", lon="lon", hover_name="country", projection="natural earth")
map_chart = st.plotly_chart(fig, use_container_width=True)

# Capture click
clicked_country = st.session_state.get("clicked_country", None)

# Add JS handler to set clicked country
clicked = st.plotly_chart(fig, use_container_width=True)
click_data = st.session_state.get("click_data", None)

# Since Streamlit can't directly catch plotly click in Python, 
# simulate with a selectbox for now (replace later with Dash or JS callback)
country_selected = st.selectbox("Simulate click country", map_df["country"])

if st.button(f"Show Popup for {country_selected}"):
    with st.modal(f"{country_selected} Popup"):
        st.write("This is your floating popup!")
        st.write("You can later add charts/indicators here.")
