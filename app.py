import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# Sample country colors
hex_df = pd.DataFrame({
    "country":["India","USA","China"],
    "iso_alpha":["IND","USA","CHN"],
    "hex":["#FF5733","#33FF57","#3357FF"]
})

# Sample indicator data
indicators_df = pd.DataFrame({
    "iso_alpha":["IND","USA","CHN"],
    "GDP":[[2.5,2.7,2.6,3.0,3.2],[21,22,20,23,24],[13,14,15,16,17]],
    "HDI":[[0.64,0.65,0.66,0.67,0.68],[0.92,0.93,0.94,0.95,0.96],[0.75,0.76,0.77,0.78,0.79]],
    "Year":[[2018,2019,2020,2021,2022]]*3
})

color_map = {row['iso_alpha']: row['hex'] for _, row in hex_df.iterrows()}

app = dash.Dash(__name__)

# Map figure
fig = px.choropleth(
    hex_df,
    locations="iso_alpha",
    color="iso_alpha",
    hover_name="country",
    color_discrete_map=color_map
)
fig.update_geos(showcoastlines=True, coastlinecolor="white", showocean=True, oceancolor="#4DA6FF", showland=True)
fig.update_layout(clickmode='event+select', margin={"r":0,"t":0,"l":0,"b":0})

# Layout with modal hidden initially
app.layout = html.Div([
    html.H1("Interactive World Map", style={'color':'white','textAlign':'center'}),
    dcc.Graph(id="world-map", figure=fig, style={'height':'80vh'}),
    
    # Modal div always exists but hidden initially
    html.Div(id="modal-container", children=[
        html.Div([
            html.H2(id="modal-title"),
            dcc.Graph(id="gdp-chart", style={'height':'250px'}),
            dcc.Graph(id="hdi-chart", style={'height':'250px'}),
            html.Button("Close", id="close-modal", n_clicks=0)
        ], style={"backgroundColor":"white","padding":"20px","borderRadius":"10px","width":"60%","margin":"50px auto","textAlign":"center"})
    ], style={"position":"fixed","top":"0","left":"0","width":"100%","height":"100%","backgroundColor":"rgba(0,0,0,0.5)",
              "zIndex":"9999","display":"none"})
], style={'backgroundColor':'#1e1e1e', 'height':'100vh'})

# Open modal on map click
@app.callback(
    Output("modal-container", "style"),
    Output("modal-title", "children"),
    Output("gdp-chart", "figure"),
    Output("hdi-chart", "figure"),
    Input("world-map", "clickData")
)
def open_modal(clickData):
    if not clickData:
        return {"display":"none"}, "", {}, {}

    iso = clickData['points'][0]['location']
    country_name = hex_df.loc[hex_df['iso_alpha']==iso, 'country'].values[0]
    data = indicators_df.loc[indicators_df['iso_alpha']==iso].iloc[0]

    gdp_fig = px.line(x=data['Year'], y=data['GDP'], title=f"{country_name} GDP")
    gdp_fig.update_layout(paper_bgcolor='white', plot_bgcolor='white', font_color='black')

    hdi_fig = px.line(x=data['Year'], y=data['HDI'], title=f"{country_name} HDI")
    hdi_fig.update_layout(paper_bgcolor='white', plot_bgcolor='white', font_color='black')

    return {"display":"block","position":"fixed","top":"0","left":"0","width":"100%","height":"100%","backgroundColor":"rgba(0,0,0,0.5)","zIndex":"9999"}, country_name + " Details", gdp_fig, hdi_fig

# Close modal
@app.callback(
    Output("modal-container", "style"),
    Input("close-modal", "n_clicks"),
    State("modal-container", "style")
)
def close_modal(n_clicks, style):
    if n_clicks:
        style['display'] = "none"
    return style

if __name__ == "__main__":
    app.run_server(debug=True)
