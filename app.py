# app.py

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Initialize Dash
app = Dash(__name__)
server = app.server  # REQUIRED for Render deployment

# Sample data for 3 countries
df = pd.DataFrame({
    "country": ["India", "United States", "China"],
    "iso": ["IND", "USA", "CHN"],
    "value": [1, 2, 3],
    "img": [
        "https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
        "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_China.svg"
    ],
    # Approximate lat/lon centers for zoom effect
    "lat": [21, 37, 35],
    "lon": [78, -95, 103],
    "zoom": [5, 3, 4]  # projection scale
})

# Function to create choropleth
def create_map(zoom_center=None):
    fig = px.choropleth(
        df,
        locations="iso",
        color="value",
        hover_name="country",
        custom_data=["img"],
        color_continuous_scale="Blues"
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br><img src='%{customdata[0]}' width='100'>"
    )
    geo_dict = dict(showframe=False, showcoastlines=False)
    if zoom_center:
        geo_dict.update(center=dict(lat=zoom_center[0], lon=zoom_center[1]), projection_scale=zoom_center[2])
    fig.update_layout(geo=geo_dict, margin=dict(l=0, r=0, t=0, b=0))
    return fig

# Layout
app.layout = html.Div([
    dcc.Graph(id="world-map", figure=create_map()),
    html.Div(
        id="popup",
        style={
            "display": "none",
            "position": "fixed",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "background": "white",
            "padding": "20px",
            "boxShadow": "0px 4px 20px rgba(0,0,0,0.3)",
            "zIndex": "999"
        }
    )
])

# Callback: click → zoom + popup
@app.callback(
    Output("world-map", "figure"),
    Output("popup", "children"),
    Output("popup", "style"),
    Input("world-map", "clickData")
)
def click_country(clickData):
    if not clickData:
        return create_map(), "", {"display": "none"}

    country_iso = clickData["points"][0]["location"]
    country_data = df[df["iso"] == country_iso].iloc[0]

    zoom_center = (country_data["lat"], country_data["lon"], country_data["zoom"])

    # Create popup content
    popup_children = [
        html.H3(country_data["country"]),
        html.Img(src=country_data["img"], style={"width": "200px"})
    ]
    popup_style = {
        "display": "block",
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "background": "white",
        "padding": "20px",
        "boxShadow": "0px 4px 20px rgba(0,0,0,0.3)",
        "zIndex": "999"
    }

    return create_map(zoom_center), popup_children, popup_style

# Run server locally
if __name__ == "__main__":
    app.run_server(debug=True)
