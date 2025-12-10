import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Country Dashboard", layout="wide")
st.title("🌍 Country Insights Explorer (Premium View)")

# Load Data
df = pd.read_csv("final_with_socio_cleaned.csv")

# Rename columns for UI clarity
df = df.rename(columns={
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

# -----------------------------
# Filters
# -----------------------------
countries = sorted(df["Country"].unique())
years = sorted(df["Year"].unique())

st.sidebar.header("⚙️ Filters")
selected_country = st.sidebar.selectbox("Select Country", countries)
selected_year = st.sidebar.slider("Select Year", min(years), max(years), max(years))

# Filtered row
row = df[(df["Country"] == selected_country) & (df["Year"] == selected_year)]
if row.empty:
    st.warning("No data for this year.")
    st.stop()
row = row.iloc[0]

st.markdown(f"## 📌 {selected_country} — {selected_year}")

# -----------------------------
# METRIC CARDS
# -----------------------------
st.subheader("📊 Key Indicators")
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
    ("COVID Deaths", "☠️"),
    ("COVID Cases", "🦠"),
]

for i, (name, emoji) in enumerate(metrics):
    with metric_cols[i % 4]:
        st.metric(f"{emoji} {name}", row[name] if pd.notna(row[name]) else "No Data")

# -----------------------------
# STOCK-STYLE TREND LINE CHART FUNCTION
# -----------------------------
def stock_chart(df, y, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df[y],
        mode="lines+markers",
        line=dict(width=3, color="cyan"),
        marker=dict(color="red", size=6)
    ))

    fig.update_layout(
        template="plotly_dark",
        title=title,
        height=380,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

# -----------------------------
# INDIVIDUAL TREND CHARTS
# -----------------------------
st.subheader("📈 Stock-Style Historical Trends")
country_data = df[df["Country"] == selected_country]

c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(stock_chart(country_data, "GDP per Capita (USD)", "💵 GDP Trend"), use_container_width=True)

with c2:
    st.plotly_chart(stock_chart(country_data, "Life Expectancy", "👶 Life Expectancy Trend"), use_container_width=True)

with c1:
    st.plotly_chart(stock_chart(country_data, "PM2.5 (µg/m³)", "🌫️ PM2.5 Air Pollution"), use_container_width=True)

with c2:
    st.plotly_chart(stock_chart(country_data, "HDI", "📘 HDI Trend"), use_container_width=True)

# -----------------------------
# MULTI LINE CHART (ALL INDICATORS)
# -----------------------------
st.subheader("📡 Multi-Indicator Line Chart")

multi_cols = [
    "GDP per Capita (USD)",
    "Life Expectancy",
    "PM2.5 (µg/m³)",
    "HDI",
    "Gini Index",
    "Health Insurance (%)",
]

long_df = country_data.melt(id_vars=["Year"], value_vars=multi_cols, var_name="Indicator", value_name="Value")

fig_multi = px.line(
    long_df,
    x="Year",
    y="Value",
    color="Indicator",
    markers=True,
    template="plotly_dark",
    title="📊 Multi-Indicator Comparison",
)

fig_multi.update_layout(height=500)
st.plotly_chart(fig_multi, use_container_width=True)

# -----------------------------
# BAR CHARTS (Attractive)
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

# -----------------------------
# RAW DATA
# -----------------------------
st.subheader("📄 Raw Data for Selected Year")
st.dataframe(pd.DataFrame([row]))
