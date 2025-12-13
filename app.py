import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("final_with_socio_cleaned.csv")
hex_df = pd.read_csv("Hex.csv")  # columns: Country/ISO3/hex

# Merge hex colors
df = df.merge(hex_df[['ISO3', 'hex']], on='ISO3', how='left')

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
    row = df[df["ISO3"] == iso]

    if row.empty:
        return {"display": "none"}, "", ""

    # Selected year data for line charts
    row_year = row[row["Year"] == year].iloc[0]

    # Small country map
    country_map = px.choropleth(
        row,
        locations="ISO3",
        color="HDI",
        hover_name="Country",
        scope="world",
        color_continuous_scale="Viridis"
    )
    country_map.update_geos(fitbounds="locations", visible=False)
    country_map.update_layout(height=150, margin=dict(l=0, r=0, t=0, b=0))

    # Line charts for key indicators
    line_df = row.sort_values("Year")
    line_fig = px.line(
        line_df,
        x="Year",
        y=["HDI", "GDP_per_capita", "Life_Expectancy"],  # key indicators
        labels={"value": "Value", "variable": "Indicator"},
        title=f"Trends - {row_year['Country']}"
    )
    line_fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white",
        height=250
    )

    popup_content = html.Div([
        html.Div([
            dcc.Graph(figure=country_map, style={'display':'inline-block', 'width':'25%'}),
            dcc.Graph(figure=line_fig, style={'display':'inline-block', 'width':'70%'})
        ])
    ])

    return {"display": "block"}, f"{row_year['Country']} ({year})", popup_content

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
