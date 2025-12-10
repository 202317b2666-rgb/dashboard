import streamlit as st
import pandas as pd

st.set_page_config(page_title="Country Wise Dashboard", layout="wide")
st.title("📊 Country Wise Insights Dashboard")

# Load the metrics CSV (for country view)
metrics_df = pd.read_csv("country_metrics.csv")

# Check required columns
required_cols = ["Country", "Year"]
missing = [c for c in required_cols if c not in metrics_df.columns]
if missing:
    st.error(f"Missing columns in country_metrics.csv: {missing}")
    st.stop()

# -------------------------
# Year slider
# -------------------------
years = sorted(metrics_df["Year"].unique())
selected_year = st.slider(
    "Select Year",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=int(max(years)),
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
               "PopulationDensity", "PM25", "GovernmentEffectiveness", "COVIDDeathsPerMillion"]

for i, metric in enumerate(metric_list):
    with cols[i % 2]:
        value = filtered.iloc[0][metric]
        st.metric(label=metric, value=value)

# -------------------------
# Raw data
# -------------------------
st.markdown("### 🔍 Raw Country Data")
st.dataframe(filtered)
