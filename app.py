import json
import pandas as pd
import plotly.express as px

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# -------------------- LOAD FILES --------------------

with open("countries.geo.json") as f:
    geojson = json.load(f)

hex_df = pd.read_csv("Hex.csv")
hex_df["iso_alpha"] = hex_df["iso_alpha"].str.upper()

color_map = dict(zip(hex_df["iso_alpha"], hex_df["hex"]))

df = pd.read_csv("final_with_socio_cleaned.csv")
df["ISO3"] = df["ISO3"].str.upper()

# Latest year per country (for map)
latest_df = df.sort_values("Year").groupby("ISO3").tail(1)

# -------------------- MAP --------------------

fig = px.choropleth(
    latest_df,
    geojson=geojson,
    locations="ISO3",
    color="ISO3",
    hover_name="Country",
    projection="natural earth",
    color_discrete_map=color_map
)

fig.update_traces(
    marker_line_color="black",
    marker_line_width=0.5
)

fig.update_layout(
    paper_bgcolor="#1e88e5",   # sea blue
    plot_bgcolor="#1e88e5",
    geo=dict(
        bgcolor="#1e88e5",
        showframe=False,
        showcoastlines=False
    ),
    margin=dict(l=0, r=0, t=0, b=0)
)

# -------------------- APP --------------------

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY]
)

server = app.server

app.layout = html.Div(
    style={"backgroundColor": "#000000", "height": "100vh"},
    children=[

        html.H2(
            "🌍 Global Health Dashboard",
            style={"textAlign": "center", "padding": "10px"}
        ),

        dcc.Graph(
            id="world-map",
            figure=fig,
            style={"height": "90vh"}
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
                dbc.ModalBody(dcc.Graph(id="line-chart"))
            ],
            id="country-modal",
            size="xl",
            centered=True,
            is_open=False
        )
    ]
)

# -------------------- CALLBACK --------------------

@app.callback(
    Output("country-modal", "is_open"),
    Output("modal-title", "children"),
    Output("line-chart", "figure"),
    Input("world-map", "clickData")
)
def open_modal(clickData):

    if not clickData:
        return False, "", {}

    iso = clickData["points"][0]["location"]
    cdf = df[df["ISO3"] == iso]

    if cdf.empty:
        return False, "", {}

    country = cdf["Country"].iloc[0]

    line_fig = px.line(
        cdf,
        x="Year",
        y=["GDP_per_capita", "HDI"],
        template="plotly_dark",
        markers=True,
        title=f"{country} – Trends"
    )

    line_fig.update_layout(
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white"
    )

    return True, country, line_fig


# -------------------- RUN --------------------

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=10000)
