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
    topic_src = 'https://cemac.github.io/DIFID/ui/#'
else:
    p_prefix = '/'
    fig_limit = 2
    topic_src = 'http://0.0.0.0:8000/ui'

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    requests_pathname_prefix=p_prefix,
)

server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    #"bottom": 0,
    "top": "100vh",
    "right": 0,
    "width": "40rem",
    "padding": "4rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-right": "40rem",
    "margin-left": "2rem",
    "padding": "2rem 1rem",
}




dfid_topics = pd.read_csv('data/dfid_topics.csv')
dt_sum = pd.read_csv('data/dt_sum.csv')
topic_df = pd.read_csv('data/topic_info.csv')
dfid_topics["ldev"] = np.log(dfid_topics["deviation"])
country_shapes = pd.read_csv('data/country_shapes.csv')
dts = pd.read_csv('data/doctopic.csv')
df = pd.read_csv("data/dfid_df.csv")

impact_driver_map = pd.read_csv('data/impact_driver_map.csv')

with open("data/dfid.geojson", "r") as f:
    geojson = json.load(f)

with open("data/driver_map.pickle", "rb") as f:
    m, xticks, yticks = pickle.load(f)

region_groups = [
    ["Western Africa"],
    ["Eastern Africa", "Northern Africa","Middle Africa"],
    ["Western Asia"],
    ["Central Asia"],
    ["Southern Asia"],
    ["South-eastern Asia"]

]

labels = [
    "Western Africa",
    "Middle, Eastern and \nNorthern Africa",
    "Western Asia",
    "Central Asia",
    "Southern Asia",
    "South-eastern Asia"
]

extents = [
    [-15,5,0,20],
    [5,55,-30,30],
    [30,60,10,40],
    [66,81,32.5,47.5],
    [59,99,3,43],
    [90,145,-20,30]
]

maps = []
bars = []
sliders = []

titles = []
t0 = time.time()
for i, (regions, extent, label) in enumerate(zip(region_groups, extents,labels)):
    #print(i, time.time()-t0)
    fig, label_n = draw_map(regions, extent, geojson, country_shapes, df, label)
    titles.append(label_n)

    maps.append(fig)

    cr = dfid_topics[dfid_topics["DFID region"]==label]
    bars.append(draw_bar(cr.tail(5)))

    sliders.append(dcc.Slider(
        id={"type":"slider","index": i},
        min=5,
        max=cr.shape[0],
        value=cr.shape[0],
        step=1,
        vertical=True
    ))

    if i >= fig_limit:
        break


##############
## Table data

table_df = df.merge(
    dts.pivot(index="doc_id",columns="topic_id",values="score").fillna(0),
    left_on="id",
    right_on="doc_id"
)

sidebar = html.Div(
    [
        html.H2("Selection"),
        html.H3("Topics"),
        html.Div("No topics selected", id="topic-selection"),
        html.H3("Documents"),
        html.Div(children=[
            dash_table.DataTable(
                id="doc-table",
                style_cell={
                    'whiteSpace': 'normal',
                    'maxHeight': '3em',
                    'maxWidth': '8em',
                    'textOverflow': 'ellipsis'
                },
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                columns=[
                    {"name": "title", "id":"title"},
                    {"name": "DOI", "id": "DOI", "presentation": "markdown"},
                    {"name": "place", "id": "word"}
                ],
                data=table_df.to_dict('records'),
                page_action="native",
                page_current= 0,
                page_size= 5,
            )
        ])
    ],
    style=SIDEBAR_STYLE,
    id="sidebar"
)

navbar = html.Nav(
    [
        html.Ul([
            html.Li(html.A("Climate and Health", href="#", className="nav-link", id="nav-home"),className="nav-item"),
            html.Li(html.A("Regions", href="#regions-map", className="nav-link", id="nav-regions"),className="nav-item"),
            html.Li(html.A("Pathways", href="#pathways", className="nav-link", id="nav-pathways"), className="nav-item"),
            html.Li(html.A("Topics", href="#topic-map",className="nav-link", id="nav-topics"),className="nav-item")
        ], className="nav nav-pills")
    ],
    className="navbar fixed-top navbar-expand navbar-light bg-light justify-content-left",
    id="navbar"
)

