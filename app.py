# app.py
import streamlit as st
import os

st.set_page_config(page_title="Interactive SVG World Map", layout="wide")

st.title("Interactive World Map with Hover & Click Effects")

# Load your SVG
svg_file = "Life.svg"  # <-- Replace with your SVG file name
if not os.path.exists(svg_file):
    st.error(f"{svg_file} not found! Please add your SVG to this folder.")
else:
    with open(svg_file, "r", encoding="utf-8") as f:
        svg_content = f.read()

# Embed SVG with JS for hover & click
svg_html = f"""
<style>
    svg path {{
        transition: all 0.2s ease;
        cursor: pointer;
    }}
    svg path:hover {{
        stroke: #FF0000;
        stroke-width: 3px;
        transform: scale(1.05);
    }}
    svg path.clicked {{
        stroke: #00FF00;
        stroke-width: 3px;
    }}
</style>

<div>
{svg_content}
</div>

<script>
const paths = document.querySelectorAll('svg path');

paths.forEach(path => {{
    path.addEventListener('click', () => {{
        paths.forEach(p => p.classList.remove('clicked'));  // remove from others
        path.classList.add('clicked');                     // highlight clicked
        console.log('Clicked country id:', path.id);      // shows country id in console
    }});
}});
</script>
"""

# Render in Streamlit
st.components.v1.html(svg_html, height=800, scrolling=True)
