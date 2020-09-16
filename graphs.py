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
from decimal import Decimal

########################################################################
## Bars

background_color = "#f9f9f9"

def draw_bar(cr, sbar=[]):
    fig = go.Figure(go.Bar(
    #fig = px.bar(
        x=cr["short_title"], y=cr["ldev"],
        hovertemplate = """
Topic: %{x}<br> %{text:.2f} times as common in the region/selection as globally<extra></extra>
        """,
        text=cr["deviation"]
    ))


    # fig.add_trace(go.Scatter(
    #     x=np.where(cr.ldev>0,-0.25,0.25),
    #     y=cr.short_title,
    #     text=cr.short_title,
    #     mode="text",
    #     textposition=np.where(cr.ldev>0,"middle left","middle right")
    # ))
    fig.layout.plot_bgcolor = background_color
    fig.layout.paper_bgcolor = background_color
    tickvals = np.arange(np.log(1/32), np.log(32), np.log(2))
    tickvals = tickvals[(tickvals>cr.ldev.min()) & (tickvals<cr.ldev.max())]
    ticktext = []
    for t in tickvals:
        if t<0:
            ticktext.append(f"1/{2**abs(t/np.log(2)):.0f}")
        else:
            ticktext.append(f"{np.exp(t):.0f}")

    fig.update_yaxes(
        tickmode="array",
        tickvals=tickvals,
        ticktext=ticktext,
        title_text="region share compared to world share"
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
        title_text="",
        categoryorder='array',
        categoryarray=cr.short_title
    )

    marker_line_width = [1] * cr.shape[0]
    marker_opacity = [0.5] * cr.shape[0]
    if len(sbar) > 0:
        for i in sbar:
            marker_line_width[i] = 3
            marker_opacity[i] = 0.8


    fig.update_traces(
        #marker_opacity=0.1,
        marker_line_color="black",
        marker_line_width=marker_line_width,
        marker_opacity=marker_opacity,
        marker_color=cr.color,
        hoverinfo="skip"
        #marker_color="white"
    )
    return fig

###################################################################
## Maps

def draw_map(
    regions, extent, geojson,
    country_shapes, df, label,
    place_ids=[]):
    cs = country_shapes.loc[
        #(country_shapes['DFID priority'] == 1) &
        (country_shapes['UN statistical'].isin(regions))
    ]

    sub_df = df[
        (df["country_predicted"].isin(cs["SOV_A3"])) |
        (df["country_predicted"].isin(cs["ADM0_A3"]))
    ]
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

    if len(place_ids) > 0:
    # Draw points for each study
        unselected = sub_df[~sub_df["place_doc_id"].isin(place_ids)]
        fig.add_trace(go.Scattergeo(
            lon = unselected['lon'],
            lat = unselected['lat'],
            ids = unselected.place_doc_id,
            marker = dict(
                size = 10,
                opacity=0.1,
                line_width=0.5,
            ),
            text=unselected["word"],
            hovertemplate = """%{text}<extra></extra>""",
        ))
        sub_df = sub_df[sub_df["place_doc_id"].isin(place_ids)]
    fig.add_trace(go.Scattergeo(
        lon = sub_df['lon'],
        lat = sub_df['lat'],
        ids = sub_df.place_doc_id,
        marker = dict(
            size = 10,
            opacity=0.5,
            line_width=0.5,
        ),
        text=sub_df["word"],
        hovertemplate = """%{text}<extra></extra>""",
    ))


    fig.update_layout(
        height=500,
        clickmode='event+select',
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
        showlegend=False
    )

    fig.update_geos(
        resolution=50,
        showocean=True,
        oceancolor="rgb(0.59375 , 0.71484375, 0.8828125)",
        lakecolor="rgb(0.59375 , 0.71484375, 0.8828125)",
        rivercolor="rgb(0.59375 , 0.71484375, 0.8828125)",
        landcolor="rgba( 0.9375 , 0.9375 , 0.859375, 0.5)"
    )

    fig.layout.plot_bgcolor = background_color
    fig.layout.paper_bgcolor = background_color

    label = f'{label}, {len(sub_df.id.unique())} studies'

    return fig, label


######################################
### heatmap
import plotly.figure_factory as ff

def draw_heatmap(m, xticks, yticks,norm=-1, t1 = None, t2 = None):
    if norm > -1:
        z = m/m.sum(axis=norm,keepdims=True)
    else:
        z = m
    heatmap = ff.create_annotated_heatmap(
        z,x=xticks,y=yticks,
        annotation_text=m,
        colorscale=px.colors.sequential.YlGnBu,
        xgap=3,
        ygap=3
    )

    heatmap.update_layout(
        height=600,
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=20,
            t=10
        ),
        dragmode="select",

    )

    if "Upper-middle" in xticks:
        heatmap.update_xaxes(
            title_text="Income Category",
            showgrid=False
        )
    else:
        heatmap.update_xaxes(
            title_text="Climate driver",
            showgrid=False
        )
    heatmap.update_yaxes(
        title_text="Health impact",
        showgrid=False
    )

    heatmap.layout.plot_bgcolor = background_color
    heatmap.layout.paper_bgcolor = background_color

    if t1 is not None:
    # Add shapes
        x0 = xticks.index(t1) / len(xticks)
        x1 = x0 + 1 / len(xticks)
        y0 = yticks.index(t2) / len(yticks)
        y1 = y0 + 1 / len(yticks)

        shape = dict(
            type="rect",
            xref="paper",
            yref="paper",
            x0=x0,
            x1=x1,
            y0=y0,
            y1=y1,
            line=dict(color="#ff6347"),
        )

        heatmap.add_shape(shape)

    return heatmap
