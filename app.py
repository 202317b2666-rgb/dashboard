import streamlit as st

st.set_page_config(layout="wide")
st.title("World Map Dashboard (Streamlit + Embedded Dash)")

st.write("Interactive world map with popups powered by Dash:")

# Embed the Dash app using an iframe
st.components.v1.iframe(
    src="https://dashboard-3-rjwo.onrender.com/",
    height=800,   # adjust height as needed
    scrolling=True,
    width=1200
)
