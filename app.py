# app.py

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Initialize Dash
app = Dash(__name__)
server = app.server  # REQUIRED for Render deployment

# Sample data for 3 countries
df = pd.DataFrame({
    "country": ["India", "United States", "China"],
    "iso": ["IND", "USA", "CHN"],
    "value": [1, 2, 3],
    "img": [
        "https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
        "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_China.svg"
    ]
})

# Create choropleth map
fig = px.choropleth(
    df,
    locations="iso",
    color="value",
    hover_name="country",
    custom_data=["img"],
    color_continuous_scale="Blues"
)

# Hover shows small image
fig.update_traces(
    hovertemplate="""
    <b>%{hovertext}</b><br><br>
    <img src="%{customdata[0]}" width="100">
    """
)

fig.update_layout(
    geo=dict(showframe=False, showcoastlines=False),
    margin=dict(l=0, r=0, t=0, b=0)
)

# Layout
app.layout = html.Div([
    dcc.Graph(id="world-map", figure=fig),
    html.Div(
        id="popup",
        style={
            "display": "none",
            "position": "fixed",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "background": "white",
            "padding": "20px",
            "boxShadow": "0px 4px 20px rgba(0,0,0,0.3)",
            "zIndex": "999"
        }
    )
])

# Callback for click → popup
@app.callback(
    Output("popup", "children"),
    Output("popup", "style"),
    Input("world-map", "clickData")
)
def show_popup(clickData):
    if not clickData:
        return "", {"display": "none"}

    country = clickData["points"][0]["hovertext"]
    img = clickData["points"][0]["customdata"][0]

    return (
        [
            html.H3(country),
            html.Img(src=img, style={"width": "200px"})
        ],
        {
            "display": "block",
            "position": "fixed",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "background": "white",
            "padding": "20px",
            "boxShadow": "0px 4px 20px rgba(0,0,0,0.3)",
            "zIndex": "999"
        }
    )

# Run server locally (optional for local testing)
if __name__ == "__main__":
    app.run_server(debug=True)
