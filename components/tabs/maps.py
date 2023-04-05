from dash import html, dcc
import dash_bootstrap_components as dbc

from ..instructions import graph_instructions, relevance_explanation
from ..figures.map import draw_map
from ..figures.barchart import draw_bar
from ..settings import region_groups, extents, labels, colors, meta_topics
from ..data import geojson, df, country_shapes, dfid_topics
from .util import make_selection_box

i = 0

slider_marks = {
    round(x * 0.05, 2): f'{1 - x * 0.05:.2f}' for x in range(1, 15)
}

slider_marks[0] = '1.00'

mapFig, mapTitle = draw_map(
    region_groups[i], extents[i], geojson, country_shapes, df, labels[i]
)

cr = (
    dfid_topics[dfid_topics['DFID region'] == labels[i]]
    .sort_values('ldev')
    .reset_index()
)

bar = draw_bar(cr)

bar_buttons = []
for j, meta_topic in enumerate(meta_topics):
    bar_buttons.append(
        html.Button(
            meta_topic,
            id=f'barfilter-{j}',
            style={'background-color': colors[j], 'font-size': '1rem'},
            className='btn btn-outline-dark m-1 p-1 cbutton'
        )
    )

graph_text = dbc.Col([
    html.P([
        'Explore studies by the places and topics they mention ',
        html.A('(more detail)', href='#collapseMap', style={'font-size': '1rem'}, **{
            'data-bs-toggle': 'collapse',
            'role': 'button',
            'aria-expanded': 'false',
            'aria-controls': 'collapseMap'
        })
    ], className='lead'),
    html.Div(
        html.Div([
            graph_instructions,
            html.A('less detail', href='#collapseMap', **{
                'data-bs-toggle': 'collapse',
                'role': 'button',
                'aria-expanded': 'false',
                'aria-controls': 'collapseMap'
            })
        ], className='card card-body'),
        className='collapse', id='collapseMap'
    )
], className='mb-3 p-0')

graphs = dbc.Row(
    dbc.Col([
        graph_text,
        dbc.Row([
            dbc.Col([
                html.P('Filter by predicted relevance score   '),
                html.Img(
                    src='assets/question-diamond-fill.svg',
                    alt='',
                    title='Predicted relevance',
                    **{
                        'data-container': 'body', 'data-bs-toggle': 'popover',
                        'data-placement': 'right', 'data-bs-content': relevance_explanation
                    },
                    style={'height': '1.3em'},
                    className='ml-1'
                )
            ]),
            dbc.Col([
                dcc.Slider(
                    id='rel_slider',
                    min=0.00,
                    max=.65,
                    value=.65,
                    step=.05,
                    marks=slider_marks
                )
            ], className='mb-2')
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='region-select',
                    options=[{'label': l, 'value': i} for i, l in enumerate(labels)],
                    value=0
                ), width=6
            ),
            dbc.Col(
                ['Click to filter topics by type: '] + bar_buttons,
                width=6
            )
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='map', figure=mapFig, config={
                'topojsonURL': 'assets/'
            }), width=6),
            dbc.Col(dcc.Graph(id='bar', figure=bar), width=6)
        ])

    ]),
    className='background-container'
)

tab = dcc.Tab(label='Maps', children=[
    graphs,
    make_selection_box('map-selection', 'Topics'),
    dcc.Store(id='map-store', storage_type='memory', data={'topics': [], 'cleared': True}),
], className='tab-first col-2')

__all__ = ['tab']
