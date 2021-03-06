import os
import pickle
import copy
import datetime as dt
import pandas as pd
import numpy as np
from flask import Flask
from flask_cors import CORS
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS

app = dash.Dash(__name__)
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
server = app.server
CORS(server)

#if 'DYNO' in os.environ:
#    app.scripts.append_script({
#        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'  # noqa: E501
#    })

# Create global chart template
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'  # noqa: E501

#df = np.random.randn(1000,3)
data = pd.read_csv('../wyns/data/tweet_global_warming.csv', encoding="latin")
data['existence2'] = data['existence'].fillna('unrelated')
df1 = np.random.rand(len(data),5)
#print(df['existence2'].unique())

layout = dict(
    autosize=True,
    height=800,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="dark",
        center=dict(
            lon=-98.4842,
            lat=39.0119
        ),
        zoom=3,
    ),
    updatemenus= [
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 3,
                                    'mapbox.center.lon': '-98.4842',
                                    'mapbox.center.lat': '39.0119',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Reset Zoom',
                            method='relayout'
                        )
                    ]),
                    direction='left',
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    type='buttons',
                    x=0.45,
                    xanchor='left',
                    yanchor='bottom',
                    bgcolor='#323130',
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(
                        color="#FFFFFF"
                    ),
                    y=0.02
                ),
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 8,
                                    'mapbox.center.lon': '-95.3698',
                                    'mapbox.center.lat': '29.7604',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Houston',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 8,
                                    'mapbox.center.lon': '-87.6298',
                                    'mapbox.center.lat': '41.8781',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Chicago',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 5,
                                    'mapbox.center.lon': '-86.9023',
                                    'mapbox.center.lat': '32.3182',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Alabama',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 8,
                                    'mapbox.center.lon': '-74.0113',
                                    'mapbox.center.lat': '40.7069',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='New York City',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 8,
                                    'mapbox.center.lon': '-122.3321',
                                    'mapbox.center.lat': '47.6062',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Seattle',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 7,
                                    'mapbox.center.lon': '-118.2437',
                                    'mapbox.center.lat': '34.0522',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Los Angeles',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 5,
                                    'mapbox.center.lon': '-86.5804',
                                    'mapbox.center.lat': '35.5175',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Tennessee',
                            method='relayout'
                        )
                    ]),
                    direction="down",
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(50, 49, 48, 0)",
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#FFFFFF"
                    ),
                    x=0,
                    y=0.05
                )
            ]
)


# Create app layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    'WYNS - Global Warming Sentiment ¯\_(ツ)_/¯',
                    #color='#CCCCCC'
                    className='eight columns',
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.H5(
                    '',
                    id='well_text', #change to no. tweets selected
                    className='two columns'
                ),
                html.H5(
                    '',
                    id='production_text', #get rid of this
                    className='eight columns', #
                    style={'text-align': 'center'} #
                ),
                html.H5(
                    '',
                    id='year_text', #change to years of tweets selected
                    className='two columns',
                    style={'text-align': 'right'}
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.P('Filter by tweet date (or select range in histogram):'),  # noqa: E501
                dcc.RangeSlider(
                    id='year_slider',
                    min=0,
                    max=len(data),
                    value=[500,4500]
                ),
             dcc.Checklist(
                            id='lock_selector', #keep this to lock location
                            options=[
                                {'label': 'Lock camera', 'value': 'locked'}
                            ],
                            values=[],
                        )
            ],
            style={'margin-top': '20'}

        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='main_graph')
                    ],
                    className='eight columns',
                    style={'margin-top': '20'}
                ),
                html.Div(
                    [
                        dcc.Graph(id='individual_graph')
                    ],
                    className='four columns',
                    style={'margin-top': '20'}
                ),
            ],
            className='row'
        ),
    ],
    className='ten columns offset-by-one'
)

# functions that help with cleaning / filtering data

TWIT_TYPES = dict(
    Yes = '#76acf2',
    Y = '#76acf2',
    No = '#e85353',
    N = '#e85353',
    unrelated = '#efe98d'
)

