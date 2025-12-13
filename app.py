import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load HEX colors
hex_df = pd.read_csv("Hex.csv")  # Columns: country, iso_alpha, hex

# Sample GDP & HDI data for demonstration
data_df = pd.DataFrame({
    "country": ["India", "USA", "China"],
    "year": [2018, 2019, 2020, 2021, 2022] * 3,
    "GDP": [2.5,2.7,2.6,3.0,3.2, 21,22,20,23,24, 13,14,13,15,16],
    "HDI": [0.64,0.65,0.66,0.67,0.68, 0.92,0.93,0.92,0.94,0.95, 0.76,0.77,0.78,0.79,0.80],
    "iso_alpha": ["IND"]*5 + ["USA"]*5 + ["CHN"]*5
})

# Merge HEX info for coloring
map_df = hex_df.copy()

# Dash app
app = dash.Dash(__name__)
app.title = "Interactive World Map"

# Layout
app.layout = html.Div([
    html.H1("Interactive World Map", style={"textAlign": "center"}),

    dcc.Graph(
        id="world-map",
        figure=px.scatter_geo(
            map_df,
            lat=[21, 37, 35],  # Approx lat for India, USA, China
            lon=[78, -95, 103],  # Approx lon
            hover_name="country",
            projection="natural earth"
        ).update_traces(marker=dict(size=12, color=map_df["hex"]))
         .update_geos(showcoastlines=True, coastlinecolor="white",
                      showland=True, landcolor="lightgrey",
                      showocean=True, oceancolor="#4DA6FF")
    ),

    html.Div(id="popup", style={
        "position": "fixed",
        "top": "10%",
        "left": "10%",
        "width": "80%",
        "height": "80%",
        "backgroundColor": "white",
        "color": "black",
        "zIndex": "9999",
        "display": "none",
        "padding": "20px",
        "overflow": "auto",
        "border": "2px solid black",
        "borderRadius": "10px"
    })
])

# Callback for country click
@app.callback(
    Output("popup", "style"),
    Output("popup", "children"),
    Input("world-map", "clickData")
)
def display_popup(clickData):
    if clickData:
        country_name = clickData["points"][0]["hovertext"]
        # Filter sample data for that country
        country_data = data_df[data_df["country"] == country_name]

        # GDP line chart
        fig_gdp = px.line(country_data, x="year", y="GDP", title=f"{country_name} GDP")
        fig_hdi = px.line(country_data, x="year", y="HDI", title=f"{country_name} HDI")

        return {
            "position": "fixed",
            "top": "10%",
            "left": "10%",
            "width": "80%",
            "height": "80%",
            "backgroundColor": "white",
            "color": "black",
            "zIndex": "9999",
            "display": "block",
            "padding": "20px",
            "overflow": "auto",
            "border": "2px solid black",
            "borderRadius": "10px"
        }, html.Div([
            html.H2(f"{country_name} Details"),
            dcc.Graph(figure=fig_gdp),
            dcc.Graph(figure=fig_hdi),
            html.Button("Close", id="close-btn", n_clicks=0)
        ])
    else:
        return {"display": "none"}, ""

# Callback to close popup
@app.callback(
    Output("popup", "style"),
    Input("close-btn", "n_clicks"),
    prevent_initial_call=True
)
def close_popup(n):
    return {"display": "none"}

if __name__ == "__main__":
    app.run_server(debug=True)
