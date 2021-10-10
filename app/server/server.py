from utils.cred_handler import get_secret
from db import models, database_connection
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import sqlalchemy as db
from sqlalchemy.sql import func
import dash_daq as daq
import dash_bootstrap_components as dbc
import db.database_connection as conn
from db.models import TerroristAct
import random
import time
import math

def get_fig():
    session = conn.create_session()

    start = time.time()
    res = session.query(TerroristAct).all()

    dates = [r.date for r in res]
    lats = [r.latitude for r in res]
    lngs = [r.longitude for r in res]
    summaries = [r.summary for r in res]
    cas_counts = [1 for _ in res]

    #random circular offsets:
    us = [random.random() + random.random() for _ in res]
    rs = [0.1 * (2 - u if u > 1 else u) for u in us]
    thetas = [random.random() * 2 * math.pi for _ in res]
    x_off = [r * math.cos(theta) for r, theta in zip(rs, thetas)]
    y_off = [r * math.sin(theta) for r, theta in zip(rs, thetas)]

    #add offsets
    lats = [lat + x for lat, x in zip(lats, x_off)]
    lngs = [lng + y for lng, y in zip(lngs, y_off)]

    print(len(res))
    print(len(lats))
    print(len(lngs))

    df = pd.DataFrame({
        'Date': dates,
        'Latitude': lats,
        'Longitude': lngs,
        'Casualties': cas_counts,
        'Summary': summaries
    })

    print('data loaded')
    #df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv') # Placeholder

    fig = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='Casualties', radius=3,
                            center=dict(lat=0, lon=180), zoom=1,
                            mapbox_style="dark", 
                            hover_data={
                                'Latitude': False,
                                'Longitude': False,
                                'Date': True,
                                'Casualties': True,
                                'Summary': True
                            })

    print('data plotted')
    fig.update_layout(
        margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor="Black"
    )
    end = time.time()
    print(f'Took {end - start} seconds.')

    return fig

def get_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
    px.set_mapbox_access_token(get_secret("mapbox_api_key"))

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='points', ),
        dbc.Navbar(
            [
                html.A(
                    [
                        html.Img(src=app.get_asset_url('TTT.png'), height='30px'),
                        dbc.NavbarBrand("errorism Tracker")
                    ],
                    href='/',
                    style={'display': 'flex', 'align-items': 'center'}
                ),
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem("About Us", id='about-link', href='/about'),
                        dbc.ListGroupItem("References", id='ref-link', href='/reference'),
                    ],
                    horizontal=True,
                )
            ],
            color="secondary",
            dark=True,
            className='d-flex',
            style={'justify-content': 'space-between'}
        ),
        html.Div(id='page-content')
    ])

    index_layout = html.Div(children=[
        html.H1(id='index-header', children='Main Page', ),
        daq.Slider(id='date-slider', min=0, max=100, value=20),
        dcc.Graph(id='map-graph', figure=get_fig())
    ])

    about_layout = html.Div(children=[
        html.H1(id='about-header', children='Welcome to our about page!'),
        html.P(id='about-text', children='text')
    ])

    ref_layout = html.Div(children=[
        html.H1(id='ref-header', children='Welcome to our reference page!'),
        html.P(id='ref-text', children='text')
    ])

    # Update the index
    @app.callback(dash.dependencies.Output('page-content', 'children'),
                [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/':
            return index_layout
        elif pathname == '/about':
            return about_layout
        elif pathname == '/reference':
            return ref_layout
        else:
            return index_layout
    # You could also return a 404 "URL not found" page here

    return app

