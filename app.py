import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# ---------------- LOAD FILES ----------------

with open("countries.geo.json", "r", encoding="utf-8") as f:
    geojson = json.load(f)

hex_df = pd.read_csv("Hex.csv")
hex_df["iso_alpha"] = hex_df["iso_alpha"].str.upper()

color_map = dict(zip(hex_df["iso_alpha"], hex_df["hex"]))

df = pd.read_csv("final_with_socio_cleaned.csv")
df["ISO3"] = df["ISO3"].str.upper()

# Latest year for map coloring
latest_df = df.sort_values("Year").groupby("ISO3", as_index=False).last()

# ---------------- MAP ----------------

map_fig = px.choropleth(
    latest_df,
    geojson=geojson,
    locations="ISO3",
    featureidkey="properties.ISO_A3",
    color="ISO3",
    hover_name="Country",
    color_discrete_map=color_map,
    projection="natural earth"
)

map_fig.update_geos(
    bgcolor="#1976D2",   # sea blue
    showcoastlines=False,
    showframe=False
)

map_fig.update_layout(
    paper_bgcolor="#1976D2",
    plot_bgcolor="#1976D2",
    margin=dict(l=0, r=0, t=0, b=0)
)

# ---------------- APP ----------------

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY]
)

server = app.server

app.layout = html.Div(
    style={"backgroundColor": "#000000"},
    children=[

        html.H2(
            "🌍 Global Health Dashboard",
            style={"textAlign": "center", "padding": "12px"}
        ),

        dcc.Graph(
            id="world-map",
            figure=map_fig,
            style={"height": "90vh"}
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
                dbc.ModalBody(
                    dcc.Graph(id="indicator-chart")
                )
            ],
            id="country-modal",
            size="xl",
            centered=True,
            is_open=False
        )
    ]
)

# ---------------- CALLBACK ----------------

@app.callback(
    Output("country-modal", "is_open"),
    Output("modal-title", "children"),
    Output("indicator-chart", "figure"),
    Input("world-map", "clickData")
)
def show_country_popup(clickData):

    if not clickData:
        return False, "", {}

    iso = clickData["points"][0]["location"]
    cdf = df[df["ISO3"] == iso]

    if cdf.empty:
        return False, "", {}

    country = cdf["Country"].iloc[0]

    fig = px.line(
        cdf,
        x="Year",
        y=["GDP_per_capita", "HDI"],
        markers=True,
        template="plotly_dark",
        title=f"{country} – Key Indicators"
    )

    fig.update_layout(
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font_color="white"
    )

    return True, country, fig


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=10000)
