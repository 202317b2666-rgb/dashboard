import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Country Dashboard", layout="wide")
st.title("🌍 Country Insights Explorer")

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

st.markdown(f"## {selected_country} — {selected_year}")

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Key Indicators")
metric_cols = st.columns(4)

metrics = [
    ("GDP per Capita (USD)"),
    ("Life Expectancy", "👶"),
    ("Median Age""),
    ("Population Density"),
    ("PM2.5 (µg/m³)"),
    ("Health Insurance (%)" ),
    ("HDI" ),
    ("Gini Index" ),
    ("COVID Deaths", "☠️"),
    ("COVID Cases", "🦠"),
]

for i, (name, emoji) in enumerate(metrics):
    with metric_cols[i % 4]:
        st.metric(f"{emoji} {name}", row[name] if pd.notna(row[name]) else "No Data")

# -----------------------------
# PREMIUM LINE CHART FUNCTION
# -----------------------------


def stock_line_chart(df, y, title):
    fig = go.Figure()

    # --- Outer Glow Line ---



def stock_line_chart(df, y, title):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df[y],
        mode="lines",
        line=dict(width=10, color="rgba(0, 255, 255, 0.2)"),  # Cyan glow
        hoverinfo="skip",
        showlegend=False
    ))

    # --- Main Neon Line ---
    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df[y],
        mode="lines",
        line=dict(width=3, color="#00FFFF"),  # Neon cyan
        marker=dict(size=0),
        hovertemplate="<b>Year %{x}</b><br>%{y}<extra></extra>",
        name=title
    ))

    fig.update_layout(
        template="plotly_dark",
        title=title,
        height=420,
        plot_bgcolor="black",
        paper_bgcolor="black",
        xaxis=dict(
            showgrid=False,
            color="white",
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            color="white",
            tickfont=dict(size=14)
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig

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
