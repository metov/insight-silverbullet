# import dash
import time

import dash as dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import *
from cassandra_models import *
from cassandra_utilities import connect_to_cassandra
import numpy as np

# Setup dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Initiate DB connection
connect_to_cassandra()

# Define dashboard elements
graph_asset_stats = dcc.Graph()

# Collect all into single layout
risk_reward_graphs = [(html.Div(children=None, id='risk-reward',
                                style={'display': 'inline-block', 'width': '48%'}))]

app.layout = html.Div([
    (html.H1(children='SilverBullet dashboard', id='title')),
    html.Button('Update', id='button'),
    (html.Div(children=None, id='plots'))])


@app.callback(
    Output('plots', 'children'),
    [Input('button', 'n_clicks')])
def clicks(n_clicks):
    """
    Method to update plots on every button click. While Dash supports more idiomatic live plots, unfortunately it
    does not support them for Cassandra as of now.
    """

    # Collect data
    assets = AssetStat.all()
    a_name = [a.asset for a in assets]
    a_reward = [a.reward for a in assets]
    a_risk = [a.risk for a in assets]
    a_latency = [a.latency for a in assets]

    portfolios = PortfolioStat.all()
    p_reward = [p.reward for p in portfolios]
    p_risk = [p.risk for p in portfolios]
    p_latency = [abs(p.latency) for p in portfolios]

    # Set colors of either value in one place
    color_assets = 'DarkOrange'
    portfolio_color = 'DodgerBlue'

    # Asset stat graph
    graph_asset_stats = dcc.Graph(id='asset-risk-reward',
                                  figure={'data': [go.Scatter(x=a_risk,
                                                              y=a_reward,
                                                              text=a_name, mode='markers',
                                                              marker=dict(line=dict(width=0.5),
                                                                          color=color_assets))],
                                          'layout': go.Layout(title=go.layout.Title(text='Asset statistics'),
                                                              xaxis={'title': 'Risk'}, yaxis={'title': 'Reward'})})

    # Portfolio stat graph
    graph_portfolio_stats = dcc.Graph(id='portfolio-risk-reward',
                                      figure={'data': [go.Scatter(x=p_risk,
                                                                  y=p_reward, mode='markers',
                                                                  marker=dict(line=dict(width=0.5),
                                                                              color=portfolio_color))],
                                              'layout': go.Layout(title=go.layout.Title(text='Portfolio statistics'),
                                                                  xaxis={'title': 'Risk'}, yaxis={'title': 'Reward'},
                                                                  hovermode='closest')})

    # Portfolio stat graph
    graph_latencies = dcc.Graph(id='latency',
                                figure={'data': [go.Scatter(x=list(np.random.rand(len(a_latency)) * 0.5),
                                                            y=a_latency,
                                                            name='Assets',
                                                            mode='markers',
                                                            marker=dict(line=dict(width=0.5),
                                                                        color=color_assets)),
                                                 go.Scatter(x=list(np.random.rand(len(p_latency)) * 0.5 + 1),
                                                            y=p_latency,
                                                            name='Portfolios',
                                                            mode='markers',
                                                            marker=dict(line=dict(width=0.5),
                                                                        color=portfolio_color))],
                                        'layout': go.Layout(title=go.layout.Title(text='Latency'),
                                                            yaxis={'title': 'Latency (ms)'},
                                                            hovermode='closest')})

    # Output graphs
    graphs = [
        (html.Div(children=graph_asset_stats, style={'display': 'inline-block', 'width': '30%'})),
        (html.Div(children=graph_portfolio_stats, style={'display': 'inline-block', 'width': '30%'})),
        (html.Div(children=graph_latencies, style={'display': 'inline-block', 'width': '30%'}))
    ]

    return graphs


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8080, debug=True)
