import json
import pandas as pd
import plotly.express as px

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# -------------------- LOAD DATA --------------------

# Country geojson
with open("countries.geo.json") as f:
    geojson = json.load(f)

# Colors
hex_df = pd.read_csv("Hex.csv")
hex_df["iso_alpha"] = hex_df["iso_alpha"].str.upper()
country_colors = dict(zip(hex_df["iso_alpha"], hex_df["hex"]))

# Socio economic data
df = pd.read_csv("final_with_socio_cleaned.csv")
df["ISO3"] = df["ISO3"].str.upper()

# Use latest year per country for map
latest_df = df.sort_values("Year").groupby("ISO3").tail(1)

# Assign color
latest_df["color"] = latest_df["ISO3"].map(country_colors).fillna("#666666")

# -------------------- MAP --------------------

map_fig = px.choropleth(
    latest_df,
    geojson=geojson,
    locations="ISO3",
    color="ISO3",  # dummy (we override colors)
    hover_name="Country",
    projection="natural earth"
)

map_fig.update_traces(
    marker_line_width=0.5,
    marker_line_color="black"
)

# Apply custom colors
for i, iso in enumerate(latest_df["ISO3"]):
    map_fig.data[0].z[i] = i
    map_fig.data[0].colorscale = [
        [0, latest_df.iloc[i]["color"]],
        [1, latest_df.iloc[i]["color"]],
    ]

map_fig.update_layout(
    paper_bgcolor="#0b3d91",   # sea blue
    plot_bgcolor="#0b3d91",
    geo=dict(
        bgcolor="#0b3d91",
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
            figure=map_fig,
            style={"height": "90vh"}
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle(id="modal-title"),
                    close_button=True
                ),
                dbc.ModalBody(
                    dcc.Graph(id="line-chart")
                )
            ],
            id="country-modal",
            size="xl",
            centered=True,
            is_open=False,
            backdrop="static"
        )
    ]
)

# -------------------- CALLBACK --------------------

@app.callback(
    Output("country-modal", "is_open"),
    Output("modal-title", "children"),
    Output("line-chart", "figure"),
    Input("world-map", "clickData"),
    Input("country-modal", "is_open")
)
def show_country_details(clickData, is_open):

    if not clickData:
        return False, "", {}

    iso = clickData["points"][0]["location"]
    country_df = df[df["ISO3"] == iso]

    if country_df.empty:
        return False, "", {}

    country_name = country_df["Country"].iloc[0]

    line_fig = px.line(
        country_df,
        x="Year",
        y=["GDP_per_capita", "HDI"],
        markers=True,
        template="plotly_dark",
        title=f"{country_name} – Trends"
    )

    line_fig.update_layout(
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font_color="white"
    )

    return True, country_name, line_fig


# -------------------- RUN --------------------

if __name__ == "__main__":
    app.run_server(debug=False)
