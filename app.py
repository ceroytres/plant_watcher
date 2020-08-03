#! /usr/bin/env python
import os
import webbrowser
import threading
import datetime
import time

import serial

import numpy as np

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
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

@app.callback(
    Output('lux-model', 'figure'),
    [Input('axis-type', 'value')]
)
def plot_lux_model(axis_type):
    
    if axis_type == "Linear":
        R = np.linspace(5, 500, 1000)
    else:
        R = np.linspace(5, 40000, 1000)
    
    lux = lux_model.r2lux(R)
    fig = px.line(x=R, y = lux, labels={'x': r'Resistance (Ω)', 'y': 'Lux (lx)'},
                color_discrete_sequence=[cfg.app.colors['text']],
                line_dash_sequence=['dot'])

    axis_type = "linear" if axis_type == "Linear" else "log"

    fig.update_layout(
        plot_bgcolor=cfg.app.colors['background'],
        paper_bgcolor=cfg.app.colors['background'],
        font_color=cfg.app.colors['text'],
        autosize = False,
        width = 500,
        yaxis_type=axis_type,
        xaxis_type=axis_type
    )

    return fig

@app.callback(
    Output('lux-sensor-output', 'figure'),
    [Input('axis-type-sensor', 'value'),
     Input('interval-component', 'n_intervals')]
)
def plot_lux_sensor(axis_type, n):
    print(axis_type, n)
    x = []
    y = []
    with serial.Serial(**cfg.serial) as ser:
        time.sleep(2)
        start_time = time.time()
        for _ in range(300):
            try:
                val = int(ser.readline().decode().rstrip())
                val = lux_model.v2lux(val/1023 * 5) 
            except:
                
                continue
            x.append(float(time.time() - start_time))
            y.append(val)
            time.sleep(.1)

    
    x = np.array(x)
    y = np.array(y)
    fig = px.line(x= x, y = y, labels={'x': 'Time', 'y': 'Lux (lx)'},
                  color_discrete_sequence=[cfg.app.colors['text']],
                  line_dash_sequence=['dot'])

    axis_type = "linear" if axis_type == "Linear" else "log"

    fig.update_layout(
        plot_bgcolor=cfg.app.colors['background'],
        paper_bgcolor=cfg.app.colors['background'],
        font_color=cfg.app.colors['text'],
        autosize = False,
        width = 500,
        yaxis_type=axis_type
    )

    return fig







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
                                        dcc.Graph(id = 'lux-model', animate = True),
                                        dcc.RadioItems(
                                            id='axis-type',
                                            options=[{'label': i, 'value': i} for i in ['Log', 'Linear']],
                                            value='Log',
                                            labelStyle={'display': 'inline-block'}
                                        )
                            ], className="column"),
                            html.Div([
                                        html.H3("Lux Sensor Output"),
                                        dcc.Graph(id = 'lux-sensor-output'),
                                        dcc.RadioItems(
                                            id='axis-type-sensor',
                                            options=[{'label': i, 'value': i} for i in ['Log', 'Linear']],
                                            value='Log',
                                            labelStyle={'display': 'inline-block'}
                                        ),
                                        dcc.Interval(id='interval-component',
                                                     interval = 45*1000,
                                                     n_intervals = 0
                                                    )
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

