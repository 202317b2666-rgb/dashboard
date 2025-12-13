# app.py
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# Load Hex.csv
hex_df = pd.read_csv("Hex.csv")  # columns: country, iso_alpha, hex

# Sample indicators data (replace with your actual data later)
indicators_df = pd.DataFrame({
    "iso_alpha": ["IND", "USA", "CHN"],
    "GDP": [[2.5, 2.7, 2.6, 3.0, 3.2], [21, 22, 20, 23, 24], [13, 14, 15, 16, 17]],
    "Year": [[2018, 2019, 2020, 2021, 2022]]*3
})

# Create color map for countries
color_map = {row['iso_alpha']: row['hex'] for _, row in hex_df.iterrows()}

# Create Dash app
app = dash.Dash(__name__)

# Create initial choropleth map
fig = px.choropleth(
    hex_df,
    locations="iso_alpha",
    color="iso_alpha",  # placeholder, colors applied via color_discrete_map
    hover_name="country",
    color_discrete_map=color_map
)

fig.update_geos(
    showcoastlines=True,
    coastlinecolor="white",
    showocean=True,
    oceancolor="#4DA6FF",  # sea blue
    showland=True
)
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor="#1e1e1e",  # dark background
    plot_bgcolor="#1e1e1e"
)

# App layout
app.layout = html.Div([
    html.H1("Interactive World Map", style={'color':'white', 'textAlign':'center'}),
    dcc.Graph(id="world-map", figure=fig, style={'height':'80vh'}),
    
    # Hidden div for modal
    html.Div(
        id="modal-container",
        style={"display":"none"}
    )
], style={'backgroundColor':'#1e1e1e', 'height':'100vh'})

# Callback to show modal on country click
@app.callback(
    Output("modal-container", "children"),
    Output("modal-container", "style"),
    Input("world-map", "clickData"),
)
def display_modal(clickData):
    if clickData is None:
        return "", {"display":"none"}
    
    iso_code = clickData['points'][0]['location']
    country_name = hex_df.loc[hex_df['iso_alpha']==iso_code, 'country'].values[0]

    # Sample line chart for GDP
    country_data = indicators_df.loc[indicators_df['iso_alpha']==iso_code].iloc[0]
    gdp_fig = px.line(
        x=country_data['Year'],
        y=country_data['GDP'],
        labels={"x":"Year", "y":"GDP"},
        title=f"{country_name} GDP Trend"
    )
    gdp_fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", font_color="black")

    modal_content = html.Div([
        html.Div([
            html.H2(f"{country_name} Details", style={"marginBottom":"10px"}),
            dcc.Graph(figure=gdp_fig, style={"height":"300px"}),
            html.Button("Close", id="close-modal", n_clicks=0)
        ], style={
            "backgroundColor":"white",
            "padding":"20px",
            "borderRadius":"10px",
            "width":"50%",
            "margin":"50px auto",
            "textAlign":"center"
        })
    ], id="modal", style={
        "position":"fixed",
        "top":"0",
        "left":"0",
        "width":"100%",
        "height":"100%",
        "backgroundColor":"rgba(0,0,0,0.5)",
        "zIndex":"9999",
        "display":"block"
    })

    return modal_content, {"display":"block"}

# Callback to close modal
@app.callback(
    Output("modal-container", "style"),
    Input("close-modal", "n_clicks"),
    State("modal-container", "style")
)
def close_modal(n_clicks, style):
    if n_clicks > 0:
        style['display'] = "none"
    return style

# Run server
if __name__ == "__main__":
    app.run_server(debug=True)
