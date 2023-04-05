from dash import dash_table, html
import dash_bootstrap_components as dbc

from ..settings import background_color
from ..data import table_df


def make_selection_box(sid, select):
    docTable = dash_table.DataTable(
        id=sid,
        style_cell={
            'font-family': 'Arial',
            'whiteSpace': 'normal',
            'maxHeight': '3em',
            'maxWidth': '8em',
            'textOverflow': 'ellipsis',
            'backgroundColor': background_color,
            'textAlign': 'left'
        },
        filter_action='native',
        style_as_list_view=True,
        columns=[
            {'name': 'Title', 'id': 'title'},
            {'name': 'Place', 'id': 'word'},
            {'name': 'DOI', 'id': 'DOI', 'presentation': 'markdown'}
        ],
        data=table_df.to_dict('records'),
        page_action='native',
        page_current=0,
        page_size=5,
    )

    selectionBox = dbc.Row(
        dbc.Col(
            [
                html.H2('Selection'),
                dbc.Row([
                    dbc.Col([
                        html.H4('Documents'),
                        html.Div(children=[
                            docTable
                        ])
                    ], width=8),
                    dbc.Col([
                        html.H3(select),
                        html.Div([
                            html.Span('No topics selected', id=f'topic-{sid}'),
                            html.Button('Clear topics', id=f'clear-topics-{sid}', className='btn btn-outline-dark m-2')
                        ]),
                    ], width=4)
                ])

            ]
        ),
        className='background-container'
    )
    return selectionBox
