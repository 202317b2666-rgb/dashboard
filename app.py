# 1️⃣ Import Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 2️⃣ Page config
st.set_page_config(page_title="Global Health & Socio-Economic Dashboard", layout="wide")

st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Click on a country in the map to see detailed indicators over time.")

# 3️⃣ Load data
hex_df = pd.read_csv("Hex.csv")
geojson = "countries.geo.json"  # path to your geojson file

# Clean column names
hex_df.columns = hex_df.columns.str.strip().str.replace('\u200b','')
# Ensure ISO3 codes are uppercase
hex_df['ISO3'] = hex_df['ISO3'].str.upper().str.strip()

# 4️⃣ Map: Choropleth
fig = px.choropleth(
    hex_df,
    locations='ISO3',          # ISO alpha-3 codes
    color='GDP_per_capita',    # Example indicator
    hover_name='Country',
    hover_data=['GDP_per_capita', 'Gini_Index', 'Life_Expectancy'],
    geojson=geojson,
    featureidkey="id",
    color_continuous_scale="Viridis"
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})

selected_country = st.plotly_chart(fig, use_container_width=True)

# 5️⃣ Country selector for detailed indicators
country_list = sorted(hex_df['Country'].unique())
selected_country_name = st.selectbox("Select a country for detailed indicators:", country_list)

country_data = hex_df[hex_df['Country'] == selected_country_name].sort_values('Year')

# 6️⃣ Line charts for multiple indicators
st.subheader(f"Indicators for {selected_country_name} Over Time")

fig_lines = go.Figure()
fig_lines.add_trace(go.Scatter(x=country_data['Year'], y=country_data['GDP_per_capita'],
                               mode='lines+markers', name='GDP per capita'))
fig_lines.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Gini_Index'],
                               mode='lines+markers', name='Gini Index'))
fig_lines.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Life_Expectancy'],
                               mode='lines+markers', name='Life Expectancy'))

fig_lines.update_layout(
    height=500,
    width=900,
    xaxis_title="Year",
    yaxis_title="Value",
    legend_title="Indicators",
    margin={"r":20,"t":30,"l":20,"b":20}
)

st.plotly_chart(fig_lines, use_container_width=True)

# 7️⃣ Display selected country latest indicators
latest = country_data.iloc[-1]
st.markdown(f"""
**Latest Indicators for {selected_country_name} ({latest['Year']}):**

- GDP per capita: {latest['GDP_per_capita']}
- Gini Index: {latest['Gini_Index']}
- Life Expectancy: {latest['Life_Expectancy']}
- PM2.5: {latest['PM25']}
- Health Insurance Coverage: {latest['Health_Insurance']}
- Median Age (Estimated): {latest['Median_Age_Est']}
- Median Age (Mid): {latest['Median_Age_Mid']}
- COVID Deaths per Million: {latest['COVID_Deaths']}
- COVID Cases per Million: {latest['COVID_Cases']}
- Population Density: {latest['Population_Density']}
- Total Population: {latest['Total_Population']}
- HDI: {latest['HDI']}
""")
