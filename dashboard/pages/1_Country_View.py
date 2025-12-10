import streamlit as st
import pandas as pd

st.set_page_config(page_title="Country Wise Dashboard", layout="wide")
st.title("📊 Country Wise Insights Dashboard")

# Load the new merged CSV
metrics_df = pd.read_csv("pages/final_with_socio.csv")

# Rename columns to make them consistent with code (optional)
metrics_df = metrics_df.rename(columns={
    'Entity': 'Country',
    'Period life expectancy at birth': 'LifeExpectancy',
    'Concentrations of fine particulate matter (PM2.5) - Residence area type: Total': 'PM25',
    'Share of population covered by health insurance (ILO (2014))': 'HealthCoverage',
    'Median age - Sex: all - Age: all - Variant: medium': 'MedianAge',
    'Total_COVID_Deaths': 'COVIDDeathsPerMillion',
    'GDP_per_capita': 'GDP',
    'Population density': 'PopulationDensity',
    'HDI': 'HDI'
})

# -------------------------
# Year slider (1980-2024)
# -------------------------
selected_year = st.slider(
    "Select Year",
    min_value=1980,
    max_value=2024,
    value=2024
)

# -------------------------
# Country dropdown
# -------------------------
countries = sorted(metrics_df["Country"].unique())
selected_country = st.selectbox("Select Country", countries)

# -------------------------
# Filter data
# -------------------------
filtered = metrics_df[
    (metrics_df["Country"] == selected_country) &
    (metrics_df["Year"] == selected_year)
]

st.subheader(f"📍 Country: {selected_country}")
st.subheader(f"📅 Year: {selected_year}")

if filtered.empty:
    st.warning("⚠ No data available for this country & year.")
else:
    st.success("Data loaded successfully!")

# -------------------------
# Display metrics
# -------------------------
st.markdown("### 📌 Key Indicators")
cols = st.columns(2)
metric_list = ["GDP", "HDI", "LifeExpectancy", "MedianAge",
               "PopulationDensity", "PM25", "HealthCoverage", "COVIDDeathsPerMillion"]

for i, metric in enumerate(metric_list):
    with cols[i % 2]:
        value = filtered.iloc[0][metric]
        st.metric(label=metric, value=value)

# -------------------------
# Raw data
# -------------------------
st.markdown("### 🔍 Raw Country Data")
st.dataframe(filtered)
