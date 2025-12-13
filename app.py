import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# ----------------------------
# Sample data
# ----------------------------
map_df = pd.DataFrame({
    "lat": [21, 37, 35],
    "lon": [78, -95, 103],
    "country": ["India", "USA", "China"]
})

indicator_data = {
    "India": pd.DataFrame({"Year": [2018,2019,2020,2021,2022], "GDP":[2.5,2.7,2.6,3.0,3.2], "HDI":[0.64,0.65,0.65,0.66,0.67]}),
    "USA": pd.DataFrame({"Year": [2018,2019,2020,2021,2022], "GDP":[20.5,21,20.8,22,23], "HDI":[0.92,0.92,0.92,0.93,0.93]}),
    "China": pd.DataFrame({"Year": [2018,2019,2020,2021,2022], "GDP":[13.5,14,14.2,15,16], "HDI":[0.75,0.76,0.76,0.77,0.78]})
}

# ----------------------------
# Map figure
# ----------------------------
fig = px.scatter_geo(map_df, lat="lat", lon="lon", hover_name="country", projection="natural earth")
fig.update_traces(marker=dict(size=12, color="blue"))
fig.update_layout(clickmode='event+select')

# ----------------------------
# Dash app
# ----------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Graph(id="world-map", figure=fig, style={"height": "70vh"}),

    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
        dbc.ModalBody(id="modal-body"),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0))
    ], id="modal", is_open=False, size="lg")
])

# ----------------------------
# Callbacks
# ----------------------------
@app.callback(
    Output("modal", "is_open"),
    Output("modal-title", "children"),
    Output("modal-body", "children"),
    Input("world-map", "clickData"),
    Input("close-modal", "n_clicks"),
    State("modal", "is_open")
)
def toggle_modal(clickData, n_close, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, "", ""

    triggered = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered == "close-modal" and is_open:
        return False, "", ""
    elif triggered == "world-map" and clickData:
        country = clickData["points"][0]["hovertext"]
        df = indicator_data.get(country)
        if df is None:
            return True, f"{country} Details", html.P("No data available")
        
        # Line charts inside modal
        gdp_chart = dcc.Graph(figure=px.line(df, x="Year", y="GDP", title=f"{country} GDP"))
        hdi_chart = dcc.Graph(figure=px.line(df, x="Year", y="HDI", title=f"{country} HDI"))

        return True, f"{country} Details", html.Div([gdp_chart, hdi_chart])
    return is_open, "", ""

if __name__ == "__main__":
    app.run_server(debug=True)
