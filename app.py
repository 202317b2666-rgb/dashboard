import json
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# -----------------------------
# Load data
# -----------------------------
data = pd.read_csv("final_with_socio_cleaned.csv")
hex_df = pd.read_csv("Hex.csv")

with open("countries.geo.json", "r", encoding="utf-8") as f:
    geojson = json.load(f)

data.columns = data.columns.str.strip()

ISO_COL = "ISO3" if "ISO3" in data.columns else "ISO3_code"

# -----------------------------
# App
# -----------------------------
app = Dash(__name__)
server = app.server

# -----------------------------
# Layout
# -----------------------------
app.layout = html.Div([

    html.H1("🌍 Global Health Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Year"),
        dcc.Slider(
            min=int(data["Year"].min()),
            max=int(data["Year"].max()),
            step=1,
            value=2020,
            marks={y: str(y) for y in range(1980, 2025, 5)},
            id="year-slider"
        ),
    ], style={"padding": "20px"}),

    dcc.Graph(id="world-map"),

    html.Div(
        id="popup",
        style={
            "position": "fixed",
            "top": "120px",
            "right": "20px",
            "width": "320px",
            "backgroundColor": "white",
            "padding": "15px",
            "borderRadius": "10px",
            "boxShadow": "0px 0px 15px rgba(0,0,0,0.3)",
            "display": "none",
            "zIndex": "1000"
        }
    )
])

# -----------------------------
# Map update
# -----------------------------
@app.callback(
    Output("world-map", "figure"),
    Input("year-slider", "value")
)
def update_map(year):
    df = data[data["Year"] == year]

    fig = px.choropleth(
        df,
        geojson=geojson,
        locations=ISO_COL,
        color="HDI",
        hover_name="Location",
        projection="natural earth",
        color_continuous_scale="Viridis"
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    return fig

# -----------------------------
# Popup update (CLICK)
# -----------------------------
@app.callback(
    Output("popup", "children"),
    Output("popup", "display"),
    Input("world-map", "clickData"),
    Input("year-slider", "value")
)
def show_popup(clickData, year):
    if not clickData:
        return "", "none"

    iso = clickData["points"][0]["location"]
    row = data[(data[ISO_COL] == iso) & (data["Year"] == year)]

    if row.empty:
        return "", "none"

    r = row.iloc[0]

    content = [
        html.H3(r["Location"]),
        html.P(f"Year: {year}"),
        html.P(f"HDI: {round(r.get('HDI', 0), 3)}"),
        html.P(f"GDP per Capita: {round(r.get('GDP_per_capita', 0), 2)}"),
        html.P(f"Gini Index: {round(r.get('GiniIndex', 0), 2)}"),
        html.P(f"Life Expectancy: {round(r.get('LEx', 0), 2)}"),
        html.P(f"Median Age: {round(r.get('MedianAgePop', 0), 2)}"),
    ]

    return content, "block"

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
