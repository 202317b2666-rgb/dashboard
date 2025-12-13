import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
import pandas as pd

# ----------------------------
# Load country colors (Hex.csv)
# ----------------------------
# Sample Hex.csv structure:
# country,iso_alpha,hex
# India,IND,#FF5733
# USA,USA,#33FF57
# China,CHN,#3357FF
hex_df = pd.read_csv("Hex.csv")

# ----------------------------
# Sample map data (latitude, longitude)
# Replace with actual coordinates for all countries later
# ----------------------------
map_df = pd.DataFrame({
    "lat": [21, 37, 35],
    "lon": [78, -95, 103],
    "country": ["India", "USA", "China"]
})

# Merge hex colors with map_df
map_df = map_df.merge(hex_df, left_on="country", right_on="country", how="left")

# ----------------------------
# Sample indicator data
# Replace/add actual indicators as needed
# ----------------------------
indicator_data = {
    "India": pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022],
        "GDP": [2.5, 2.7, 2.6, 3.0, 3.2],
        "HDI": [0.64, 0.65, 0.65, 0.66, 0.67]
    }),
    "USA": pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022],
        "GDP": [20.5, 21.0, 20.8, 22.0, 23.0],
        "HDI": [0.92, 0.92, 0.92, 0.93, 0.93]
    }),
    "China": pd.DataFrame({
        "Year": [2018, 2019, 2020, 2021, 2022],
        "GDP": [13.5, 14.0, 14.2, 15.0, 16.0],
        "HDI": [0.75, 0.76, 0.76, 0.77, 0.78]
    })
}

# ----------------------------
# Plotly map figure
# ----------------------------
fig = px.scatter_geo(
    map_df,
    lat="lat",
    lon="lon",
    hover_name="country",
    projection="natural earth",
    title="Interactive World Map"
)

# Use Hex colors for countries
fig.update_traces(marker=dict(size=12, color=map_df["hex"]))

# Blue sea and land color fallback
fig.update_geos(
    showcoastlines=True, coastlinecolor="white",
    showland=True, landcolor="lightgrey",
    showocean=True, oceancolor="#4DA6FF"
)

fig.update_layout(
    paper_bgcolor="#0c0c0c",
    plot_bgcolor="#0c0c0c",
    font_color="white",
    margin={"r":0,"t":30,"l":0,"b":0}
)

# ----------------------------
# Initialize Dash app
# ----------------------------
app = dash.Dash(__name__)
app.title = "Global Health Dashboard"

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div(style={"backgroundColor": "#0c0c0c", "height": "100vh", "padding": "20px"}, children=[
    html.H1("Global Health Dashboard", style={"color": "white", "textAlign": "center"}),
    
    dcc.Graph(id="world-map", figure=fig, style={"height": "75vh", "margin-top": "20px"}),
    
    # Hidden popup
    html.Div(id="popup-div", style={
        "display": "none",
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "width": "600px",
        "height": "500px",
        "background-color": "#111111",  # dark popup
        "color": "white",
        "border": "2px solid #444",
        "box-shadow": "0 4px 20px rgba(0,0,0,0.7)",
        "z-index": "999",
        "padding": "20px",
        "overflow-y": "scroll"
    }, children=[
        html.H2(id="popup-title", children=""),
        html.Div(id="popup-charts"),
        html.Button("Close", id="close-popup", n_clicks=0,
                    style={"margin-top": "20px", "padding": "5px 10px"})
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

        # Get indicator data
        df = indicator_data.get(country)
        if df is None:
            return current_style, f"{country} Details", html.P("No data available")
        
        # Create charts
        gdp_chart = dcc.Graph(
            figure=px.line(df, x="Year", y="GDP", title=f"{country} GDP Trend", template="plotly_dark")
        )
        hdi_chart = dcc.Graph(
            figure=px.line(df, x="Year", y="HDI", title=f"{country} HDI Trend", template="plotly_dark")
        )

        charts = html.Div([gdp_chart, hdi_chart])

        return current_style, f"{country} Details", charts

    return current_style, "", ""

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
