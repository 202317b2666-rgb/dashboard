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
selected_year = st.slider("📅 Select Year", int(min(years)), int(max(years)), int(max(years)))

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
# Premium Stock-Market Style Line Chart
# ---------------------------------------------------
def stock_line_chart(df, y, title):
    fig = go.Figure()

    # Glow line
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df[y],
        mode="lines",
        line=dict(width=10, color="rgba(0, 255, 255, 0.2)"),
        hoverinfo="skip",
        showlegend=False
    ))

    # Neon line
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df[y],
        mode="lines",
        line=dict(width=3, color="#00FFFF"),
        hovertemplate="<b>Year %{x}</b><br>%{y}<extra></extra>",
        name=title
    ))

    fig.update_layout(
        template="plotly_dark",
        title=title,
        height=420,
        plot_bgcolor="black",
        paper_bgcolor="black",
        xaxis=dict(showgrid=False, color="white"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", color="white"),
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig

# ---------------------------------------------------
# Trend Charts (Stock style)
# ---------------------------------------------------
st.subheader("📈 Historical Trends (Stock Style)")

trend_cols = st.columns(2)

with trend_cols[0]:
    st.plotly_chart(stock_line_chart(country_data, "GDP per Capita (USD)", "💵 GDP Trend"), use_container_width=True)

with trend_cols[1]:
    st.plotly_chart(stock_line_chart(country_data, "Life Expectancy", "👶 Life Expectancy Trend"), use_container_width=True)

with trend_cols[0]:
    st.plotly_chart(stock_line_chart(country_data, "PM2.5 (µg/m³)", "🌫️ PM2.5 Pollution Trend"), use_container_width=True)

with trend_cols[1]:
    st.plotly_chart(stock_line_chart(country_data, "HDI", "📘 HDI Trend Over Time"), use_container_width=True)

# ---------------------------------------------------
# Bar Charts
# ---------------------------------------------------
# -----------------------------
# BAR CHARTS WITH SAME THEME
# -----------------------------
st.subheader("📦 Attractive Bar Charts")

b1, b2 = st.columns(2)

with b1:
    fig_bar1 = px.bar(
        country_data,
        x="Year",
        y="Total Population",
        title="📌 Total Population Over Time",
        template="plotly_dark"
    )
    st.plotly_chart(fig_bar1, use_container_width=True)

with b2:
    fig_bar2 = px.bar(
        country_data,
        x="Year",
        y="COVID Cases",
        title="🦠 COVID Cases Over Time",
        color="COVID Cases",
        template="plotly_dark"
    )
    st.plotly_chart(fig_bar2, use_container_width=True)

# ---------------------------------------------------
# Raw Data
# ---------------------------------------------------
st.markdown("### 🔍 Full Data for Selected Year")
st.dataframe(pd.DataFrame([row]))
