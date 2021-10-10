from dash.html import Frameset
from utils.about import get_about
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
from db.models import TerroristAct, Region
import random
import time
import math
import numpy as np
from db.database_connection import initialize

df = pd.DataFrame({})

def get_df():
    print("Starting DB query.")
    global df
    session = conn.create_session()

    start = time.time()
    res = session.query(
        TerroristAct.date, 
        TerroristAct.latitude, 
        TerroristAct.longitude, 
        TerroristAct.summary, 
        TerroristAct.num_killed, 
        TerroristAct.num_injured, 
        TerroristAct.prop_dam_value, 
        TerroristAct.prop_comment,
        TerroristAct.num_hostages,
        TerroristAct.ransom_amt,
        Region.name).\
            where(TerroristAct.region == Region.id).\
                limit(10000)

                #order_by(func.random()).\
                #    limit(10000).all()

    t_query = time.time()
    print(f'Query took {t_query - start} seconds.')
    

    dates = [r.date for r in res]
    lats = [r.latitude for r in res]
    lngs = [r.longitude for r in res]
    summaries = [r.summary for r in res]
    killed_counts = [r.num_killed for r in res]
    injured_counts = [r.num_injured for r in res]
    region_names = [r.name for r in res]
    prop_dam_values = [r.prop_dam_value for r in res]
    prop_dam_comments = [r.prop_comment for r in res]
    hostages = [r.num_hostages for r in res]
    ransoms = [r.ransom_amt for r in res]

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

    df = pd.DataFrame({
        'Date': pd.to_datetime(dates),
        'Latitude': lats,
        'Longitude': lngs,
        'Casualties': cas_counts,
        'Casualties (x 10^n)' : log_cas_counts,
        'Killed': killed_counts,
        'Injured': injured_counts,
        'Summary': summaries,
        'Has Casualties': has_casualties,
        'Region': region_names,
        'Damage Value': prop_dam_values,
        'Damage Comments': prop_dam_comments,
        'Hostages': hostages,
        'Ransom': ransoms
    }).sort_values(by=['Has Casualties'])
    end = time.time()
    print(f'Processing took {end - t_query} seconds.')
    print(f'Total load took {end - start} seconds.')
    print('Data loaded.')
    session.close()

