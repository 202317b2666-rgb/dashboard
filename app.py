import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("final_with_socio_cleaned.csv")
df["Year"] = df["Year"].astype(int)
years = sorted(df["Year"].unique().tolist())

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
                "backgroundColor": "rgba(0,0,0,0.85)",
                "zIndex": "999",
                "overflow": "hidden"
            },
            children=[
                html.Div(
                    style={
                        "position": "absolute",
                        "top": "50%",
                        "left": "50%",
                        "transform": "translate(-50%, -50%)",
                        "width": "85%",
                        "maxHeight": "90%",
                        "backgroundColor": "#111",
                        "padding": "25px",
                        "borderRadius": "10px",
                        "color": "white",
                        "display": "flex",
                        "flexDirection": "column"
                    },
                    children=[
                        html.H4(id="popup-title"),
                        html.Hr(),
                        html.Div(
                            id="popup-content",
                            style={
                                "overflowY": "auto",
                                "maxHeight": "75vh",
                                "display": "grid",
                                "gridTemplateColumns": "1fr 1fr",
                                "gap": "20px"
                            }
                        ),
                        html.Br(),
                        dbc.Button("Close", id="close-popup", color="danger", style={"alignSelf": "center"})
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
# Popup Callback with Individual Charts
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

    # List of important indicators
    indicators = {
        "HDI": "HDI",
        "GDP per Capita": "GDP_per_capita",
        "Life Expectancy": "Life_Expectancy",
        "Median Age": "Median_Age_Est",
        "Gini Index": "Gini_Index",
        "COVID Deaths / mil": "COVID_Deaths",
        "Population Density": "Population_Density"
    }

    chart_list = []

    for title, col in indicators.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=country_df["Year"],
            y=country_df[col],
            mode="lines+markers",
            name=title
        ))
        fig.update_layout(
            title=title,
            template="plotly_dark",
            height=300,
            margin=dict(t=30, b=20),
            xaxis=dict(title="Year", tickangle=-45, nticks=10)
        )
        chart_list.append(dcc.Graph(figure=fig))

    return {"display": "block"}, f"{country_df.iloc[0]['Country']} ({year})", chart_list

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
