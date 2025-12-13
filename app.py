import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🌍 World Map – Pop-out on Click Simulation")

# ---------------- DATA ----------------
df = pd.DataFrame({
    "country": ["India", "United States", "Germany"],
    "iso_alpha": ["IND", "USA", "DEU"],
    "Life Expectancy": [69.7, 78.9, 81.1],
    "HDI": [0.633, 0.921, 0.942]
})

# ---------------- STATE ----------------
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

# ---------------- BASE MAP ----------------
base_fig = px.choropleth(
    df,
    locations="iso_alpha",
    color="Life Expectancy",
    hover_name="country",
    color_continuous_scale="Blues"
)

base_fig.update_layout(
    geo=dict(
        projection_type="natural earth",
        showcountries=True,
        countrycolor="white"
    ),
    height=420,
    margin=dict(l=0, r=0, t=0, b=0)
)

st.subheader("Base Map")
st.plotly_chart(base_fig, use_container_width=True)

# ---------------- TRIGGER ----------------
st.markdown("### 🔘 Click to Pop-out Map")
col1, col2, col3 = st.columns(3)

if col1.button("🇮🇳 India"):
    st.session_state.show_popup = True

if col2.button("🇺🇸 USA"):
    st.session_state.show_popup = True

if col3.button("🇩🇪 Germany"):
    st.session_state.show_popup = True

# ---------------- POP-OUT MAP ----------------
if st.session_state.show_popup:
    st.markdown("---")
    st.subheader("🔍 Focus View (Pop-out)")

    popup_fig = px.choropleth(
        df,
        locations="iso_alpha",
        color="Life Expectancy",
        hover_name="country",
        color_continuous_scale="Blues"
    )

    popup_fig.update_layout(
        geo=dict(
            projection_type="natural earth",
            showcountries=True,
            countrycolor="black"
        ),
        height=600,   # 👈 bigger = pop-out feel
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(popup_fig, use_container_width=True)

    if st.button("❌ Close"):
        st.session_state.show_popup = False
