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

# -----------------------------
# Rename columns for UI clarity
# -----------------------------
df = df.rename(columns={
    "Country": "Country",
    "ISO3": "ISO3",
    "Year": "Year",
    "GDP_per_capita": "GDP per Capita (USD)",
    "Gini_Index": "Gini Index",
    "Life_Expectancy": "Life Expectancy",
    "PM25": "PM2.5 (µg/m³)",
    "Health_Insurance": "Health Insurance (%)",
    "Median_Age_Est": "Median Age (Estimates)",
    "Median_Age_Mid": "Median Age (Medium)",
    "COVID_Deaths": "COVID Deaths",
    "COVID_Cases": "COVID Cases",
    "Population_Density": "Population Density",
    "Total_Population": "Total Population",
    "Male_Population": "Male Population",
    "Female_Population": "Female Population",
    "Births": "Births",
    "Deaths": "Deaths",
    "HDI": "HDI"
})

# Remove duplicates
df = df.drop_duplicates(subset=["Country", "Year"])

# -----------------------------
# Filters
# -----------------------------
countries = sorted(df["Country"].unique())
years = sorted(df["Year"].unique())

selected_country = st.selectbox("🌍 Select Country", countries)
selected_year = st.slider("📅 Select Year", int(min(years)), int(max(years)), int(max(years)))

# Filter selected row
row = df[(df["Country"] == selected_country) & (df["Year"] == selected_year)]

if row.empty:
    st.warning("⚠ No data available for this year.")
    st.stop()

row = row.iloc[0]

st.markdown(f"### 📍 {selected_country} — {selected_year}")

# -----------------------------
# Metric Cards
# -----------------------------
st.subheader("📌 Key Indicators")

metric_cols = st.columns(4)

metrics_to_show = [
    ("GDP per Capita (USD)", "💵"),
    ("Life Expectancy", "👶"),
    ("Median Age (Medium)", "📈"),
    ("Population Density", "🌍"),
    ("PM2.5 (µg/m³)", "🌫️"),
    ("Health Insurance (%)", "🏥"),
    ("HDI", "📘"),
    ("Gini Index", "📊"),
    ("COVID Deaths", "☠️"),
    ("COVID Cases", "🦠"),
]

for i, (metric, icon) in enumerate(metrics_to_show):
    value = row.get(metric, None)
    value = value if pd.notna(value) else "No Data"

    with metric_cols[i % 4]:
        st.metric(f"{icon} {metric}", value)

# -----------------------------
# Trends
# -----------------------------
st.subheader("📈 Historical Trends")
country_data = df[df["Country"] == selected_country]

def plot_trend(y_col, title):
    if y_col in country_data.columns:
        fig = px.line(country_data, x="Year", y=y_col, title=title, markers=True)
        st.plotly_chart(fig, use_container_width=True)

trend_cols = st.columns(2)

with trend_cols[0]:
    plot_trend("GDP per Capita (USD)", "GDP per Capita Over Years")

with trend_cols[1]:
    plot_trend("Life Expectancy", "Life Expectancy Over Time")

with trend_cols[0]:
    plot_trend("PM2.5 (µg/m³)", "PM2.5 Pollution Trend")

with trend_cols[1]:
    plot_trend("HDI", "HDI Trend Over Time")

# -----------------------------
# Raw Data
# -----------------------------
st.markdown("### 🔍 Full Data for Selected Year")
st.dataframe(pd.DataFrame([row]))
