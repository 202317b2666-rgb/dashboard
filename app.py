import streamlit as st
import pandas as pd
import plotly.express as px

st.title("World Map Dashboard")

# Sample country selection
country_selected = st.selectbox("Select Country", ["India", "USA", "China"])

# Simulate click → open modal
if st.button(f"Show {country_selected} Details"):
    with st.modal(f"{country_selected} Details"):
        st.subheader(f"{country_selected} Indicators")
        st.write("Population: 1.4B" if country_selected=="India" else "Population info")
        st.write("GDP: $3T" if country_selected=="India" else "GDP info")

        # Sample line chart
        df = pd.DataFrame({
            "Year": [2018, 2019, 2020, 2021, 2022],
            "GDP": [2.5, 2.7, 2.6, 3.0, 3.2] if country_selected=="India" else [21, 22, 20, 23, 24]
        })
        fig = px.line(df, x="Year", y="GDP", title=f"{country_selected} GDP Trend")
        st.plotly_chart(fig)
