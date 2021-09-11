import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
import pathlib
from dash.dependencies import Input, Output, State


# Initialize app

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "PUMAS Dashboard Test"
server = app.server


# Load data

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

with open('data/tl_2019_01_puma10.json') as geojson_file:
    pumas = json.load(geojson_file)

with open('data/psam_p01.csv') as df_file:
    df = pd.read_csv(df_file, dtype={"PUMA": "string", "AGEP": int})

df_count = df.groupby('PUMA', as_index=False)['AGEP'].size()

# Map figure

map_fig = px.choropleth_mapbox(df_count, geojson=pumas, locations='PUMA', featureidkey="properties.PUMACE10", color='size',
                               color_continuous_scale=px.colors.sequential.Plasma,
                               mapbox_style="carto-darkmatter",
                               zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                               opacity=1,
                               )
map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})



# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(children="PUMAS Dashboard Test"),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    "Heatmap Title",
                                    id="heatmap-title",
                                ),
                                dcc.Graph(
                                    id="county-choropleth",
                                    figure=map_fig
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)