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

# Rename columns
df = df.rename(columns={
    "GDP_per_capita": "GDP per Capita (USD)",
    "Gini_Index": "Gini Index",
    "Life_Expectancy": "Life Expectancy",
    "PM25": "PM2.5 (µg/m³)",
    "Health_Insurance": "Health Insurance (%)",
    "Median_Age_Mid": "Median Age",
    "COVID_Deaths": "COVID Deaths",
    "COVID_Cases": "COVID Cases",
    "Population_Density": "Population Density",
    "Total_Population": "Total Population",
    "Births": "Births",
    "Deaths": "Deaths",
    "HDI": "HDI"
})

df = df.drop_duplicates(subset=["Country", "Year"])

# -----------------------------
# TOP FILTERS (NOT SIDEBAR)
# -----------------------------
colA, colB = st.columns([3, 2])

countries = sorted(df["Country"].unique())
years = sorted(df["Year"].unique())

with colA:
    selected_country = st.selectbox("🌎 Select Country", countries)

with colB:
    selected_year = st.slider("📅 Select Year", min(years), max(years), max(years))

# Filtered
row = df[(df["Country"] == selected_country) & (df["Year"] == selected_year)]
if row.empty:
    st.warning("No data for this year.")
    st.stop()
row = row.iloc[0]

st.markdown(f"## 📌 {selected_country} — {selected_year}")

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Key Indicators")
metric_cols = st.columns(4)

metrics = [
    ("GDP per Capita (USD)", "💵"),
    ("Life Expectancy", "👶"),
    ("Median Age", "📈"),
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
# PREMIUM LINE CHART FUNCTION
# -----------------------------
def premium_line(df, y, title):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df[y],
        mode="lines+markers",
        line=dict(width=4, color="#00E5FF"),   # Glow cyan-blue
        marker=dict(size=8, color="#FF3366"),  # Neon red markers
        hovertemplate="<b>Year %{x}</b><br>%{y}<extra></extra>"
    ))

    fig.update_layout(
        template="plotly_dark",
        title=title,
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#333"),
    )
    return fig

# -----------------------------
# TREND CHARTS (BEAUTIFUL)
# -----------------------------
st.subheader("📈 Attractive Trend Charts")

country_data = df[df["Country"] == selected_country]

t1, t2 = st.columns(2)

with t1:
    st.plotly_chart(premium_line(country_data, "GDP per Capita (USD)", "💵 GDP Trend"), use_container_width=True)

with t2:
    st.plotly_chart(premium_line(country_data, "Life Expectancy", "👶 Life Expectancy"), use_container_width=True)

with t1:
    st.plotly_chart(premium_line(country_data, "PM2.5 (µg/m³)", "🌫️ PM2.5 Air Pollution"), use_container_width=True)

with t2:
    st.plotly_chart(premium_line(country_data, "HDI", "📘 HDI Trend"), use_container_width=True)

# -----------------------------
# BAR CHARTS WITH SAME THEME
# -----------------------------
st.subheader("📦 Important Bar Charts")

b1, b2 = st.columns(2)

def themed_bar(df, y, title):
    fig = px.bar(
        df,
        x="Year",
        y=y,
        color=y,
        template="plotly_dark",
        title=title
    )
    fig.update_layout(height=400)
    return fig

with b1:
    st.plotly_chart(themed_bar(country_data, "Total Population", "📌 Total Population Over Time"), use_container_width=True)

with b2:
    st.plotly_chart(themed_bar(country_data, "COVID Cases", "🦠 COVID Cases Over Time"), use_container_width=True)

with b1:
    st.plotly_chart(themed_bar(country_data, "Births", "👶 Births Over Time"), use_container_width=True)

with b2:
    st.plotly_chart(themed_bar(country_data, "Deaths", "⚰️ Deaths Over Time"), use_container_width=True)

# -----------------------------
# RAW DATA
# -----------------------------
st.subheader("📄 Raw Data for Selected Year")
st.dataframe(pd.DataFrame([row]))
