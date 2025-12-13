import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
import pandas as pd
import json

# ----------------------------
# Load Hex colors
# ----------------------------
hex_df = pd.read_csv("Hex.csv")  # country, iso_alpha, hex
hex_df = hex_df.set_index("iso_alpha")

# ----------------------------
# Load full socio-economic data
# ----------------------------
socio_df = pd.read_csv("final_socio_cleaned.csv")
# Expected columns: Location, ISO3_code, Year, GDP, HDI, LifeExpectancy, etc.

# Convert to dictionary keyed by country
indicator_data = {}
for country, df in socio_df.groupby("Location"):
    indicator_data[country] = df.sort_values("Year")

# ----------------------------
# Load GeoJSON
# ----------------------------
with open("countries.geo.json") as f:
    geojson = json.load(f)

# ----------------------------
# Choropleth map
# ----------------------------
fig = px.choropleth(
    locations=hex_df.index,
    geojson=geojson,
    color=hex_df["hex"],
    hover_name=hex_df["country"],
    projection="natural earth"
)

fig.update_geos(
    showcoastlines=True, coastlinecolor="white",
    showland=True, landcolor="lightgrey",
    showocean=True, oceancolor="#4DA6FF"
)

fig.update_layout(
    paper_bgcolor="#0c0c0c",
    plot_bgcolor="#0c0c0c",
    font_color="white",
    margin={"r":0,"t":30,"l":0,"b":0}
)

# ----------------------------
# Dash App
# ----------------------------
app = dash.Dash(__name__)
app.title = "Global Health Dashboard"

app.layout = html.Div(style={"backgroundColor": "#0c0c0c", "height": "100vh", "padding": "20px"}, children=[
    html.H1("Global Health Dashboard", style={"color": "white", "textAlign": "center"}),

    dcc.Graph(id="world-map", figure=fig, style={"height": "75vh", "margin-top": "20px"}),

    html.Div(id="popup-div", style={
        "display": "none",
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "width": "600px",
        "height": "500px",
        "background-color": "#111111",
        "color": "white",
        "border": "2px solid #444",
        "box-shadow": "0 4px 20px rgba(0,0,0,0.7)",
        "z-index": "999",
        "padding": "20px",
        "overflow-y": "scroll"
    }, children=[
        html.H2(id="popup-title", children=""),
        html.Div(id="popup-charts"),
        html.Button("Close", id="close-popup", n_clicks=0,
                    style={"margin-top": "20px", "padding": "5px 10px"})
    ])
])

# ----------------------------
# Callback for popup
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

    if triggered_id == "close-popup":
        current_style["display"] = "none"
        return current_style, "", ""

    if clickData:
        country = clickData["points"][0]["hovertext"]
        current_style["display"] = "block"
        df = indicator_data.get(country)
        if df is None:
            return current_style, f"{country} Details", html.P("No data available")

        # Generate charts for all numeric indicators
        charts = []
        for col in df.columns:
            if col not in ["Location", "ISO3_code", "Year"]:
                chart = dcc.Graph(
                    figure=px.line(df, x="Year", y=col, title=f"{country} {col} Trend", template="plotly_dark")
                )
                charts.append(chart)

        return current_style, f"{country} Details", html.Div(charts)

    return current_style, "", ""

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
