import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
import pandas as pd

# ----------------------------
# Load datasets
# ----------------------------
socio_df = pd.read_csv("final_socio_cleaned.csv")
hex_df = pd.read_csv("Hex.csv")

# Merge colors
country_colors = dict(zip(hex_df["country"], hex_df["hex"]))

# ----------------------------
# Prepare map figure
# ----------------------------
map_df = socio_df.groupby("Country").first().reset_index()  # one row per country

fig = px.scatter_geo(
    map_df,
    lat=[0]*len(map_df),  # placeholder lat
    lon=[0]*len(map_df),  # placeholder lon
    hover_name="Country",
    projection="natural earth",
    title="Global Health Dashboard"
)

# Assign country colors if exists in Hex.csv
fig.update_traces(marker=dict(size=12, color=[
    country_colors.get(c, "blue") for c in map_df["Country"]
]))

fig.update_geos(
    showcoastlines=True, coastlinecolor="white",
    showland=True, landcolor="lightgrey",
    showocean=True, oceancolor="#4DA6FF"
)

# ----------------------------
# Initialize Dash app
# ----------------------------
app = dash.Dash(__name__)
app.title = "Global Health Dashboard"

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div([
    html.H1("Global Health Dashboard", style={"color": "white", "textAlign": "center"}),
    dcc.Graph(id="world-map", figure=fig, style={"height": "70vh"}),
    
    # Floating popup window
    html.Div(id="popup-div", style={
        "display": "none",
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "width": "700px",
        "height": "500px",
        "background-color": "#111",  # black background
        "color": "white",
        "border": "2px solid white",
        "box-shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "z-index": "999",
        "padding": "20px",
        "overflow-y": "scroll"
    }, children=[
        html.H2(id="popup-title", children=""),
        html.Div(id="popup-charts"),
        html.Button("Close", id="close-popup", n_clicks=0, style={
            "margin-top": "20px", "padding": "5px 10px"
        })
    ])
])

# ----------------------------
# Callbacks
# ----------------------------
@app.callback(
    Output("popup-div", "style"),
    Output("popup-title", "children"),
    Output("popup-charts", "children"),
    Input("world-map", "clickData"),
    Input("close-popup", "n_clicks"),
    State("popup-div", "style"),
    prevent_initial_call=True
)
def display_popup(clickData, n_clicks, current_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_style, "", ""
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Close popup
    if triggered_id == "close-popup":
        current_style["display"] = "none"
        return current_style, "", ""
    
    # Show popup for clicked country
    if clickData:
        country = clickData["points"][0]["hovertext"]
        current_style["display"] = "block"

        # Filter data for the country
        df = socio_df[socio_df["Country"] == country]
        if df.empty:
            return current_style, f"{country} Details", html.P("No data available", style={"color": "white"})
        
        # Line charts for GDP_per_capita, HDI
        gdp_chart = dcc.Graph(
            figure=px.line(df, x="Year", y="GDP_per_capita", title=f"{country} GDP per Capita", template="plotly_dark")
        )
        hdi_chart = dcc.Graph(
            figure=px.line(df, x="Year", y="HDI", title=f"{country} HDI", template="plotly_dark")
        )

        charts = html.Div([gdp_chart, hdi_chart])
        return current_style, f"{country} Details", charts

    return current_style, "", ""

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
