import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("final_with_socio_cleaned.csv")

df["Year"] = df["Year"].astype(int)

years = sorted(df["Year"].unique().tolist())  # 👈 convert to python list

# -----------------------------
# Dash App
# -----------------------------
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)

server = app.server  # REQUIRED for Render

# -----------------------------
# Layout
# -----------------------------
app.layout = dbc.Container(
    fluid=True,
    children=[

        html.H2(
            "🌍 Global Health Dashboard",
            style={"textAlign": "center", "margin": "20px"}
        ),

        # ---- Year Slider ----
        html.Div([
            html.Label("Select Year"),
            dcc.Slider(
                id="year-slider",
                min=int(min(years)),
                max=int(max(years)),
                value=int(max(years)),
                step=1,
                marks={int(y): str(y) for y in years if y % 5 == 0}  # ✅ FIX
            )
        ], style={"margin": "20px"}),

        # ---- World Map ----
        dcc.Graph(
            id="world-map",
            style={"height": "75vh"}
        ),

        # ---- Floating Popup ----
        html.Div(
            id="popup-overlay",
            style={
                "display": "none",
                "position": "fixed",
                "top": "0",
                "left": "0",
                "width": "100%",
                "height": "100%",
                "backgroundColor": "rgba(0,0,0,0.75)",
                "zIndex": "999"
            },
            children=[
                html.Div(
                    style={
                        "position": "absolute",
                        "top": "50%",
                        "left": "50%",
                        "transform": "translate(-50%, -50%)",
                        "width": "60%",
                        "backgroundColor": "#111",
                        "padding": "25px",
                        "borderRadius": "10px",
                        "color": "white"
                    },
                    children=[
                        html.H4(id="popup-title"),
                        html.Hr(),
                        html.Div(id="popup-content"),
                        html.Br(),
                        dbc.Button("Close", id="close-popup", color="danger")
                    ]
                )
            ]
        )
    ]
)

# -----------------------------
# Map Callback
# -----------------------------
@app.callback(
    Output("world-map", "figure"),
    Input("year-slider", "value")
)
def update_map(year):
    dff = df[df["Year"] == year]

    fig = px.choropleth(
        dff,
        locations="ISO3",
        color="HDI",
        hover_name="Country",
        color_continuous_scale="Viridis",
        title=f"Global HDI Map - {year}"
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            bgcolor="black"
        ),
        paper_bgcolor="black",
        plot_bgcolor="black"
    )

    return fig

# -----------------------------
# Popup Callback
# -----------------------------
@app.callback(
    Output("popup-overlay", "style"),
    Output("popup-title", "children"),
    Output("popup-content", "children"),
    Input("world-map", "clickData"),
    Input("close-popup", "n_clicks"),
    State("year-slider", "value")
)
def show_popup(clickData, close_clicks, year):

    if close_clicks:
        return {"display": "none"}, "", ""

    if not clickData:
        return {"display": "none"}, "", ""

    iso = clickData["points"][0]["location"]
    row = df[(df["ISO3"] == iso) & (df["Year"] == year)]

    if row.empty:
        return {"display": "none"}, "", ""

    r = row.iloc[0]

    content = html.Div([
        html.P(f"HDI: {r['HDI']}"),
        html.P(f"GDP per Capita: {r['GDP_per_capita']}"),
        html.P(f"Gini Index: {r['Gini_Index']}"),
        html.P(f"Life Expectancy: {r['Life_Expectancy']}"),
        html.P(f"Median Age: {r['Median_Age_Est']}"),
        html.P(f"COVID Deaths / mil: {r['COVID_Deaths']}"),
        html.P(f"Population Density: {r['Population_Density']}")
    ])

    return {"display": "block"}, f"{r['Country']} ({year})", content


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
