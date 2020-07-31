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

import instructions

from graphs import draw_bar, draw_map, draw_heatmap

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

external_scripts = [
    "https://code.jquery.com/jquery-3.5.1.js",
    'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.bundle.min.js',
]

external_stylesheets = [
    "https://cdn.rawgit.com/dreampulse/computer-modern-web-font/master/fonts.css",
    dbc.themes.BOOTSTRAP
]

if "/var/www" in abspath:
    p_prefix = '/climate-health/'
    fig_limit = 100
    topic_src = 'https://cemac.github.io/DIFID/ui/'
else:
    p_prefix = '/'
    fig_limit = 1
    topic_src = 'https://cemac.github.io/DIFID/ui/'
    #topic_src = 'http://0.0.0.0:8000/ui'

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    requests_pathname_prefix=p_prefix,
)

server = app.server

background_color = "#f9f9f9"
# LOAD DATA

dfid_topics = pd.read_csv('data/dfid_topics.csv')
dt_sum = pd.read_csv('data/dt_sum.csv')
topic_df = pd.read_csv('data/topic_info.csv')
dfid_topics["ldev"] = np.log(dfid_topics["deviation"])
country_shapes = pd.read_csv('data/country_shapes.csv')
dts = pd.read_csv('data/doctopic.csv')
#df = pd.read_csv("data/dfid_df.csv")
df = pd.read_csv("data/df_places.csv")
doc_df = pd.read_csv("data/doc_information.csv")

##############
## Table data

table_df = doc_df.merge(
    dts.pivot(index="doc_id",columns="topic_id",values="score").fillna(0),
    left_on="id",
    right_on="doc_id"
)


with open("data/dfid.geojson", "r") as f:
    geojson = json.load(f)

heat_dfs = [
    pd.read_csv('data/impact_driver_map.csv'),
    pd.read_csv('data/impact_income_map.csv')
]

m = []
xticks = []
yticks = []

heatfiles = [
    "data/impact_driver_map.pickle",
    "data/impact_income_map.pickle"
]

pathway_names = [
    "Climate and health pathways",
    "Impact and income categories"
]

for fname in heatfiles:
    with open(fname, "rb") as f:
        p = pickle.load(f)
        m.append(p[0])
        xticks.append(p[1])
        yticks.append(p[2])

colors = ["#fed9a6","#fbb4ae","#ccebc5","#b3cde3","#bdbdbd"]
meta_topics = ["Health impact", "Exposure", "Intervention option", "Mediating pathways","Other"]

region_groups = [
    ["Western Africa"],
    ["Eastern Africa", "Northern Africa","Middle Africa"],
    ["Western Asia"],
    ["Central Asia","Southern Asia"],
    ["South-eastern Asia"]
]

labels = [
    "Western Africa",
    "Middle, Eastern and Northern Africa",
    "Western Asia",
    "Central and Southern Asia",
    "South-eastern Asia"
]

extents = [
    [-20,12,-2.5,27.5],
    [0,60,-30,30],
    [25,65,10,45],
    [45,104,3,48],
    [85,150,-20,30]
]

t0 = time.time()

i = 0

map, mapTitle = draw_map(
    region_groups[i], extents[i], geojson, country_shapes, df, labels[i]
)

cr = (
    dfid_topics[dfid_topics["DFID region"]==labels[i]]
    .sort_values('ldev')
    .reset_index()
)

bar = draw_bar(cr)



logos = [
    #'/assets/DfID.png',
    '/assets/University-of-Leeds-logo.png',
    '/assets/lshtm-black.svg',
    '/assets/MCC_Logo_RZ_rgb.jpg'
]

logo_cols = [dbc.Col([html.Img(src=x, height="128em")], lg=4, className="m-4") for x in logos]


header = dbc.Row(
    [
        dbc.Col(
            html.Div()
            ,
        ),
        dbc.Col(
            html.Div(
                html.H1("Climate and Health")
            )
            ,
        ),
        dbc.Col(
            html.Div()
            ,
        )
    ],
    id="header",
)

bar_buttons = []
for j, meta_topic in enumerate(meta_topics):
    bar_buttons.append(
        html.Button(
            meta_topic,
            id=f"barfilter-{j}",
            style={"background-color": colors[j], "font-size":"1rem"},
            className="btn btn-outline-dark m-1 p-1 cbutton"
        )
    )



