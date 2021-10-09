from utils.cred_handler import get_secret
from db import models, database_connection
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output
import plotly.express as px
import pandas as pd
import sqlalchemy as db
from sqlalchemy.sql import func


def get_app():
    app = dash.Dash(__name__)

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')

    px.set_mapbox_access_token(get_secret("mapbox_api_key"))
    fig = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='Magnitude', radius=10,
                            center=dict(lat=0, lon=180), zoom=1,
                            mapbox_style="dark")

    app.layout = html.Div(children=[
        dcc.Graph(id='map-graph', figure=fig)
    ])

    return app

