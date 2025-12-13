import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
import pandas as pd

# ----------------------------
# Sample country map data with HEX colors
# ----------------------------
map_df = pd.DataFrame({
    "lat": [21, 37, 35],
    "lon": [78, -95, 103],
    "country": ["India", "USA", "China"],
    "hex": ["#FF5733", "#33FF57", "#3357FF"]
})

# Sample indicator data (GDP, HDI)
indicator_data = {
    "India": pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022],
        "GDP": [2.5, 2.7, 2.6, 3.0, 3.2],
        "HDI": [0.64, 0.65, 0.65, 0.66, 0.67]
    }),
    "USA": pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022],
        "GDP": [20.5, 21.0, 20.8, 22.0, 23.0],
        "HDI": [0.92, 0.92, 0.92, 0.93, 0.93]
    }),
    "China": pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022],
        "GDP": [13.5, 14.0, 14.2, 15.0, 16.0],
        "HDI": [0.75, 0.76, 0.76, 0.77, 0.78]
    })
}

# ----------------------------
# Plotly map figure with sea blue background
# ----------------------------
fig = px.scatter_geo(
    map_df,
    lat="lat",
    lon="lon",
    hover_name="country",
    projection="natural earth",
    title="Interactive World Map"
)
# Set ocean color and country HEX colors
fig.update_geos(
    showcoastlines=True, coastlinecolor="white",
    showland=True, landcolor=map_df["hex"],
    showocean=True, oceancolor="#4DA6FF"  # sea blue
)
fig.update_traces(marker=dict(size=12, color=map_df["hex"]))

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

    # Hidden popup
    html.Div(id="popup-div", style={
        "display": "none",
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "width": "650px",
        "height": "500px",
        "background-color": "#121212",  # dark mode background
        "color": "white",               # text in popup white
        "border": "2px solid white",
        "box-shadow": "0 4px 20px rgba(0,0,0,0.7)",
        "z-index": "999",
        "padding": "20px",
        "overflow-y": "scroll"
    }, children=[
        html.H2(id="popup-title", children="", style={"color": "white"}),
        html.Div(id="popup-charts"),
        html.Button("Close", id="close-popup", n_clicks=0,
                    style={"margin-top": "20px", "padding": "5px 10px"})
    ])
])

# ----------------------------
# Callbacks
# ----------------------------
@app.callback(
    Output("popup-div", "style"),
    Output("popup-title", "children"),
    Output("popup-charts", "children"),
    Input("world-map", "clickData"),
    Input("close-popup", "n_clicks"),
    State("popup-div", "style"),
    prevent_initial_call=True
)
def display_popup(clickData, n_clicks, current_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_style, "", ""
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Close popup
    if triggered_id == "close-popup":
        current_style["display"] = "none"
        return current_style, "", ""
    
    # Show popup for clicked country
    if clickData:
        country = clickData["points"][0]["hovertext"]
        current_style["display"] = "block"

        # Get indicator data
        df = indicator_data.get(country)
        if df is None:
            return current_style, f"{country} Details", html.P("No data available", style={"color": "white"})
        
        # Create charts with white background
        gdp_chart = dcc.Graph(
            figure=px.line(df, x="Year", y="GDP", title=f"{country} GDP Trend").update_layout(
                plot_bgcolor="#ffffff", paper_bgcolor="#121212", font_color="white"
            )
        )
        hdi_chart = dcc.Graph(
            figure=px.line(df, x="Year", y="HDI", title=f"{country} HDI Trend").update_layout(
                plot_bgcolor="#ffffff", paper_bgcolor="#121212", font_color="white"
            )
        )

        charts = html.Div([gdp_chart, hdi_chart])

        return current_style, f"{country} Details", charts

    return current_style, "", ""

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