# start the callbacks
# Main Graph -> update
# The below code makes a map which colors by 'existence' and hence required pre-classification
#@app.callback(Output('main_graph', 'figure'),
#              [Input('year_slider', 'value')],
#             [State('lock_selector', 'values'),
#              State('main_graph', 'relayoutData')])
#def make_main_figure(year_slider, selector, main_graph_layout):
#
#    length = len(df)
#    df2 = np.random.rand(length,2)
#    traces = []
#    for existence, dff in df.groupby('existence2'):
#        length = len(dff)
#        df2 = np.random.rand(length,2)
#        trace = dict(
#            type='scattermapbox',
#            lon=df2[:,0]-122.45,
#            lat=df2[:,1]+47.62,
#            text = dff['tweet'],
#    #            text=twit[0],
#            customdata=df2[:,0],
#            name=df2[:,0],
#            marker=dict(
#                size=4,
#                opacity=0.6,
#                color=TWIT_TYPES[existence]
#            )
#        )
#        traces.append(trace)
#
#    if (main_graph_layout is not None and 'locked' in selector):
#        lon = float(main_graph_layout['mapbox']['center']['lon'])
#        lat = float(main_graph_layout['mapbox']['center']['lat'])
#        zoom = float(main_graph_layout['mapbox']['zoom'])
#        layout['mapbox']['center']['lon'] = lon
#        layout['mapbox']['center']['lat'] = lat
#        layout['mapbox']['zoom'] = zoom
#    else:
#        lon = -122.45,
#        lat = 47.62
#        zoom = 7
#
#    figure = dict(data=traces, layout=layout)
#    return figure

# Main Graph -> update
# the below code uses a heatmap to render the
@app.callback(Output('main_graph', 'figure'),
              [Input('year_slider', 'value')],
             [State('lock_selector', 'values'),
              State('main_graph', 'relayoutData')])
def make_main_figure(year_slider, selector, main_graph_layout):
    df = data.iloc[year_slider[0]:year_slider[1]]
    df2 = df1[year_slider[0]:year_slider[1],:]
#    length = len(df)
#    df2 = np.random.rand(length,5) # 2 locations and 3 one-hot encoded values
    traces = [dict(
        type='scattermapbox',
        lon = df2[:,0]*50-120.3698,
        lat = df2[:,1]*20+27.6648,
        text = df['tweet'],
    #            text=twit[0],
        customdata=df2[:,0],
        name=df2[:,0],
        marker=dict(
            size=4,
            opacity=0.8,
            color = df2[:,3],
            colorbar = dict(
                title='Belief'
            ),
            colorscale = [[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'], [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]
        ),

    )]


    if (main_graph_layout is not None and 'locked' in selector):
#        print(main_graph_layout)
        try:
            lon = float(main_graph_layout['mapbox']['center']['lon'])
            lat = float(main_graph_layout['mapbox']['center']['lat'])
            zoom = float(main_graph_layout['mapbox']['zoom'])
            layout['mapbox']['center']['lon'] = lon
            layout['mapbox']['center']['lat'] = lat
            layout['mapbox']['zoom'] = zoom
        except:
            print(main_graph_layout)
            lon = float(main_graph_layout['mapbox.center.lon'])
            lat = float(main_graph_layout['mapbox.center.lat'])
            zoom = float(main_graph_layout['mapbox.zoom'])
            layout['mapbox']['center']['lon'] = lon
            layout['mapbox']['center']['lat'] = lat
            layout['mapbox']['zoom'] = zoom
    else:
        lon = -122.45,
        lat = 47.62
        zoom = 7

    figure = dict(data=traces, layout=layout)
    return figure

# Slider -> year text
@app.callback(Output('year_text', 'children'),
              [Input('year_slider', 'value')])
def update_year_text(year_slider):
    return "{} | {}".format(year_slider[0], year_slider[1])

# Slider / Selection -> individual graph
@app.callback(Output('individual_graph', 'figure'),
              [Input('main_graph', 'selectedData'),
              Input('year_slider', 'value')])
def make_individual_figure(main_graph_data, year_slider):
    df = data.iloc[year_slider[0]:year_slider[1]]
    df2 = df1[year_slider[0]:year_slider[1],:]
    layout_individual = copy.deepcopy(layout)
    layout_individual['title'] = 'Histogram from index %i to %i' % (year_slider[0], year_slider[1])
    layout_individual['updatemenus'] = []
    # custom histogram code:
    hist = np.histogram(df2[:,3], bins=10)
    traces = [dict(
        type='bar',
        x = hist[1][:-1],
        y = hist[0],
        marker = dict(
            color = hist[1][:-1],
            colorscale = [[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'], [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]
        ),
    )]

    figure = dict(data=traces, layout=layout_individual)
    return figure







# Main
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)


