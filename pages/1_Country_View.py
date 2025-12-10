import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Country Dashboard", layout="wide")
st.title("📊 Country Insights Explorer")

# -----------------------------
# Theme Toggle (Dark/Light)
# -----------------------------
mode = st.radio("🌗 Select Theme:", ["Light Mode", "Dark Mode"])
if mode == "Dark Mode":
    bg_color = "black"
    font_color = "white"
else:
    bg_color = "white"
    font_color = "black"

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
# Line Chart (Stock Market Style)
# -----------------------------
st.subheader("📈 Historical Trends (Stock Market Style)")

def stock_style_line(x, y, title, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color=color, width=2)))
    fig.update_layout(
        title=dict(text=title, font=dict(color=font_color)),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=font_color),
        xaxis=dict(showgrid=False, color=font_color),
        yaxis=dict(showgrid=False, color=font_color),
    )
    return fig

country_data = df[df["Country"] == selected_country]

# Only for columns with numeric data
line_charts = [
    ("GDP per Capita (USD)", "cyan"),
    ("Life Expectancy", "red"),
    ("HDI", "yellow"),
]

line_cols = st.columns(2)
for i, (col_name, color) in enumerate(line_charts):
    fig = stock_style_line(country_data["Year"], country_data[col_name], col_name, color)
    with line_cols[i % 2]:
        st.plotly_chart(fig, use_container_width=True)

# Multi-Line Chart
fig_multi = go.Figure()
for col_name, color in line_charts:
    fig_multi.add_trace(go.Scatter(x=country_data["Year"], y=country_data[col_name], mode="lines", name=col_name, line=dict(color=color, width=2)))

fig_multi.update_layout(
    title=dict(text="Combined Multi-Line Trends", font=dict(color=font_color)),
    plot_bgcolor=bg_color,
    paper_bgcolor=bg_color,
    font=dict(color=font_color),
    xaxis=dict(showgrid=False, color=font_color),
    yaxis=dict(showgrid=False, color=font_color),
)

st.plotly_chart(fig_multi, use_container_width=True)

# -----------------------------
# COVID Chart (from first available year)
# -----------------------------
st.subheader("🦠 COVID Trends")

covid_data = country_data.dropna(subset=["COVID_Deaths", "COVID_Cases"])
if not covid_data.empty:
    covid_data = covid_data[covid_data["Year"] >= 2020]
    fig_covid = px.bar(
        covid_data,
        x="Year",
        y=["COVID_Deaths", "COVID_Cases"],
        barmode="group",
        title="COVID Deaths & Cases",
        text_auto=True
    )
    fig_covid.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=font_color)
    )
    st.plotly_chart(fig_covid, use_container_width=True)

# -----------------------------
# Raw Data
# -----------------------------
st.subheader("🔍 Full Data for Selected Year")
st.dataframe(pd.DataFrame([row]))
