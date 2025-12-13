import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("final_with_socio_cleaned.csv")
df["Year"] = df["Year"].astype(int)
years = sorted(df["Year"].unique().tolist())  # python list for slider

# Hex colors
hex_df = pd.read_csv("Hex.csv")
hex_df.columns = hex_df.columns.str.strip()  # remove spaces
# Merge safely
if 'ISO3' not in hex_df.columns and 'iso_alpha' in hex_df.columns:
    hex_df = hex_df.rename(columns={'iso_alpha':'ISO3'})
df = df.merge(hex_df[['ISO3', 'hex']], on='ISO3', how='left')

# -----------------------------
# Dash App
# -----------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)
server = app.server

# -----------------------------
# Layout
# -----------------------------
app.layout = dbc.Container(
    fluid=True,
    children=[
        html.H2("🌍 Global Health Dashboard", style={"textAlign": "center", "margin": "20px"}),

        # Year Slider
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

        # World Map
        dcc.Graph(id="world-map", style={"height": "75vh"}),

        # Floating Popup
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
                        "width": "70%",
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
        geo=dict(showframe=False, showcoastlines=False, bgcolor="black"),
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
    if close_clicks or not clickData:
        return {"display": "none"}, "", ""

    iso = clickData["points"][0]["location"]
    row = df[df["ISO3"] == iso].sort_values("Year")

    if row.empty:
        return {"display": "none"}, "", ""

    r = row[row["Year"] == year].iloc[0]

    # Mini country map
    mini_map = px.choropleth(
        row[row["Year"]==year],
        locations="ISO3",
        color="HDI",
        hover_name="Country",
        scope="world",
        color_continuous_scale="Viridis"
    )
    mini_map.update_geos(fitbounds="locations", visible=False)
    mini_map.update_layout(height=150, margin=dict(l=0, r=0, t=0, b=0))

    # Line chart for HDI, GDP, Life Expectancy
    line_fig = px.line(
        row,
        x="Year",
        y=["HDI", "GDP_per_capita", "Life_Expectancy"],
        labels={"value": "Value", "variable": "Indicator"},
        title=f"Trends - {r['Country']}"
    )
    line_fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white",
        height=250
    )
    line_fig.update_xaxes(tickvals=row['Year'], tickangle=45)

    content = html.Div([
        html.P(f"HDI: {r['HDI']}"),
        html.P(f"GDP per Capita: {r['GDP_per_capita']}"),
        html.P(f"Life Expectancy: {r['Life_Expectancy']}"),
        dcc.Graph(figure=line_fig),
        dcc.Graph(figure=mini_map)
    ])

    return {"display": "block"}, f"{r['Country']} ({year})", content

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
