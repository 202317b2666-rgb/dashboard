import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load cleaned dataset
df = pd.read_csv("final_with_socio_cleaned.csv")

st.write("Loaded Columns:", df.columns.tolist())  # Debug line (optional)

# --- Sidebar ---
st.sidebar.title("Country View Dashboard")
country = st.sidebar.selectbox("Select a Country", sorted(df["Country"].unique()))

country_df = df[df["Country"] == country]

st.title(f"📊 {country} - Socio-Economic & Health Overview")

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

# Chart 1: GDP per capita
gdp_fig = line_chart_dark(country_df["Year"], country_df["GDP_per_capita"], "GDP per Capita", "cyan")
st.plotly_chart(gdp_fig, use_container_width=True)

# Chart 2: Life Expectancy
life_fig = line_chart_dark(country_df["Year"], country_df["Life_Expectancy"], "Life Expectancy", "red")
st.plotly_chart(life_fig, use_container_width=True)

# Chart 3: HDI
hdi_fig = line_chart_dark(country_df["Year"], country_df["HDI"], "Human Development Index", "yellow")
st.plotly_chart(hdi_fig, use_container_width=True)

# --- Combined Multi-Line Chart ---
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
