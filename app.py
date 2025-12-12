# 1️⃣ Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import json

# 2️⃣ Load data
hex_df = pd.read_csv("Hex.csv")  # Columns: country, iso_alpha, hex
with open("countries.geo.json") as f:
    geojson_data = json.load(f)

# 3️⃣ Merge HEX colors into GeoJSON properties
for feature in geojson_data['features']:
    iso = feature['properties']['ISO_A3']
    color = hex_df.loc[hex_df['iso_alpha'] == iso, 'hex'].values
    feature['properties']['color'] = color[0] if len(color) > 0 else "#CCCCCC"

# 4️⃣ Create Plotly choropleth map
fig = px.choropleth(
    geojson=geojson_data,
    locations=[f['properties']['ISO_A3'] for f in geojson_data['features']],
    color=[f['properties']['color'] for f in geojson_data['features']],
    color_discrete_map="identity",  # Use HEX colors directly
)

# 5️⃣ Update layout for hover/click effects
fig.update_traces(
    hoverinfo="location",
    hovertemplate="<b>%{location}</b>",
    marker_line_width=0.5,  # Default border
    marker_line_color="black",
)

# 6️⃣ Add hover + click "lift" effect
fig.update_traces(
    marker=dict(
        line=dict(width=0.5, color="black")
    ),
    selector=dict(type="choropleth")
)

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth',
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
)

# 7️⃣ Streamlit app
st.title("Interactive World Map with Hover Effect")
st.plotly_chart(fig, use_container_width=True)
