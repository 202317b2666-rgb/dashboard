import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("final_with_socio_cleaned.csv")

# Ensure ISO3 column exists
df["ISO3"] = df["ISO3"].astype(str)

# -----------------------------
# APP SETUP
# -----------------------------
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
server = app.server

# -----------------------------
# WORLD MAP
# -----------------------------
fig = px.choropleth(
    df,
    locations="ISO3",
    color="HDI",
    hover_name="Location",
    color_continuous_scale="Viridis",
    title="Global HDI Map"
)

# -----------------------------
# LAYOUT (ALL IDS MUST EXIST)
# -----------------------------
app.layout = dbc.Container([

    html.H2("🌍 Global Country Dashboard", className="text-center mt-3"),

    dcc.Graph(
        id="world-map",
        figure=fig,
        style={"height": "75vh"}
    ),

    # 🔹 POPUP (MUST ALWAYS EXIST)
    html.Div(
        id="popup-div",
        style={
            "display": "none",
            "position": "fixed",
            "top": "10%",
            "left": "20%",
            "width": "60%",
            "background": "white",
            "padding": "20px",
            "boxShadow": "0px 0px 15px rgba(0,0,0,0.3)",
            "zIndex": "1000"
        },
        children=[
            html.H4(id="popup-title"),
            html.Hr(),
            html.Div(id="popup-charts"),
            html.Br(),
            dbc.Button("Close", id="close-popup", color="danger")
        ]
    )

], fluid=True)

# -----------------------------
# CALLBACK: SHOW POPUP
# -----------------------------
@app.callback(
    Output("popup-div", "style"),
    Output("popup-title", "children"),
    Output("popup-charts", "children"),
    Input("world-map", "clickData"),
    Input("close-popup", "n_clicks")
)
def display_country_details(clickData, close_clicks):

    if close_clicks:
        return {"display": "none"}, "", ""

    if not clickData:
        return {"display": "none"}, "", ""

    iso = clickData["points"][0]["location"]
    country_df = df[df["ISO3"] == iso]

    if country_df.empty:
        return {"display": "none"}, "", ""

    country_name = country_df.iloc[0]["Location"]

    details = html.Ul([
        html.Li(f"HDI: {country_df.iloc[0]['HDI']}"),
        html.Li(f"Gini Index: {country_df.iloc[0]['GiniIndex']}"),
        html.Li(f"Life Expectancy: {country_df.iloc[0]['LEx']}"),
        html.Li(f"Median Age: {country_df.iloc[0]['MedianAgePop']}")
    ])

    return (
        {"display": "block"},
        f"📊 {country_name}",
        details
    )

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=10000, debug=False)
