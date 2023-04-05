from dash import html
import dash_bootstrap_components as dbc

header = dbc.Row(
    [
        dbc.Col(html.Div()),
        dbc.Col(
            html.Div(html.H1('Climate and Health', className='mt-4'))
        ),
        dbc.Col(html.Div())
    ],
    id='header',
)

__all__ = ['header']
