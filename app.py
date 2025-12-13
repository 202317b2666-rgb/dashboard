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

# Render the map ONLY ONCE
st.plotly_chart(fig, use_container_width=True)

# Temporary workaround: simulate click with selectbox
country_selected = st.selectbox("Simulate click country", map_df["country"])

# Button triggers popup modal
if st.button(f"Show Popup for {country_selected}"):
    with st.modal(f"{country_selected} Popup"):
        st.write("This is your floating popup!")
        st.write("You can later add charts/indicators here.")
