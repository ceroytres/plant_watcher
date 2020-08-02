#! /usr/bin/env python
import os
import webbrowser
import threading
import datetime

import serial

import numpy as np

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

from omegaconf import OmegaConf
from hydra.experimental import initialize, compose

from plant_watcher.models import LuxModel

#Load configuration settings
initialize(config_dir='config')
cfg = compose(config_file='config.yaml')
  
print('Configuration Settings...')
print(cfg.pretty())

app = dash.Dash(__name__, title=cfg.app.name, external_stylesheets=['/assets/style.css'],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

lux_model = LuxModel(**cfg.lux_model)
R = np.linspace(5, 20000, 1000)
lux = lux_model.r2lux(R)

fig = px.line(x=R, y = lux, labels={'x': r'Resistance (Ω)', 'y': 'Lux (lx)'},
            color_discrete_sequence=[cfg.app.colors['text']],
            line_dash_sequence=['dot'])


fig.update_layout(
    plot_bgcolor=cfg.app.colors['background'],
    paper_bgcolor=cfg.app.colors['background'],
    font_color=cfg.app.colors['text'],
    autosize = False,
    width = 600,
    yaxis_type="log",
    xaxis_type="log"
)

app.layout=html.Div([
                        #Header
                        html.Div([
                                    html.H1(cfg.app.name, style = {'textAlign': 'center'}),
                                    html.H3("Watch my plant!", style = {'textAlign': 'center'})
                        ]),
                        #Graph
                        html.Div([
                            html.Div([
                                        html.H3("Resistance to Lux Model"),
                                        dcc.Graph(figure=fig, id = 'lux_model')

                            ], className="column"),
                            html.Div([
                                        html.H3("Resistance to Lux Model"),
                                        dcc.Graph(figure=fig, id = 'lux_model2')

                            ], className="column")                            
                        ], className="row")

                        ])



def open_browser():
    webbrowser.open(cfg.browser.url)

if __name__ == "__main__":

    if cfg.browser.open:
        threading.Timer(1, open_browser).start()

    app.run_server(host = cfg.server.host, port = cfg.server.port,
                debug = cfg.server.debug)

