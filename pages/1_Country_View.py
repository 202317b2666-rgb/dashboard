import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Country Dashboard", layout="wide")
st.title("📊 Country Insights Explorer")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("final_with_socio_cleaned.csv")

# Drop duplicates if any
df = df.drop_duplicates(subset=["Entity", "Year"])

# Rename columns for UI clarity
df = df.rename(columns={
    "Entity": "Country",
    "GDP_per_capita": "GDP per Capita (USD)",
    "Period life expectancy at birth": "Life Expectancy",
    "Population density": "Population Density",
    "Concentrations of fine particulate matter (PM2.5) - Residence area type: Total": "PM2.5",
    "Share of population covered by health insurance (ILO (2014))": "Health Insurance (%)",
    "Median age - Sex: all - Age: all - Variant: medium": "Median Age",
    "Total_COVID_Deaths": "COVID Deaths",
    "Total_COVID_Cases": "COVID Cases"
})

# -----------------------------
# Sidebar Filters
# -----------------------------
country_list = sorted(df["Country"].unique())
year_list = sorted(df["Year"].unique())

selected_country = st.selectbox("🌍 Select Country", country_list)
selected_year = st.slider("📅 Select Year", min(year_list), max(year_list), max(year_list))

# Filter for selected country & year
row = df[(df["Country"] == selected_country) & (df["Year"] == selected_year)]

st.markdown(f"### 📍 {selected_country} — {selected_year}")

if row.empty:
    st.warning("⚠ No data available for selected year.")
    st.stop()

data = row.iloc[0]

# -----------------------------
# Metric Cards
# -----------------------------
st.subheader("📌 Key Indicators")

metric_cols = st.columns(4)

metrics_to_show = {
    "GDP per Capita (USD)": "💵",
    "Life Expectancy": "👶",
    "Median Age": "📈",
    "Population Density": "🌏",
    "PM2.5": "🌫️",
    "Health Insurance (%)": "🏥",
    "HDI": "📘",
    "COVID Deaths": "☠️"
}

index = 0
for label, icon in metrics_to_show.items():
    with metric_cols[index % 4]:
        value = data[label] if pd.notna(data[label]) else "No data"
        st.metric(f"{icon} {label}", value)
    index += 1

# -----------------------------
# Trend Charts
# -----------------------------
st.subheader("📈 Historical Trends")

country_data = df[df["Country"] == selected_country]

chart_cols = st.columns(2)

# Chart 1 — GDP Trend
with chart_cols[0]:
    fig = px.line(country_data, x="Year", y="GDP per Capita (USD)", title="GDP per Capita Over Time")
    st.plotly_chart(fig, use_container_width=True)

# Chart 2 — Life Expectancy Trend
with chart_cols[1]:
    fig = px.line(country_data, x="Year", y="Life Expectancy", title="Life Expectancy Over Time")
    st.plotly_chart(fig, use_container_width=True)

# Chart 3 — PM2.5 Trend
with chart_cols[0]:
    fig = px.line(country_data, x="Year", y="PM2.5", title="PM2.5 Pollution Trend")
    st.plotly_chart(fig, use_container_width=True)

# Chart 4 — HDI Trend
with chart_cols[1]:
    fig = px.line(country_data, x="Year", y="HDI", title="HDI Trend")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Raw Data
# -----------------------------
st.markdown("### 🔍 Detailed Data")
st.dataframe(row)
