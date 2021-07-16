# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os
import sys
import warnings
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
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, title='NLP Contract Analytics', update_title=None, external_stylesheets=external_stylesheets)

cols = ['Group', 'Entity text', 'Score']
df = pd.DataFrame(data=[['','','']], columns=cols)

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

app.layout = html.Div(children=[
    html.H1(children='NLP Contract Analytics Project'),

    html.H4(children='''
        by Robert Juhasz | Galvanize RPP2
    '''),

    html.Br(),
    dcc.Textarea(
        id='textarea-example',
        placeholder='Enter text here...',
        value='',
        autoFocus='true',
        style={'width': '70%', 'height': 200}),
    
    html.Br(),
    html.Button('Analyze text', id='button'),

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
    Output(component_id='textarea-example-output', component_property='children'),
    Output(component_id='table', component_property='data'),
    Input(component_id='button', component_property='n_clicks'),
    State('textarea-example', 'value')
)
def update_output(n_clicks, value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        # summarization | Bart model with Pytorch
        summarizer_pyt = pipeline("summarization")
        summary_pyt = summarizer_pyt(value, min_length=5, max_length=100)
        
        # entity extraction
        tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)
        ner_results = nlp(value)
        df = ner_categories(ner_results,10)
        data=df.to_dict('records')
        return next(iter(summary_pyt[0].values())), data


'''
SUMMARIZATION with Huggingface Transformers
'''

# summarization | t5-base model with TensorFlow
# summarizer_tf = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
# summary_tf = summarizer_tf(value, min_length=5, max_length=100)


# print(format_results(summary_pyt, 'Summary by Bart model with Pytorch'))
# print(format_results(summary_tf, 'Summary by t5-base model with TensorFlow'))


'''
ENTITY EXTRACTION with Huggingface Transformers
'''


# tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
# model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

# nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)

# ner_results = nlp(value)
# df = ner_categories(ner_results)


if __name__ == '__main__':
    app.run_server(debug=True)