graphs = []
for i, fig in enumerate(maps):
    graphs.append(
        dbc.Container([
            dbc.Row([
                html.H3(titles[i],className="m-5")
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id={"type": "map", "index": i}, figure=maps[i]),
                    lg=6
                ),
                dbc.Col(
                    dcc.Graph(id={"type":"bar","index": i}, figure=bars[i]),
                    lg=4
                ),
                dbc.Col(
                    sliders[i],
                    lg=1
                )
            ])
        ])
    )


content = html.Div([
    dbc.Container(
        graphs
    )
] , style=CONTENT_STYLE, id="content")

logos = [
    #'/assets/DfID.png',
    '/assets/University-of-Leeds-logo.png',
    '/assets/lshtm-black.svg',
    '/assets/MCC_Logo_RZ_rgb.jpg'
]

logo_cols = [dbc.Col([html.Img(src=x, height="128em")], lg=4, className="m-4") for x in logos]

topic_content = html.Div([
    html.Iframe(src="http://0.0.0.0:8000/ui/",width="100%",height="1000px")
])


pathway_content = html.Div([
    dbc.Container([
        dbc.Row([
            html.H3("Climate and health pathways",className="m-5"),
        ]),
        dbc.Row([
            html.P([
                html.Button('No normalisation',id="bnorm-1", className="btn btn-outline-dark m-2"),
                html.Button('Normalise by column sum',id="bnorm-2", className="btn btn-outline-dark m-2"),
                html.Button('Normalise by row sum',id="bnorm-3", className="btn btn-outline-dark m-2"),
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="heatmap_1",
                    figure=draw_heatmap(m, xticks, yticks)),
            ])
        ]),
    ],className="mb-5")
], style=CONTENT_STYLE)

pathways_text = dcc.Markdown("""

We grouped the topics above into broaders **climate drivers** and **health impacts** categories

The following "Heatmaps" show the number of documents in each combination of topic.

Click on any cell to see the documents which score highly for both topics.

The cells are coloured by absolute numbers (larger numbers = darker colouring).
Click on the normalise buttons to colour by row proportion or column proportion
""")

app.layout = html.Div([
    navbar,
    html.Div([
        html.Header([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            html.H1("Climate and Health",className="m-5"),
                        ],className="justify-content-center"),
                        dbc.Row([
                            html.H2("A rapid, computer-assisted systematic map of the literature",className="mb-5")
                        ], className="justify-content-center"),
                        dbc.Row([
                            html.H4("Funded by the Department for International Development",className="mb-5")
                        ], className="justify-content-center"),
                        dbc.Row(logo_cols,className="col-12 justify-content-md-center")
                    ],className="col-12 text-center"),
                ], className="h-100 align-items-center"),
            ], className="h-100")
        ], className="masthead"),
        ###### SECTION
        ## SECTIONTITLE
        dbc.Container([
            html.H2(children='Climate and Health studies in DfID priority countries',id="regions-map"),
            html.Div(children='''
                Select a group of studies by dragging a box around them on the maps below.
                Click on the topic bars to filter by topic.
            '''),
        ], className="sectionHeading", id="regions-heading", fluid=True),
        ## SECTIONCONTENT
        html.Div(children=[
            content,
            sidebar
            ]
        ),
        ####### SECTION
        ## SECTIONTITLE
        dbc.Container([
            html.H2(children='Climate and Health Pathways',id="pathways"),
            html.Div(pathways_text),
        ], className="sectionHeading", id="pathways-heading", fluid=True),
        html.Div(children=[
            pathway_content
        ]),
        ####### SECTION
        ## SECTIONTITLE
        dbc.Container([
            html.H2(children='Topic Map of Climate and Health Literature',id="topic-map"),
            html.Div(children='''
                This section maps each individual document as a point in a 2-dimensional representation of the topic space.
                Documents with similar topics are plotted close togther.

                Hover over a document to see its title, and double click to search for it online.
            '''),
        ], className="sectionHeading", id="topic-heading", fluid=True),
        html.Div(children=[
            topic_content
        ])
    ])
])