graph_text = dbc.Col([
    html.P([
        "Explore studies by the places and topics they mention ",
        html.A("(more detail)", href="#collapseMap", style={"font-size": "1rem"}, **{"data-toggle": "collapse"})
    ],className="lead"),
    html.Div(
        html.Div([
            instructions.graph_instructions,
            html.A("less detail", href="#collapseMap", **{"data-toggle": "collapse"})
        ], className="card card-body"),
        className="collapse", id="collapseMap"
    )
], className="mb-3 p-0")

graphs = dbc.Row(
    dbc.Col([
        graph_text,
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id = "region-select",
                    options = [{"label":l, 'value':i} for i,l in enumerate(labels)],
                    value=0
                ), width=6
            ),
            dbc.Col(
                ["Click to filter topics by type: "] + bar_buttons,
                width=6
            )
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="map", figure=map), width=6),
            dbc.Col(dcc.Graph(id="bar", figure=bar), width=6)
        ])

    ]),
    className="background-container"
)

pathway_text = dbc.Col([
    html.P([
        "Explore studies in combinations of categories ",
        html.A("(more detail)", href="#collapseHeatmap", style={"font-size": "1rem"}, **{"data-toggle": "collapse"})
    ],className="lead"),
    html.Div(
        html.Div([
            instructions.heatmap_instructions,
            html.A("less detail", href="#collapseHeatmap", **{"data-toggle": "collapse"})
        ], className="card card-body"),
        className="collapse", id="collapseHeatmap"
    )
], className="mb-3")

pathways = dbc.Row(
    dbc.Col(
        [
            pathway_text,
            dbc.Row(
                dbc.Col([
                    dbc.Row(dbc.Col(
                        dcc.Dropdown(
                            id="heatmap-select",
                            options = [{'label': l, 'value':i} for i, l in enumerate(pathway_names)],
                            value = 0
                        ),className="mb-3"
                    )),
                    dbc.Row(dbc.Col([
                        html.Button('No normalisation',id="bnorm-1" , className="btn btn-outline-dark m-2"),
                        html.Button('Normalise by column sum',id="bnorm-2", className="btn btn-outline-dark m-2"),
                        html.Button('Normalise by row sum',id="bnorm-3", className="btn btn-outline-dark m-2"),
                    ]),className="mb-3" ),
                    dbc.Row(dbc.Col(
                        dcc.Graph(id="heatmap", figure=draw_heatmap(m[0],xticks[0],yticks[0]))
                    ))
                ])
            ),

        ]
    ),
    className="background-container"
)

topic_text = dbc.Col([
    html.P([
        "Explore studies by the topic content ",
        html.A("(more detail)", href="#collapseTopic", style={"font-size": "1rem"}, **{"data-toggle": "collapse"})
    ],className="lead"),
    html.Div(
        html.Div([
            instructions.heatmap_instructions,
            html.A("less detail", href="#collapseTopic", **{"data-toggle": "collapse"})
        ], className="card card-body"),
        className="collapse", id="collapseTopic"
    )
], className="mb-3")

topic_tab = dbc.Row(
    dbc.Col(
        [
            topic_text,
            html.Iframe(src=topic_src,width="100%",height="800px")
        ]
    ),
    className="background-container"
)

def make_selection_box(id, tselect):
    docTable = dash_table.DataTable(
        id=id,
        style_cell={
            'font-family': 'Arial',
            'whiteSpace': 'normal',
            'maxHeight': '3em',
            'maxWidth': '8em',
            'textOverflow': 'ellipsis',
            'backgroundColor': background_color,
            'textAlign': 'left'
        },
        filter_action="native",
        style_as_list_view=True,
        columns=[
            {"name": "Title", "id":"title"},
            {"name": "Place", "id": "word"},
            {"name": "DOI", "id": "DOI", "presentation": "markdown"}
        ],
        data=table_df.to_dict('records'),
        page_action="native",
        page_current= 0,
        page_size= 5,
    )

    selectionBox = dbc.Row(
        dbc.Col(
            [
                html.H2("Selection"),
                dbc.Row([
                    dbc.Col([
                        html.H4("Documents"),
                        html.Div(children=[
                            docTable
                        ])
                    ], width=8),
                    dbc.Col([
                        html.H3(tselect),
                        html.Div([
                            html.Span("No topics selected", id=f"topic-{id}"),
                            html.Button("Clear topics", id=f"clear-topics-{id}", className="btn btn-outline-dark m-2")
                        ]),
                    ],width=4)
                ])

            ]
        ),
        className="background-container"
    )
    return selectionBox



