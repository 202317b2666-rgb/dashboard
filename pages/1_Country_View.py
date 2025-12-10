import streamlit as st
import pandas as pd

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Country Wise Dashboard", layout="wide")
st.title("📊 Country Wise Insights Dashboard")

# -------------------------
# Load dataset
# -------------------------
metrics_df = pd.read_csv("final_with_socio.csv")

# Check required columns
required_cols = ["Entity", "Year"]
missing = [c for c in required_cols if c not in metrics_df.columns]
if missing:
    st.error(f"Missing columns in final_with_socio.csv: {missing}")
    st.stop()

# -------------------------
# Year slider
# -------------------------
years = sorted(metrics_df["Year"].unique())
selected_year = st.slider(
    "Select Year",
    min_value=int(min(years)),  # 1980
    max_value=int(max(years)),  # 2024
    value=int(max(years)),      # default 2024
)

# -------------------------
# Country dropdown
# -------------------------
countries = sorted(metrics_df["Entity"].unique())
selected_country = st.selectbox("Select Country", countries)

# -------------------------
# Filter data
# -------------------------
filtered = metrics_df[
    (metrics_df["Entity"] == selected_country) &
    (metrics_df["Year"] == selected_year)
]

st.subheader(f"📍 Country: {selected_country}")
st.subheader(f"📅 Year: {selected_year}")

if filtered.empty:
    st.warning("⚠ No data available for this country & year.")
else:
    st.success("Data loaded successfully!")

# -------------------------
# Display key metrics
# -------------------------
st.markdown("### 📌 Key Indicators")
cols = st.columns(2)

metric_list = [
    "GDP_per_capita",
    "HDI",
    "Period life expectancy at birth",
    "Median age - Sex: all - Age: all - Variant: estimates",
    "Population density",
    "Concentrations of fine particulate matter (PM2.5) - Residence area type: Total",
    "Share of population covered by health insurance (ILO (2014))",
    "Total_COVID_Deaths"
]

metric_labels = [
    "GDP per Capita (USD)",
    "Human Development Index (HDI)",
    "Life Expectancy at Birth",
    "Median Age",
    "Population Density",
    "PM2.5 (µg/m³)",
    "Health Insurance Coverage (%)",
    "Total COVID Deaths"
]

for i, metric in enumerate(metric_list):
    with cols[i % 2]:
        value = filtered.iloc[0][metric]
        st.metric(label=metric_labels[i], value=value)

# -------------------------
# Raw data display
# -------------------------
st.markdown("### 🔍 Raw Country Data")
st.dataframe(filtered)
