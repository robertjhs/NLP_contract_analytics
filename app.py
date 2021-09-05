# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os
import sys
import warnings
import base64
from numpy.core.fromnumeric import size
import pandas as pd

import transformers
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification

import dash
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
from dash_html_components import Br
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
# from src import ocr
import cv2
import pdf2image as p2i
import pytesseract as pt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, title='Contract Analytics | NLP', update_title=None, external_stylesheets=[dbc.themes.BOOTSTRAP])

cols = ['Group', 'Entity text', 'Score']
df = pd.DataFrame(data=[['','','']], columns=cols)

# OCR
def ocr_process(data):
    content_type, content_string = data.split(',')
    decoded = base64.b64decode(content_string)
    doc = p2i.convert_from_bytes(decoded)
    whole_txt = ''
    for page_number, page_data in enumerate(doc):
        txt = pt.image_to_string(page_data)
        whole_txt += txt
    return whole_txt

# convert results to a Pandas dataframe
def ner_categories(ner,max_cols=5):
    df = pd.DataFrame(data=ner)
    df.drop(['start','end'], axis=1, inplace=True)
    new_df = df.groupby('word').max().sort_values('score', ascending=False)
    new_df.reset_index(inplace=True)
    new_df['score'] = new_df['score'].apply(lambda x: round(x,3))
    new_df.columns = ['Entity text', 'Group', 'Score']
    return new_df[:max_cols]


# create html table from dataframe
def generate_table(dataframe, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app.layout = dbc.Container(children=[
    dbc.NavbarSimple(brand='Contract Analytics with Natural Language Processing', color='dark', dark=True, style={'font-size': '80px', 'font-weight': 'bold', 'height': '80px'}),

    html.H6('created by Robert Juhasz', style={'font-style': 'italic'}),

    html.Br(),

    dcc.Upload(
        id='upload-data',
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
        },
    ),

    html.Br(),

    dcc.Loading(
        dcc.Textarea(
            id='textarea-example',
            placeholder='Upload file or enter text here...',
            value='',
            autoFocus='true',
            style={'width': '100%', 'height': 150}),
        type='dot'
    ),

    dcc.RadioItems(
        id='radio_summarizer',
        options=[{'label': 'BART model | Pytorch', 'value': 'pyt'},
                 {'label': 'T5-base model | TensorFlow', 'value': 'tf'}],
        value='pyt'
    ),  

    html.Br(),
    # html.Button('Analyze text', id='button'),
    dbc.Button('Analyze Contract', color='primary', className='mr-1', id='button'),

    html.Br(),
    html.Br(),
    html.H4(children='Summary:'),

    dcc.Loading(
            id="loading",
            type="dot",
            children=[
                html.Div(id='textarea-example-output', style={'width': '70%', 'whiteSpace': 'pre-line'})
                ]),
    
    html.Br(),
    html.H4(children='Entities extracted:'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'width': '50%'},
        style_cell={'width': 'auto'})

])


@app.callback(
    Output('textarea-example', 'value'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
)
def update_output(contents, filename):
    if contents is not None:
        return ocr_process(contents)


@app.callback(
    Output(component_id='textarea-example-output', component_property='children'),
    Output(component_id='table', component_property='data'),
    Input(component_id='button', component_property='n_clicks'),
    State('radio_summarizer', 'value'),
    State('textarea-example', 'value')
)
def update_output(n_clicks, radio_summarizer, text):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # summarization
        if radio_summarizer == 'pyt':
            summarizer = pipeline("summarization")
            summary = summarizer(text, min_length=5, max_length=100)
        elif radio_summarizer == 'tf':
            summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
            summary = summarizer(text, min_length=5, max_length=100)
        
        # entity extraction
        tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)
        ner_results = nlp(text)
        if len(ner_results) > 0:        
            df = ner_categories(ner_results,10)
        else:
            df = pd.DataFrame(data=[['','','']])
        data=df.to_dict('records')
                
        return next(iter(summary[0].values())), data


if __name__ == '__main__':
    app.run_server(debug=True)