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
    res = session.query(TerroristAct).limit(10000).all()
    t_query = time.time()
    print(f'Query took {t_query - start} seconds.')
    

    dates = [r.date for r in res]
    lats = [r.latitude for r in res]
    lngs = [r.longitude for r in res]
    summaries = [r.summary for r in res]
    killed_counts = [r.num_killed for r in res]
    injured_counts = [r.num_injured for r in res]

    cas_counts = [(k if not k == None else 0) + (w if not w == None else 0) for k, w in zip(killed_counts, injured_counts)]
    log_cas_counts = [math.log(c) + 1 if c > 0 else 1 for c in cas_counts]
    has_casualties = [True if c > 0 else False for c in cas_counts]

    #random circular offsets:
    us = [random.random() + random.random() for _ in res]
    rs = [0.01 * (2 - u if u > 1 else u) for u in us]
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
        'Casualties (x 10^n)' : log_cas_counts,
        'Killed': killed_counts,
        'Injured': injured_counts,
        'Summary': summaries,
        'Has Casualties': has_casualties
    })

    print('data loaded')
    #df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv') # Placeholder

    fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude',
                            center=dict(lat=0, lon=180), zoom=1,
                            mapbox_style="dark", 
                            color='Has Casualties',
                            hover_data={
                                'Latitude': False,
                                'Longitude': False,
                                'Date': True,
                                'Casualties': True,
                                'Killed': False,
                                'Injured': False,
                                'Summary': False
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
        dbc.NavbarSimple(
            id = 'navbar',
            children=[
                dbc.NavItem(dbc.NavLink("About", id='about-link', href='/about'))
            ],
            brand='INSERT NAME HERE',
            brand_href='/',
            color='secondary',
            dark=True
        ),
        html.Div(id='page-content')
    ])

    index_layout = html.Div(children=[
        html.H1(id='index-header', children='Main Page', ),
        daq.Slider(id='date-slider', min=0, max=100, value=20),
        dcc.Graph(id='map-graph', figure=get_fig()),
        html.Div(id='summary-container', children='')
    ])

    about_layout = html.Div(children=[
        html.H1(id='about-header', children='Welcome to our about page!'),
        html.P(id='about-text', children='text')
    ])

    # Update the index
    @app.callback(dash.dependencies.Output('page-content', 'children'),
                [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/':
            return index_layout
        elif pathname == '/about':
            return about_layout
        else:
            return index_layout
    # You could also return a 404 "URL not found" page here

    @app.callback(
        dash.dependencies.Output('summary-container', 'children'),
        dash.dependencies.Input('map-graph', 'hoverData'))
    def display_hover_data(hoverData):
        print(hoverData)
        summary = hoverData['points'][0]['customdata'][6]
        injured = hoverData['points'][0]['customdata'][5]
        killed = hoverData['points'][0]['customdata'][4]
        
        if injured == None:
            injured = 'None Reported'
        elif injured == '0':
            injured = 'No injuries.'

        if killed == None:
            killed = 'None Reported'
        elif killed == '0':
            killed = 'No deaths.'

        if summary == '' or summary == None:
            summary = 'No summary available.'

        #print(summary)

        kill_elem = html.P(id='kill-count-text', children=f'Deaths: {killed}')
        injured_elem = html.P(id='injured-count-text', children=f'Injuries: {injured}')
        summary_elem = html.P(id='summary-text', children=summary)

        return [kill_elem, injured_elem, summary_elem]

    return app

