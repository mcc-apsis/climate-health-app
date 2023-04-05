import plotly.graph_objects as go
import numpy as np
import pandas as pd

from . import background_color


def draw_bar(cr, sbar=None):
    if sbar is None:
        sbar = []
    fig = go.Figure(go.Bar(
        # fig = px.bar(
        x=cr['short_title'], y=cr['ldev'],
        hovertemplate='Topic: %{x}<br> %{text:.2f} times as common in the region/selection as globally<extra></extra>',
        text=cr['deviation']
    ))

    fig.layout.plot_bgcolor = background_color
    fig.layout.paper_bgcolor = background_color
    tickvals = np.arange(np.log(1 / 32), np.log(32), np.log(2))
    tickvals = tickvals[(tickvals > cr.ldev.min()) & (tickvals < cr.ldev.max())]
    ticktext = []
    for t in tickvals:
        if t < 0:
            ticktext.append(f'1/{2 ** abs(t / np.log(2)):.0f}')
        else:
            ticktext.append(f'{np.exp(t):.0f}')

    fig.update_yaxes(
        tickmode='array',
        tickvals=tickvals,
        ticktext=ticktext,
        title_text='region share compared to world share'
    )
    fig.update_layout(
        height=500,
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=10
        ),
        showlegend=False
    )
    fig.update_xaxes(
        showticklabels=False,
        title_text='',
        categoryorder='array',
        categoryarray=cr.short_title
    )

    marker_line_width = [1] * cr.shape[0]
    marker_opacity = [0.5] * cr.shape[0]

    if 'count' in cr.columns:
        marker_opacity = np.where(pd.isna(cr['count']), 0.2, 0.5)
    if len(sbar) > 0:
        for i in sbar:
            marker_line_width[i] = 3
            marker_opacity[i] = 0.8

    fig.update_traces(
        # marker_opacity=0.1,
        marker_line_color='black',
        marker_line_width=marker_line_width,
        marker_opacity=marker_opacity,
        marker_color=cr.color,
        hoverinfo='skip'
        # marker_color='white'
    )
    return fig
