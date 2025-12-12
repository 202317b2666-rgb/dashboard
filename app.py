# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Figma Map Viewer", layout="wide")
st.title("Interactive World Map (Figma Embed)")

# Embed your Figma map
components.html("""
<iframe 
    style="border: 1px solid rgba(0, 0, 0, 0.1);" 
    width="1000" 
    height="600" 
    src="https://embed.figma.com/design/zqPLjtme3ls56S2vz9NR8z/Untitled?node-id=0-1&embed-host=share" 
    allowfullscreen>
</iframe>
""", height=620)
