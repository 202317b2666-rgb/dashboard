import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load cleaned dataset
df = pd.read_csv("final_with_socio_cleaned.csv")

# --- Sidebar ---
st.sidebar.title("Country View Dashboard")
country = st.sidebar.selectbox("Select a Country", sorted(df["Country"].unique()))

country_df = df[df["Country"] == country].sort_values("Year")

st.title(f"📊 {country} - Socio-Economic & Health Overview")

# Pick the latest year for KPIs
latest = country_df.iloc[-1]

# --- KPI Cards ---
st.subheader("📌 Key Indicators")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric("GDP per Capita (USD)", f"{latest['GDP_per_capita']:.2f}" if pd.notna(latest['GDP_per_capita']) else "NA")
col2.metric("Life Expectancy", f"{latest['Life_Expectancy']:.2f}" if pd.notna(latest['Life_Expectancy']) else "NA")
col3.metric("HDI", f"{latest['HDI']:.3f}" if pd.notna(latest['HDI']) else "NA")

col4.metric("Population Density", f"{latest['Population_Density']:.2f}" if pd.notna(latest['Population_Density']) else "NA")
col5.metric("Births", f"{latest['Births']:.2f}" if pd.notna(latest['Births']) else "NA")
col6.metric("Deaths", f"{latest['Deaths']:.2f}" if pd.notna(latest['Deaths']) else "NA")

# --- Line Chart Theme (Share Market Style) ---
def line_chart_dark(x, y, title, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(width=2, color=color)))
    fig.update_layout(
        title=title,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        xaxis=dict(showgrid=False, color="white"),
        yaxis=dict(showgrid=False, color="white"),
    )
    return fig

st.subheader("📈 Trend Charts")

# Chart 1: GDP
gdp_fig = line_chart_dark(country_df["Year"], country_df["GDP_per_capita"], "GDP per Capita Over Time", "cyan")
st.plotly_chart(gdp_fig, use_container_width=True)

# Chart 2: Life Expectancy
life_fig = line_chart_dark(country_df["Year"], country_df["Life_Expectancy"], "Life Expectancy Over Time", "red")
st.plotly_chart(life_fig, use_container_width=True)

# Chart 3: HDI
hdi_fig = line_chart_dark(country_df["Year"], country_df["HDI"], "HDI Over Time", "yellow")
st.plotly_chart(hdi_fig, use_container_width=True)

# --- Combined Multi-Line Chart ---
st.subheader("📊 Combined Trend View")

fig_multi = go.Figure()

fig_multi.add_trace(go.Scatter(x=country_df["Year"], y=country_df["GDP_per_capita"], mode="lines", name="GDP", line=dict(width=2)))
fig_multi.add_trace(go.Scatter(x=country_df["Year"], y=country_df["Life_Expectancy"], mode="lines", name="Life Expectancy", line=dict(width=2)))
fig_multi.add_trace(go.Scatter(x=country_df["Year"], y=country_df["HDI"], mode="lines", name="HDI", line=dict(width=2)))

fig_multi.update_layout(
    title="Combined Multi-Line Trends",
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    xaxis=dict(showgrid=False, color="white"),
    yaxis=dict(showgrid=False, color="white"),
)

st.plotly_chart(fig_multi, use_container_width=True)
