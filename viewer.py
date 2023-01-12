import os
import dash
from dash.dependencies import Input, Output, State
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html
# import dash_auth

from common.utilities import parse_contents


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

PORT = 8050 # Wait for IT response - remove from the src and config in the environment

# Keep this out of source code repository - save in a file or a database
# USERNAME = os.environ['USER_NAME']
# PASSWORD = os.environ['PASSWORD']
# VALID_USERNAME_PASSWORD_PAIRS = {
#     USERNAME: PASSWORD
# }

# For Download Upload From S3
# UPLOAD_DIRECTORY = "uploads"
# BUCKET = os.environ['S3_BUCKET_NAME']
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Authentication
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])

@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents'),
               State('upload-image', 'filename')
              ])
def update_output(images,list_of_names):
    if not images:
        return
    children = [parse_contents(images[i],fname,i) for i,fname in zip(range(len(images)),list_of_names)]
    return children


if __name__ == '__main__':
    app.run_server(debug=True,port=PORT)