def get_heatmap_fig(df):
    frame = df[df['Has Casualties']]
    fig = px.density_mapbox(frame, lat='Latitude', lon='Longitude', z='Casualties (x 10^n)', radius=5,
                            center=dict(lat=45, lon=0), zoom=3,
                            mapbox_style="dark", 
                            hover_data={
                                'Latitude': False,
                                'Longitude': False,
                                'Casualties (x 10^n)': False,
                                'Date': True,
                                'Casualties': True,
                                'Damage Value': False,
                                'Damage Comments': False,
                                'Killed': False,
                                'Injured': False,
                                'Summary': False,
                                'Hostages': False,
                                'Ransom': False
                            })

    fig.update_layout(
        margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor="Black",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    return fig

def get_map_fig(df):
    fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude',
                            center=dict(lat=45, lon=0), zoom=3,
                            mapbox_style="dark", 
                            color='Has Casualties',
                            hover_data={
                                'Latitude': False,
                                'Longitude': False,
                                'Date': True,
                                'Casualties': True,
                                'Damage Value': False,
                                'Damage Comments': False,
                                'Killed': False,
                                'Injured': False,
                                'Summary': False,
                                'Hostages': False,
                                'Ransom': False
                            })

    fig.update_layout(
        margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor="Black",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    return fig

def get_dbr_fig(df):
    frame = df.groupby(['Region'], as_index=False).aggregate(np.sum)
    fig = px.bar(frame, x='Region', y=['Damage Value', 'Ransom'], title="Reported Monetary Damages By World Region In Selected Timeframe")
    fig.update_layout(
        yaxis_title='Value (USD)',
        xaxis_title='',
        margin=dict(l=0,r=0,b=0),
        paper_bgcolor="Black",
        plot_bgcolor="Black",
    )
    return fig

def get_dmg_fig(df):
    frame = df.groupby(['Region'], as_index=False).aggregate(np.sum)
    fig = px.bar(frame, x='Region', y=['Killed', 'Injured'], title="Reported Casualties By World Region In Selected Timeframe")
    fig.update_layout(
        yaxis_title='Count',
        xaxis_title='',
        margin=dict(l=0,r=0,b=0),
        paper_bgcolor="Black",
        plot_bgcolor="Black",
    )
    return fig

def get_app():
    initialize()
    global df
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
    px.set_mapbox_access_token(get_secret("mapbox_api_key"))
    get_df()

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

    min_year = df['Date'].min().year
    max_year = df['Date'].max().year + 1
    marks = {(y-min_year)*12 : str(y) for y in range(min_year, max_year+1)}
    max_months = (max_year - min_year) * 12

    index_layout = html.Div(children=[
        dcc.RangeSlider(id='date-slider', min=0, max=max_months, value=[0,max_months], marks=marks),
        dcc.Graph(id='map-graph', figure=get_map_fig(df), style={'height':'50vh'}),
        html.Div(id='bottom-container', children=[
            dbc.Row([
                dbc.Col([
                    html.Div(id='summary-container', children='')
                ]),
                dbc.Col([
                    dcc.Graph(id='deaths-by-region-graph', figure=get_dbr_fig(df), style={'height':'38vh'})
                ]),
                dbc.Col([
                    dcc.Graph(id='damage-by-region-graph', figure=get_dmg_fig(df), style={'height':'38vh'})
                ]),
            ])
        ])
    ])

    about_children = []
    about_content = get_about()
    for i, contributor in enumerate(about_content['Contributors']):
        contribution = about_content['Contributions'][i]
        contrib_content = f'{contributor} - {contribution}'
        about_children.append(html.Span(contrib_content))
        about_children.append(html.Br())

    about_layout = html.Div(children=[
        html.H3(id='about-header', children='About the Devs'),
        html.P(id='about-text', children=
            about_children,
            className='page-text'
        )
    ])

    ref_children = [about_content['References'][0], html.Br()]
    for reason in about_content[
        'Reason'
        ]:
        ref_children.append(html.Span(reason))
        ref_children.append(html.Br())

    ref_layout = html.Div(children=[
        html.H3(id='ref-header', children='References'),
        html.P(id='ref-text', children=
            ref_children,
            className='page-text'
        )
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

    @app.callback(
        dash.dependencies.Output('map-graph', 'figure'),
        dash.dependencies.Output('deaths-by-region-graph', 'figure'),
         dash.dependencies.Output('damage-by-region-graph', 'figure'),
        dash.dependencies.Input('date-slider', 'value'),
        dash.dependencies.Input('date-slider', 'max'),
    )
    def filter_by_time(dates, maxdate):  
        filtered = df[(df['Date'] > pd.to_datetime(f'{df["Date"].min().year}-01-01')+pd.DateOffset(months=min(dates))) & (df['Date'] <  pd.to_datetime(f'{df["Date"].min().year}-01-01')+pd.DateOffset(months=max(dates)))]
        if filtered.empty:
            if maxdate - min(dates) <= min(dates):
                filtered = df[df['Date'] == df['Date'].max()]
            else:
                filtered = df[df['Date'] == df['Date'].min()]
        #fig = get_heatmap_fig(filtered)
        fig = get_map_fig(filtered) #Currently the way I choose heatmap v Scatterplot
        fig2 = get_dbr_fig(filtered)
        fig3 = get_dmg_fig(filtered)
        return fig, fig2, fig3

    @app.callback(
        dash.dependencies.Output('summary-container', 'children'),
        dash.dependencies.Input('map-graph', 'hoverData'))
    def display_hover_data(hoverData):
        #print(hoverData)
        #print()
        header = html.H4(id='details-header', children='Attack Details')
        if hoverData == None:
            return [header]
        summary = hoverData['points'][0]['customdata'][8]
        injured = hoverData['points'][0]['customdata'][7]
        killed = hoverData['points'][0]['customdata'][6]
        damage = hoverData['points'][0]['customdata'][4]
        damage_note = hoverData['points'][0]['customdata'][5]
        hostages =  hoverData['points'][0]['customdata'][9]
        ransom = hoverData['points'][0]['customdata'][10]

        if hostages == None:
            hostages = 'None reported'
        elif hostages == '0':
            hostages = 'No hostages'

        if ransom == None or ransom < 0:
            ransom = 'No reported ransom'

        if damage == None or damage < 0:
            damage = 'No reported value'
        else:
            damage = f'${damage} USD'

        if injured == None:
            injured = 'None reported'
        elif injured == '0':
            injured = 'No injuries'

        if killed == None:
            killed = 'None reported'
        elif killed == '0':
            killed = 'No deaths'

        if summary == '' or summary == None:
            summary = 'No summary available'

        #print(summary)
        kill_elem = html.Div(id='kill-count-text', children=f'Deaths: {killed}')
        injured_elem = html.Div(id='injured-count-text', children=f'Injuries: {injured}')
        hostages_elem = html.Div(id='hostage-count-text', children=f'Hostages: {hostages}')
        ret_elems = [header,kill_elem, injured_elem, hostages_elem]

        if not (hostages == 'None reported' or hostages =='No hostages'):
            ransom_elem = html.Div(id='ransom-text', children=f'Ransom: {ransom}')
            ret_elems.append(ransom_elem)

        damage_elem = html.Div(id='damage-value-text', children=f'Monetary Damages: {damage}')
        ret_elems.append(damage_elem)

        if not damage_note == None:
            damage_note_elem = html.Div(id='damage-note-text', children=f'Note: {damage_note}')
            ret_elems.append(html.Br())
            ret_elems.append(damage_note_elem)
        summary_elem = html.Div(id='summary-text', children=summary)
        ret_elems.append(html.Br())
        ret_elems.append(summary_elem)

        return ret_elems

    return app

