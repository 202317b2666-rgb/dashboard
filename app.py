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
    color_discrete_map="identity",
)

# 5️⃣ Default layout for borders
fig.update_traces(
    hoverinfo="location",
    hovertemplate="<b>%{location}</b>",
    marker_line_width=0.5,  # default border width
    marker_line_color="black",
)

# 6️⃣ Add interactive "pop-out" effect using hover
fig.update_traces(
    marker=dict(
        line=dict(width=0.5, color="black")
    ),
    selector=dict(type="choropleth")
)

# Add hover/click visual effect
fig.update_traces(
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Arial"
    ),
    selected=dict(
        marker=dict(line=dict(width=3, color="red")),
        opacity=1
    ),
    unselected=dict(
        opacity=0.6
    )
)

# 7️⃣ Update geo layout
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth',
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
)

# 8️⃣ Streamlit app
st.title("Interactive World Map with Click Pop-Out Effect")
st.plotly_chart(fig, use_container_width=True)
