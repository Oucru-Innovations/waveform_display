from dash import dcc
from dash import html
# import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import base64
import pandas as pd
import io
import numpy as np

from common.utilities import *



def create_chart(data,i):
    zoom_layout = go.Layout(
        yaxis=dict(
            range=[np.min(data)-3000, np.max(data)+3000],
            fixedrange= True
        ),
        xaxis=dict(
            range=[0, 500]
        )
    )
    fig = go.Figure(layout=zoom_layout)
    fig.add_traces(go.Scatter(x=np.arange(1, len(data[0])),
                              y=data[0], mode="lines",
                              name="PPG preprocessed signal"))

    return dcc.Graph(id='graph_'+str(i),figure=fig,style={'height':'400px', 'width':'1200px'})


def parse_img(image_name):
    # test_png = 'test.png'
    image_base64 = base64.b64encode(open(image_name, 'rb').read()).decode('ascii')

    src = 'data:image/png;base64,{}'.format(image_base64)
    return src

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), header=None)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
    except Exception as e:
        print(e)
    return df

def parse_contents(contents,fname,idx=0):
    explanations = [
        "systolic.png",
        "diastolic.png",
        "amplitude.png",
        "AuC.png",
        "dicrotic.png",
        "flat.png",
        "peak_detection.png",
        "peak_detection.png",
        "decision.png"
    ]
    data = parse_data(contents,'csv')
    return html.Div([
        html.Hr(),
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Div(fname),
        create_chart(data,idx),
        html.Hr()
    ])