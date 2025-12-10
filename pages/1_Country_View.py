import streamlit as st
import pandas as pd

st.set_page_config(page_title="Country Wise Dashboard", layout="wide")

st.title("📊 Country Wise Insights Dashboard")

# Load HEX dataset
hex_df = pd.read_csv("HEX.csv")

# Check required columns
required_cols = ["Country", "Year"]
missing = [c for c in required_cols if c not in hex_df.columns]
if missing:
    st.error(f"Missing columns in HEX.csv: {missing}")
    st.stop()

# -------------------------
# Year slider
# -------------------------
years = sorted(hex_df["Year"].unique())
selected_year = st.slider(
    "Select Year",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=int(max(years)),
)

# -------------------------
# Country dropdown
# -------------------------
countries = sorted(hex_df["Country"].unique())
selected_country = st.selectbox("Select Country", countries)

# -------------------------
# Filter data
# -------------------------
filtered = hex_df[
    (hex_df["Country"] == selected_country) &
    (hex_df["Year"] == selected_year)
]

st.subheader(f"📍 Country: {selected_country}")
st.subheader(f"📅 Year: {selected_year}")

if filtered.empty:
    st.warning("⚠ No data available for this country & year.")
else:
    st.success("Data loaded successfully!")

# -------------------------
# Dummy metrics (replace later)
# -------------------------
st.markdown("### 📌 Key Indicators (Prototype Values)")

dummy_metrics = {
    "GDP per capita": "₹ 75,000",
    "HDI": 0.71,
    "Life Expectancy": "70.5 yrs",
    "Median Age": "28.2 yrs",
    "Population Density": "432 / km²",
    "PM2.5 Pollution": 41.5,
    "Govt Effectiveness": -0.18,
    "COVID Deaths / million": 315,
}

cols = st.columns(2)
for i, (name, value) in enumerate(dummy_metrics.items()):
    with cols[i % 2]:
        st.metric(label=name, value=value)

# -------------------------
# Raw HEX data
# -------------------------
st.markdown("### 🔍 Raw HEX Data")
st.dataframe(filtered)