@app.callback(
    [Output("heatmap_1","figure")],
    [
        Input('bnorm-1','n_clicks'),
        Input('bnorm-2','n_clicks'),
        Input('bnorm-3','n_clicks')
    ]
)
def bnorm_heatmap(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "bnorm-1" in changed_id:
        return [draw_heatmap(m, xticks, yticks,-1)]
    elif "bnorm-2" in changed_id:
        return [draw_heatmap(m, xticks, yticks,0)]
    elif "bnorm-3" in changed_id:
        return [draw_heatmap(m, xticks, yticks,1)]
    return [draw_heatmap(m, xticks, yticks,-1)]

@app.callback(
    [
        Output(component_id="doc-table",component_property='data'),
        Output(component_id="topic-selection", component_property='children'),
    ],
    [
        Input({'type': 'bar', 'index': ALL}, 'clickData'),
        Input({'type': 'map', 'index': ALL}, 'selectedData'),
        Input("heatmap_1", 'clickData')
    ],
)
def bar_click(clickData, selectedData, heatmapClick):
    ctx = dash.callback_context
    t = "No topics selected"
    if not ctx.triggered:
        return [table_df.to_dict('records'), t ]
    else:

        rel_df = table_df

        if "heatmap_1" in ctx.triggered[0]['prop_id']:
            t1 = heatmapClick['points'][0]['x']
            t2 = heatmapClick['points'][0]['y']
            thresh=0.015
            sub_df = impact_driver_map[
                (impact_driver_map[t1]>thresh) &
                (impact_driver_map[t2]>thresh)
            ]
            sub_df["tp"] = sub_df[t1]*sub_df[t2]

            rel_df = (
                sub_df
                .sort_values('tp',ascending=False)
                .reset_index(drop=True)
                .merge(table_df, left_on="doc_id",right_on="id")
            )
            return rel_df.to_dict('records'), f"{t2} & {t1}"

        idx = ast.literal_eval(ctx.triggered[0]['prop_id'].split('.')[0])['index']

        if clickData[idx] is not None:
            t = clickData[idx]["points"][0]["y"]
            topic = topic_df[topic_df["short_title"]==t]["id"].values[0]
            rel_df = table_df[
                (table_df[topic]>0.01) &
                (table_df["DFID region"]==labels[idx])
            ].sort_values(topic,ascending=False)
        if selectedData[idx] is not None:

            ids = [x["id"] for x in selectedData[idx]["points"] if "id" in x]
            rel_df = rel_df[
                (rel_df['place_doc_id'].isin(ids))
            ]
        return [rel_df.to_dict('records'), t]
    return [table_df.to_dict('records'), t]

@app.callback(
    Output({'type': 'bar', 'index': MATCH},'figure'),
    [
        Input({'type': 'slider', 'index': MATCH}, 'value'),
        Input({'type': 'map', 'index': MATCH}, 'selectedData')
    ],
    [State({'type': 'slider', 'index': MATCH}, 'id')]
)
def update_figure(n, selectedData, i):
    i = i['index']
    ctx = dash.callback_context
    cr = dfid_topics[dfid_topics["DFID region"]==labels[i]].head(n).tail(5)
    if selectedData is not None:
        ids = [x["id"] for x in selectedData["points"] if "id" in x]
        rel_df = table_df[
            (table_df['place_doc_id'].isin(ids))
        ]
        sel_df = df
        sel_df["subset"] = 0
        sel_df.loc[sel_df["id"].isin(rel_df["doc_id"]),"subset"]=1
        gdt = (sel_df[["doc_id","subset"]]
               .merge(dts)
               .groupby(['topic_id','subset'])['score']
               .sum()
               .reset_index()
              )
        gdt['share'] = gdt['score'] / gdt.groupby('subset')['score'].transform('sum')
        gdt = gdt.merge(dt_sum)
        gdt['deviation'] = gdt['share'] / gdt['total_share']
        gdt['ldev'] = np.log(gdt['deviation'])
        gdt = gdt[gdt['subset']==1]
        cr = gdt.merge(topic_df, left_on="topic_id",right_on="id").sort_values('ldev').head(n).tail(5)

    fig = draw_bar(cr)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
