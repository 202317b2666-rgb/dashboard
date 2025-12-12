import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Load your datasets
# -------------------------
# World map coloring info (hex colors)
hex_df = pd.read_csv("Hex.csv")  # columns: country, iso_alpha, hex

# Socio-economic data
data_df = pd.read_csv("final_with_socio_cleaned.csv")  # detailed indicators

# -------------------------
# Streamlit page
# -------------------------
st.set_page_config(page_title="Global Health & Socio-Economic Dashboard", layout="wide")
st.title("🌍 Interactive Global Health & Socio-Economic Dashboard")
st.write("Hover over a country to highlight. Click to see detailed indicators.")

# -------------------------
# Choropleth Map
# -------------------------
fig = px.choropleth(
    hex_df,
    locations="iso_alpha",
    color="hex",  # we can use hex just for coloring
    hover_name="country",
    color_discrete_map={row['iso_alpha']: row['hex'] for idx, row in hex_df.iterrows()},
    scope="world",
)

# Update layout: background, remove borders
fig.update_geos(
    showcountries=True,
    countrycolor="white",
    showcoastlines=True,
    coastlinecolor="white",
    showframe=False,
    projection_type='natural earth'
)
fig.update_layout(
    geo=dict(bgcolor='rgb(40, 100, 160)'),  # ocean-blue background
    margin={"r":0,"t":0,"l":0,"b":0},
)

# Highlight effect on hover
fig.update_traces(
    marker_line_width=0,
    hoverinfo="location+name",
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial"),
    selector=dict(type='choropleth')
)

# -------------------------
# Render Map
# -------------------------
clicked = st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Click to show details
# -------------------------
# NOTE: Plotly's native click event in Streamlit is limited
# For demonstration, use a selectbox to simulate click
country_list = hex_df['country'].tolist()
selected_country = st.selectbox("Select a country to see details:", country_list)

if selected_country:
    st.subheader(f"Detailed Indicators for {selected_country}")
    
    country_data = data_df[data_df['country'] == selected_country].sort_values("Year")
    
    # Example line charts
    st.line_chart(country_data[["Year", "GDP_per_capita"]].set_index("Year"))
    st.line_chart(country_data[["Year", "Life_Expectancy"]].set_index("Year"))
    st.line_chart(country_data[["Year", "HDI"]].set_index("Year"))
