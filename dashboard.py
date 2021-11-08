import plotly.express as px
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import os

import pandas as pd
import json

from utils.globals import *


# Initialize app

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
app.title = "ACS Dashboard"
server = app.server


# Load data
with open(os.path.join(PUMAS_GEOJSON_DIRECTORY, PUMAS_GEOJSON_FILE)) as geojson_file:
    pumas = json.load(geojson_file)

with open(os.path.join(PUMS_CSV_FILE_DIRECTORY, 'pums.csv')) as df_file:
    df = pd.read_csv(df_file, dtype={'GEOID': str})

# Map figure

map_fig = px.choropleth_mapbox(df, geojson=pumas, locations='GEOID', featureidkey="properties.GEOID10", color='size',
                               color_continuous_scale=px.colors.sequential.Viridis,
                               mapbox_style="carto-positron",
                               zoom=7, center={"lat": 43.9, "lon": -72.75},
                               opacity=0.7,
                               )
map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


# App layout

header = dbc.Row(
    id="header",
    justify="between",
    align="start",
    children=[
        dbc.Col(
            width=8,
            children=[
                html.H1(children="American Community Survey Analysis"),
            ]
        ),
    ],
)

main_map = html.Div(
    id="map-container",
    children=[
        dbc.Row(
            dbc.Col(
                width=12,
                children=[
                    html.H2(
                        "PUMAs",
                        id="map-title",
                    ),
                ]
            )
        ),
        dbc.Row(
            dbc.Col(
                width=12,
                children=[
                    dcc.Graph(
                        id="map-figure",
                        figure=map_fig
                    ),
                ]
            )
        )
    ]
)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

graphs = html.Div(
    id="graph-container",
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                    ]
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.Markdown("""
                                            **Click Data**

                                            Click on PUMAs on the map.
                                        """),
                            html.Pre(id='click-data', style=styles['pre']),
                        ],
                        className='three columns'),
                ),
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(

                ),
                dbc.Col(

                ),
            ]
        )
    ]
)

app.layout = dbc.Container(
    id="root",
    fluid=True,
    className="p-5",
    children=[
        header,
        main_map,
        graphs,
    ],
)


@app.callback(
    Output('click-data', 'children'),
    Input('map-figure', 'clickData')
)
def display_click_data(clickData):
    try:
        return clickData["points"][0]["location"]
    except TypeError:
        return


if __name__ == "__main__":
    app.run_server(debug=True)