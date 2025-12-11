import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------------------------------------------
# Page Setup
# ---------------------------------------------------
st.set_page_config(page_title="Country Dashboard", layout="wide")
st.title("📊 Country Insights Explorer")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
df = pd.read_csv("final_with_socio_cleaned.csv")

# Rename columns (UI friendly)
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

df = df.drop_duplicates(subset=["Country", "Year"])

# ---------------------------------------------------
# Filters
# ---------------------------------------------------
countries = sorted(df["Country"].unique())
years = sorted(df["Year"].unique())

selected_country = st.selectbox("🌍 Select Country", countries)

st.write("")  # GAP 1

selected_year = st.slider("📅 Select Year", int(min(years)), int(max(years)), int(max(years)))

st.write("")  # GAP 2

# Filter the row
row = df[(df["Country"] == selected_country) & (df["Year"] == selected_year)]
if row.empty:
    st.warning("⚠ No data for this year.")
    st.stop()

row = row.iloc[0]
country_data = df[df["Country"] == selected_country]

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.markdown(f"### 📍 {selected_country} — {selected_year}")

# ---------------------------------------------------
# Metric Cards
# ---------------------------------------------------
st.subheader("📌 Key Indicators")
st.write("")  # GAP 3

metric_cols = st.columns(4)

metrics = [
    ("GDP per Capita (USD)", "💵"),
    ("Life Expectancy", "👶"),
    ("Median Age (Medium)", "📈"),
    ("Population Density", "🌍"),
    ("PM2.5 (µg/m³)", "🌫️"),
    ("Health Insurance (%)", "🏥"),
    ("HDI", "📘"),
    ("Gini Index", "📊"),
]

for i, (m, icon) in enumerate(metrics):
    val = row.get(m, "NA")
    val = "No Data" if pd.isna(val) else round(val, 3)
    with metric_cols[i % 4]:
        st.metric(f"{icon} {m}", val)

# ---------------------------------------------------
# Stock-style Line Chart (Neon)
# ---------------------------------------------------
def stock_line_chart(df, y, title, color):
    fig = go.Figure()

    # Glow line
    fig.add_trace(go.Scatter(
        x=df["Year"], y=df[y], mode="lines",
        line=dict(width=10, color=color.replace("1)", "0.2)")),
        hoverinfo="skip", showlegend=False
    ))

    # Main neon line
    fig.add_trace(go.Scatter(
        x=df["Year"], y=df[y], mode="lines+markers",
        line=dict(width=3, color=color),
        hovertemplate="<b>Year %{x}</b><br>%{y}<extra></extra>"
    ))

    fig.update_layout(
        template="plotly_dark",
        title=title, height=420,
        plot_bgcolor="black", paper_bgcolor="black",
        xaxis=dict(showgrid=False, color="white"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", color="white"),
    )
    return fig

line_colors = [
    "rgba(0,255,255,1)",   # Cyan
    "rgba(255,0,255,1)",   # Pink
    "rgba(0,255,150,1)",   # Greenish teal
    "rgba(255,165,0,1)"    # Orange
]

# ---------------------------------------------------
# Trend Charts
# ---------------------------------------------------
st.subheader("📈 Historical Trends (Stock Style)")

trend_cols = st.columns(2)

with trend_cols[0]:
    st.plotly_chart(stock_line_chart(country_data, "GDP per Capita (USD)", "💵 GDP Trend", line_colors[0]), use_container_width=True)

with trend_cols[1]:
    st.plotly_chart(stock_line_chart(country_data, "Life Expectancy", "👶 Life Expectancy Trend", line_colors[1]), use_container_width=True)

with trend_cols[0]:
    st.plotly_chart(stock_line_chart(country_data, "PM2.5 (µg/m³)", "🌫️ PM2.5 Pollution Trend", line_colors[2]), use_container_width=True)

with trend_cols[1]:
    st.plotly_chart(stock_line_chart(country_data, "HDI", "📘 HDI Trend", line_colors[3]), use_container_width=True)

# ---------------------------------------------------
# Gradient Bar Charts
# ---------------------------------------------------
# ---------------------------------------------------
# Gradient Bar Charts (Expanded)
# ---------------------------------------------------
st.subheader("📊 Additional Visual Insights")

bar_charts = [
    ("COVID Cases", "🦠 COVID Cases Over Years", "Viridis"),
    ("Births", "👶 Births Over Years", "Plasma"),
    ("GDP per Capita (USD)", "💵 GDP per Capita Over Years", "Cividis"),
    ("Gini Index", "📊 Gini Index Over Years", "Turbo"),
    ("Health Insurance (%)", "🏥 Health Insurance Coverage", "Magma"),
    ("PM2.5 (µg/m³)", "🌫️ PM2.5 Air Pollution Over Years", "Inferno"),
]

for metric, title, gradient in bar_charts:
    if metric in country_data.columns:
        fig = px.bar(
            country_data,
            x="Year",
            y=metric,
            title=title,
            template="plotly_dark",
            color=metric,
            color_continuous_scale=gradient
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# --- COVID Chart: Filter from 2020 only ---
covid_data = country_data[country_data["Year"] >= 2020]

if not covid_data.empty:
    fig_covid = px.bar(
        covid_data,
        x="Year",
        y="COVID Cases",
        title="🦠 COVID Cases (2020 Onwards)",
        template="plotly_dark",
        color="COVID Cases",
        color_continuous_scale="Viridis"
    )
    fig_covid.update_layout(height=400)
    st.plotly_chart(fig_covid, use_container_width=True)

# ---------------------------------------------------
# Raw Data
# ---------------------------------------------------
st.markdown("### 🔍 Full Data for Selected Year")
st.dataframe(pd.DataFrame([row]))