tabs = dcc.Tabs(
    className='d-flex justify-content-center',
    children = [
        dcc.Tab(label="Maps", children=[
            graphs,
            make_selection_box("map-selection", "Topics"),
            dcc.Store(id="map-store", storage_type="memory", data = {"topics": [], "cleared": True}),
        ],className="tab-first col-2"),
        dcc.Tab(label="Heatmaps", className="col-2", children=[
            pathways,
            make_selection_box("heatmap-selection", "Categories"),
            dcc.Store(id="heatmap-store", storage_type="memory",data={"cleared": True, "bnorm":-1}),
        ]),
        dcc.Tab(label="Topic Map", className="col-2", children= [
            topic_tab

        ]
    )
])

app.layout = dbc.Container([
    header,
    dbc.Col(tabs),
], id="mainContainer")


@app.callback(
    [
        Output("bar", "figure"),
        Output("map", "figure"),
        Output("map-selection", "data"),
        Output("topic-map-selection", "children"),
        Output("map-store", "data")
    ],
    [
        Input("region-select", "value"),
        Input("map", "selectedData"),
        Input("bar", "clickData"),
        Input("barfilter-0", "n_clicks"),
        Input("barfilter-1", "n_clicks"),
        Input("barfilter-2", "n_clicks"),
        Input("barfilter-3", "n_clicks"),
        Input("barfilter-4", "n_clicks"),
        Input("bar", "relayoutData"),
        Input('clear-topics-map-selection', 'n_clicks')
    ],
    [
        State("map-store", "data"),

    ]
)
def region_interaction(
    i, selectedData, clickData,
    bf_0, bf_1, bf_2, bf_3, bf_4,
    relayoutData, clearTopics, storeData):

    ctx = dash.callback_context

    if "region-select" in ctx.triggered[0]['prop_id']:
        relayoutData = None
        selectedData = None

    topic_selection = "No topics selected"
    place_ids = []
    rel_df = None

    # did we just, or have we cleared topics without since clicking on them?
    if "clear-topics" in ctx.triggered[0]['prop_id']:
        storeData["topics"] = []
        storeData["cleared"] = True


    # have we just clicked on a topic bar
    if "bar.clickData" in ctx.triggered[0]['prop_id']:
        storeData["cleared"] = False
        if clickData is not None:
            cd = clickData["points"][0]["label"]
            if cd in storeData["topics"]:
                storeData["topics"] = [x for x in storeData["topics"] if x!= cd]
            else:
                storeData["topics"] += [cd]


    # Filter topics to just include those in the metacategories selected
    sub_topics = dfid_topics[dfid_topics["DFID region"]==labels[i]]
    topicids = set([])
    for j, bf in enumerate([bf_0, bf_1, bf_2, bf_3, bf_4]):
        if bf is None:
            continue
        elif bf%2==1:
            topicids = topicids | set(topic_df.loc[topic_df['Aggregated meta-topic']==meta_topics[j],"id"])

    if len(topicids)>0:
        sub_topics = sub_topics[sub_topics.topic_id.isin(topicids)]

    cr = (
        sub_topics
        .sort_values('ldev')
        .reset_index()
    )

    if selectedData is not None:
        place_ids = [x["id"] for x in selectedData["points"] if "id" in x]
        if len(place_ids)==1:
            place = df.loc[df['place_doc_id']==place_ids[0]]
            place_ids = df.loc[
                (df['lat']==place.lat.values[0]) &
                (df['lon']==place.lon.values[0]),
                "place_doc_id"
            ]
        docids = df.loc[df['place_doc_id'].isin(place_ids),"doc_id"]
        rel_df = table_df[
            (table_df['id'].isin(docids))
        ]
        sel_df = df
        sel_df["subset"] = 0
        sel_df.loc[sel_df["id"].isin(rel_df["id"]),"subset"]=1

        gdt = (sel_df[["id","subset"]]
               .merge(dts, left_on="id",right_on="doc_id")
               .groupby(['topic_id','subset'])['score']
               .sum()
               .reset_index()
              )
        gdt['share'] = gdt['score'] / gdt.groupby('subset')['score'].transform('sum')
        gdt = gdt.merge(dt_sum)
        gdt['deviation'] = gdt['share'] / gdt['total_share']
        gdt['ldev'] = np.log(gdt['deviation'])
        gdt = gdt[gdt['subset']==1]
        if len(topicids)>0:
            gdt = gdt[gdt.topic_id.isin(topicids)]
        cr = gdt.merge(topic_df, left_on="topic_id",right_on="id").sort_values('ldev')

    else:
        docids = df.loc[df['DFID region']==labels[i],"doc_id"]
        rel_df = table_df[
            (table_df["id"].isin(docids))
        ]

    if len(storeData["topics"]) > 0:
        topics = topic_df[topic_df["short_title"].isin(storeData["topics"])]["id"].values
        topic_selection = ", ".join(storeData["topics"])
        for top in topics:
            rel_df = rel_df[
                (rel_df[top]>0.01)
            ]
        rel_df["topics"] = rel_df[topics].sum()
        rel_df = rel_df.sort_values("topics",ascending=False)
        if len(place_ids) > 0:
            place_ids = set(place_ids) & set(df.loc[df["doc_id"].isin(rel_df["id"]), "place_doc_id"])
        else:
            place_ids = set(df.loc[df["doc_id"].isin(rel_df["id"]), "place_doc_id"])




    cr = cr.reset_index(drop=True)
    sbar = cr.loc[cr["short_title"].isin(storeData["topics"])].index

    bar = draw_bar(cr, sbar)

    if "barfilter" not in ctx.triggered[0]['prop_id']:
        if relayoutData is not None:
            if "autosize" not in relayoutData:
                if "xaxis.range[0]" in relayoutData:
                    bar.update_xaxes(range=[
                        relayoutData["xaxis.range[0]"],
                        relayoutData["xaxis.range[1]"]
                    ])
                if "yaxis.range[0]" in relayoutData:
                    bar.update_yaxes(range=[
                        relayoutData["yaxis.range[0]"],
                        relayoutData["yaxis.range[1]"]
                    ])



    map, mapTitle = draw_map(
        region_groups[i], extents[i], geojson,
        country_shapes, df, labels[i],
        place_ids
    )

    if rel_df is not None:
        rel_df = rel_df.to_dict('records')

    return bar, map, rel_df, topic_selection, storeData

