import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
import pandas as pd
import json

# ----------------------------
# Load datasets
# ----------------------------
socio_df = pd.read_csv("final_with_socio_cleaned.csv")
hex_df = pd.read_csv("Hex.csv")

# Map country name -> color
country_colors = dict(zip(hex_df["country"], hex_df["hex"]))

# Load geojson for country shapes
with open("countries.geo.json") as f:
    countries_geo = json.load(f)

# ----------------------------
# Prepare map figure
# ----------------------------
fig = px.choropleth(
    socio_df.groupby("Country").first().reset_index(),  # one row per country
    geojson=countries_geo,
    locations="ISO3",       # ISO3 codes must match geojson 'id'
    color="Country",        # temporary, colors will be replaced manually
    hover_name="Country",
    projection="natural earth",
    title="Global Health Dashboard",
)

# Update colors using Hex.csv
for i, c in enumerate(socio_df["Country"].unique()):
    if c in country_colors:
        fig.data[0].marker.colors[i] = country_colors[c]

# Geo layout adjustments
fig.update_geos(
    visible=False,
    showcoastlines=True, coastlinecolor="white",
    showland=True, landcolor="lightgrey",
    showocean=True, oceancolor="#4DA6FF"
)

fig.update_layout(
    template="plotly_dark",
    margin={"r":0,"t":50,"l":0,"b":0}
)

# ----------------------------
# Initialize Dash app
# ----------------------------
app = dash.Dash(__name__)
app.title = "Global Health Dashboard"

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div(style={"background-color":"#111"}, children=[
    html.H1("Global Health Dashboard", style={"color": "white", "textAlign": "center"}),
    dcc.Graph(id="world-map", figure=fig, style={"height": "80vh"}),
    
    # Floating popup window
    html.Div(id="popup-div", style={
        "display": "none",
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "width": "700px",
        "height": "500px",
        "background-color": "#111",  # black background
        "color": "white",
        "border": "2px solid white",
        "box-shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "z-index": "999",
        "padding": "20px",
        "overflow-y": "scroll"
    }, children=[
        html.H2(id="popup-title", children=""),
        html.Div(id="popup-charts"),
        html.Button("Close", id="close-popup", n_clicks=0, style={
            "margin-top": "20px", "padding": "5px 10px"
        })
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
        country = clickData["points"][0]["location"]  # ISO3 code from choropleth
        df = socio_df[socio_df["ISO3"] == country]
        country_name = df["Country"].iloc[0] if not df.empty else country
        current_style["display"] = "block"

        if df.empty:
            return current_style, f"{country_name} Details", html.P("No data available", style={"color": "white"})

        # Line charts for indicators
        charts = []
        for col in ["GDP_per_capita", "HDI", "Life_Expectancy", "PM25"]:
            if col in df.columns:
                chart = dcc.Graph(
                    figure=px.line(df, x="Year", y=col, title=f"{country_name} {col.replace('_',' ')}", template="plotly_dark")
                )
                charts.append(chart)

        return current_style, f"{country_name} Details", html.Div(charts)

    return current_style, "", ""

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
