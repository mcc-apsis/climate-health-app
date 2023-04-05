from dash import html, dcc
import dash_bootstrap_components as dbc

from ..figures.heatmap import draw_heatmap
from ..instructions import heatmap_instructions
from ..settings import pathway_names
from ..data import m, xticks, yticks
from .util import make_selection_box

pathway_text = dbc.Col([
    html.P([
        'Explore studies in combinations of categories ',
        html.A('(more detail)', href='#collapseHeatmap', style={'font-size': '1rem'}, **{'data-bs-toggle': 'collapse'})
    ], className='lead'),
    html.Div(
        html.Div([
            heatmap_instructions,
            html.A('less detail', href='#collapseHeatmap', **{'data-bs-toggle': 'collapse'})
        ], className='card card-body'),
        className='collapse', id='collapseHeatmap'
    )
], className='mb-3')

pathways = dbc.Row(
    dbc.Col(
        [
            pathway_text,
            dbc.Row(
                dbc.Col([
                    dbc.Row(dbc.Col(
                        dcc.Dropdown(
                            id='heatmap-select',
                            options=[{'label': l, 'value': i} for i, l in enumerate(pathway_names)],
                            value=0
                        ), className='mb-3'
                    )),
                    dbc.Row(dbc.Col([
                        html.Button('No normalisation', id='bnorm-1', className='btn btn-outline-dark m-2'),
                        html.Button('Normalise by column sum', id='bnorm-2', className='btn btn-outline-dark m-2'),
                        html.Button('Normalise by row sum', id='bnorm-3', className='btn btn-outline-dark m-2'),
                    ]), className='mb-3'),
                    dbc.Row(dbc.Col(
                        dcc.Graph(id='heatmap', figure=draw_heatmap(m[0], xticks[0], yticks[0]))
                    ))
                ])
            ),

        ]
    ),
    className='background-container'
)

tab = dcc.Tab(label='Heatmaps', className='col-2', children=[
    pathways,
    make_selection_box('heatmap-selection', 'Categories'),
    dcc.Store(id='heatmap-store', storage_type='memory', data={'cleared': True, 'bnorm': -1}),
])

__all__ = ['tab']