@app.callback(
    [
        Output("heatmap", "figure"),
        Output("heatmap-selection", "data"),
        Output("topic-heatmap-selection", "children"),
        Output("heatmap-store", "data")
    ],
    [
        Input("heatmap-select", "value"),
        Input("heatmap", 'clickData'),
        Input('bnorm-1', 'n_clicks'),
        Input('bnorm-2', 'n_clicks'),
        Input('bnorm-3', 'n_clicks'),
        Input('clear-topics-heatmap-selection', 'n_clicks')
        # clear topics
    ],
    [
        State("heatmap-store", "data")
    ]
)
def heatmap_click(i, clickData, bn1, bn2, bn3, clearTopics, storeData):
    t1, t2, topic_selection, rel_df = None, None, None, None
    ctx = dash.callback_context

    # did we just, or have we cleared topics without since clicking on them?
    if "clear-topics" in ctx.triggered[0]['prop_id']:
        clickData = None
        storeData["cleared"] = True
    if ctx.triggered[0]['prop_id'] != "heatmap.clickData":
        if storeData["cleared"]:
            clickData = None
    else:
        storeData["cleared"] = False

    for button, bnorm in zip(["bnorm-1","bnorm-2","bnorm-3"],[-1,0,1]):
        if button in ctx.triggered[0]['prop_id']:
            storeData["bnorm"] = bnorm

    # Have we just or have we since clearing, clicked on a topic combination
    if clickData is not None:
        t1 = clickData['points'][0]['x']
        t2 = clickData['points'][0]['y']
        topic_selection = f"{t1} & {t2}"
        sub_df = heat_dfs[i]
        if t1 in sub_df.columns and t2 in sub_df.columns:
            thresh=0.015
            sub_df = sub_df[
                (sub_df[t1]>thresh) &
                (sub_df[t2]>thresh)
            ]
            sub_df["tp"] = sub_df[t1]*sub_df[t2]

            rel_df = (
                sub_df
                .sort_values('tp',ascending=False)
                .reset_index(drop=True)
                .merge(table_df, left_on="doc_id",right_on="id")
            ).to_dict('records')
        else:
            # We must have changed heatmap
            t1, t2, topic_selection = None, None, None

    heatmap = draw_heatmap(m[i], xticks[i], yticks[i], storeData["bnorm"], t1, t2)

    return heatmap, rel_df, topic_selection, storeData


if __name__ == '__main__':
    app.run_server(debug=True)
