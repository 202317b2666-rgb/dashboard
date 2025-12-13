import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("final_with_socio_cleaned.csv")

df["ISO3"] = df["ISO3"].astype(str)

# -----------------------------
# DASH APP
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
    hover_name="Country",   # ✅ FIXED
    color_continuous_scale="Viridis",
    title="Global HDI Map"
)

# -----------------------------
# LAYOUT
# -----------------------------
app.layout = dbc.Container([

    html.H2("🌍 Global Health Dashboard", className="text-center mt-3"),

    dcc.Graph(
        id="world-map",
        figure=fig,
        style={"height": "75vh"}
    ),

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
# CALLBACK
# -----------------------------
@app.callback(
    Output("popup-div", "style"),
    Output("popup-title", "children"),
    Output("popup-charts", "children"),
    Input("world-map", "clickData"),
    Input("close-popup", "n_clicks")
)
def show_country(clickData, close_clicks):

    if close_clicks:
        return {"display": "none"}, "", ""

    if not clickData:
        return {"display": "none"}, "", ""

    iso = clickData["points"][0]["location"]
    row = df[df["ISO3"] == iso]

    if row.empty:
        return {"display": "none"}, "", ""

    r = row.iloc[0]

    content = html.Ul([
        html.Li(f"HDI: {r['HDI']}"),
        html.Li(f"GDP per Capita: {r['GDP_per_capita']}"),
        html.Li(f"Gini Index: {r['Gini_Index']}"),
        html.Li(f"Life Expectancy: {r['Life_Expectancy']}"),
        html.Li(f"Median Age (Est): {r['Median_Age_Est']}"),
        html.Li(f"COVID Deaths / mil: {r['COVID_Deaths']}")
    ])

    return (
        {"display": "block"},
        f"📊 {r['Country']}",
        content
    )

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=10000, debug=False)
