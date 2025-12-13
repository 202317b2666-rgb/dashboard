# app.py

import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
import pandas as pd

# ----------------------------
# Sample country data
# ----------------------------
map_df = pd.DataFrame({
    "lat": [21, 37, 35],
    "lon": [78, -95, 103],
    "country": ["India", "USA", "China"]
})

# ----------------------------
# Plotly map figure
# ----------------------------
fig = px.scatter_geo(
    map_df,
    lat="lat",
    lon="lon",
    hover_name="country",
    projection="natural earth",
    title="Interactive World Map"
)
fig.update_traces(marker=dict(size=12, color="blue"))

# ----------------------------
# Initialize Dash app
# ----------------------------
app = dash.Dash(__name__)
app.title = "Interactive World Map Dashboard"

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div([
    dcc.Graph(id="world-map", figure=fig, style={"height": "70vh"}),
    
    # Hidden div for popup
    html.Div(id="popup-div", style={
        "display": "none",
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "width": "500px",
        "height": "400px",
        "background-color": "white",
        "border": "2px solid black",
        "box-shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "z-index": "999",
        "padding": "20px",
    }, children=[
        html.H2(id="popup-title", children=""),
        html.P("This is a floating popup window!"),
        html.Button("Close", id="close-popup", n_clicks=0)
    ])
])

# ----------------------------
# Callbacks
# ----------------------------
@app.callback(
    Output("popup-div", "style"),
    Output("popup-title", "children"),
    Input("world-map", "clickData"),
    Input("close-popup", "n_clicks"),
    State("popup-div", "style"),
    prevent_initial_call=True
)
def display_popup(clickData, n_clicks, current_style):
    ctx = dash.callback_context

    if not ctx.triggered:
        return current_style, ""
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Close popup
    if triggered_id == "close-popup":
        current_style["display"] = "none"
        return current_style, ""
    
    # Show popup for clicked country
    if clickData:
        country = clickData["points"][0]["hovertext"]
        current_style["display"] = "block"
        return current_style, f"{country} Details"

    return current_style, ""

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
