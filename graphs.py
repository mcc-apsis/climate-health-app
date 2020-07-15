import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go
import textwrap
import dash_bootstrap_components as dbc
import numpy as np
import ast
import time
from dash.dependencies import Input, Output, State, MATCH, ALL
import os
import pandas as pd
import json
import pickle

########################################################################
## Bars

def draw_bar(cr):
    fig = px.bar(
        cr, y="short_title", x="ldev",
        #text="short_title"
    )

    fig.add_trace(go.Scatter(
        x=np.where(cr.ldev>0,-0.25,0.25),
        y=cr.short_title,
        text=cr.short_title,
        mode="text",
        textposition=np.where(cr.ldev>0,"middle left","middle right")
    ))
    fig.layout.plot_bgcolor = 'white'
    fig.layout.paper_bgcolor = 'white'
    fig.update_xaxes(
        tickmode="array",
        tickvals=np.log([0.125,0.25,0.5,1,2,4,8]),
        ticktext=["1/8","1/4","1/2","1","2","4","8"],
        title_text="region share/world share"
    )
    fig.update_layout(
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=10,
            t=0
        ),
         xaxis_range=[
            min(np.log(0.125),cr.ldev.min()),max(np.log(8),cr.ldev.max())
        ],
        showlegend=False
    )
    fig.update_yaxes(
        showticklabels=False,
        title_text=""
    )

    fig.update_traces(
        #marker_opacity=0.1,
        marker_line_color="black",
        marker_line_width=1,
        marker_color="white"
    )
    return fig

###################################################################
## Maps

def draw_map(regions, extent, geojson, country_shapes, df, label):
    cs = country_shapes.loc[
        (country_shapes['DFID priority'] == 1) &
        (country_shapes['UN statistical'].isin(regions))
    ]

    sub_df = df[df["country_predicted"].isin(cs["SOV_A3"])]
    fig = go.Figure()

    # Colour DFID priority countries in the region
    fig.add_trace(go.Choropleth(
        locations = cs["SOV_A3"],
        geojson=geojson,
        z=cs["DFID priority"],
        featureidkey='properties.id',
        colorscale = [[0, "#fed9a6"], [1, "#fed9a6"]],
        showscale=False,
    ))

    # Draw points for each study
    fig.add_trace(go.Scattergeo(
        lon = sub_df['lon'],
        lat = sub_df['lat'],
        ids = sub_df.place_doc_id,
        marker = dict(
            size = 10,
            opacity=0.5,
            line_width=0.5,
        )
    ))

    fig.update_layout(
        #height=500,
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=10,
            t=0
        ),
        geo = go.layout.Geo(
            lonaxis_range=extent[0:2],
            lataxis_range=extent[2:],
            showcountries = True,
        ),
        dragmode="select",
        showlegend=None
    )

    fig.update_geos(
        resolution=50,
        showocean=True,
        oceancolor="rgb(0.59375 , 0.71484375, 0.8828125)",
        lakecolor="rgb(0.59375 , 0.71484375, 0.8828125)",
        rivercolor="rgb(0.59375 , 0.71484375, 0.8828125)",
        landcolor="rgba( 0.9375 , 0.9375 , 0.859375, 0.5)"
    )

    label = f'{label}, {len(sub_df.id.unique())} studies'

    return fig, label


######################################
### heatmap
import plotly.figure_factory as ff

def draw_heatmap(m, xticks, yticks,norm=-1):
    if norm > -1:
        z = m/m.sum(axis=norm,keepdims=True)
    else:
        z = m
    heatmap = ff.create_annotated_heatmap(
        z,x=xticks,y=yticks,
        annotation_text=m,
        colorscale=px.colors.sequential.YlGnBu
    )

    heatmap.update_layout(
        height=600,
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=10,
            t=0
        ),
        dragmode="select",
    )

    return heatmap
