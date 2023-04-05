from dash import html, dcc
import dash_bootstrap_components as dbc
from ..instructions import topic_instructions

topic_text = dbc.Col([
    html.P([
        'Explore studies by the topic content ',
        html.A('(more detail)', href='#collapseTopic', style={'font-size': '1rem'}, **{'data-bs-toggle': 'collapse'})
    ], className='lead'),
    html.Div(
        html.Div([
            topic_instructions,
            html.A('less detail', href='#collapseTopic', **{'data-bs-toggle': 'collapse'})
        ], className='card card-body'),
        className='collapse', id='collapseTopic'
    )
], className='mb-3')

topic_tab = dbc.Row(
    dbc.Col(
        [
            topic_text,
            html.Iframe(src='static/difid/index.html', width='100%', height='800px')
        ]
    ),
    className='background-container'
)

tab = dcc.Tab(label='Topic Map', className='col-2', children=[topic_tab])

__all__ = ['tab']
