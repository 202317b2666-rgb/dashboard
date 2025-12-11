# ----------------------- COUNTRY VIEW PAGE -----------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title("🌍 Country View")

# Load datasets
hex_df = pd.read_csv("HEX.csv")

with open("countries.geo.json", "r") as f:
    geojson_data = json.load(f)

# ----------------------- COUNTRY SELECTION -----------------------
st.subheader("Select a Country")

if "country" not in hex_df.columns:
    st.error("❌ 'country' column not found in HEX.csv")
else:
    country_list = sorted(hex_df["country"].dropna().unique())
    selected_country = st.selectbox("Choose a Country", country_list)

    # Filter data
    country_data = hex_df[hex_df["country"] == selected_country]

    # ----------------------- COUNTRY DATA TABLE -----------------------
    st.subheader(f"📄 Data for {selected_country}")
    st.dataframe(country_data)

    # ----------------------- NUMERIC COLUMNS -----------------------
    numeric_columns = country_data.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if len(numeric_columns) == 0:
        st.warning("⚠ No numeric columns available for visualization.")
    else:
        # ----------------------- GRADIENT BAR CHART -----------------------
        st.subheader("📊 Gradient Bar Chart")

        bar_metric = st.selectbox(
            "Select a Metric for Bar Chart",
            numeric_columns,
            key="bar_metric"
        )

        fig_bar = px.bar(
            country_data,
            x="country",
            y=bar_metric,
            color=country_data[bar_metric],
            title=f"{bar_metric} for {selected_country}",
            color_continuous_scale="Viridis"  # gradient
        )

        fig_bar.update_layout(
            template="plotly_white",
            height=450,
            coloraxis_colorbar=dict(title="Value"),
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        # ----------------------- LINE CHART -----------------------
        st.subheader("📈 Line Chart Over Years")

        if "year" not in country_data.columns:
            st.warning("⚠ 'year' column missing. Cannot draw line chart.")
        else:
            line_metric = st.selectbox(
                "Select a Metric for Line Chart",
                numeric_columns,
                key="line_metric"
            )

            fig_line = px.line(
                country_data.sort_values("year"),
                x="year",
                y=line_metric,
                markers=True,
                title=f"{line_metric} Over Years — {selected_country}"
            )

            fig_line.update_layout(
                template="plotly_white",
                height=450
            )

            st.plotly_chart(fig_line, use_container_width=True)

    # ----------------------- HEX COLOR BOX -----------------------
    st.subheader("🎨 HEX Color for Map")

    if "hex" in country_data.columns:
        hex_color = country_data["hex"].iloc[0]
        st.markdown(
            f"""
            <div style="
                width:150px; height:150px; 
                background:{hex_color}; 
                border-radius:12px; 
                border:2px solid #333;
            "></div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("⚠ No HEX color available for this country.")
