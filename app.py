import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("final_with_socio_cleaned.csv")
df["Year"] = df["Year"].astype(int)
years = sorted(df["Year"].unique().tolist())  # convert to python list

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
                marks={int(y): str(y) for y in years if y % 5 == 0}
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
                        "width": "80%",
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
# Popup Callback with Line Charts
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
    triggered_id = ctx.triggered_id

    if triggered_id == "close-popup":
        return {"display": "none"}, "", ""

    if triggered_id != "world-map" or not clickData:
        return {"display": "none"}, "", ""

    iso = clickData["points"][0]["location"]
    country_df = df[df["ISO3"] == iso]

    if country_df.empty:
        return {"display": "none"}, "", ""

    # Create line charts for selected attributes
    fig = make_subplots(rows=2, cols=2, subplot_titles=("HDI", "GDP per Capita", "Life Expectancy", "Population Density"))

    # HDI
    fig.add_trace(go.Scatter(
        x=country_df["Year"], y=country_df["HDI"], mode="lines+markers", name="HDI"
    ), row=1, col=1)

    # GDP per Capita
    fig.add_trace(go.Scatter(
        x=country_df["Year"], y=country_df["GDP_per_capita"], mode="lines+markers", name="GDP per Capita"
    ), row=1, col=2)

    # Life Expectancy
    fig.add_trace(go.Scatter(
        x=country_df["Year"], y=country_df["Life_Expectancy"], mode="lines+markers", name="Life Expectancy"
    ), row=2, col=1)

    # Population Density
    fig.add_trace(go.Scatter(
        x=country_df["Year"], y=country_df["Population_Density"], mode="lines+markers", name="Population Density"
    ), row=2, col=2)

    fig.update_layout(
        height=500,
        width=800,
        template="plotly_dark",
        margin=dict(t=50, b=20)
    )

    return {"display": "block"}, f"{country_df.iloc[0]['Country']} ({year})", dcc.Graph(figure=fig)

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
