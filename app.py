import os
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from components.tabs.maps import tab as tab_map
from components.tabs.topic_map import tab as tab_topics
from components.tabs.heatmaps import tab as tab_heat
from components.header import header
from components.footer import footer
from components.figures.barchart import draw_bar
from components.figures.map import draw_map
from components.figures.heatmap import draw_heatmap
from components.settings import labels, meta_topics, extents, region_groups, url_req, url_asset, url_routes, url_base
from components.data import doc_df, topic_df, df, table_df, dts, dt_sum, geojson, country_shapes, yticks, \
    xticks, heat_dfs, m

app = dash.Dash(
    __name__,
    title='Climate and Health',
    external_scripts=[
        f'{url_req}{url_asset}assets/js/popper.2.11.7.min.js',
    ],
    external_stylesheets=[
        f'{url_req}{url_asset}assets/css/bootstrap.5.2.3.css',
        f'{url_req}{url_asset}assets/css/computer-modern-web-font/fonts.css'
    ],
    url_base_pathname=url_base,
    requests_pathname_prefix=url_req,
    routes_pathname_prefix=url_routes,
    assets_url_path=url_asset
)

server = app.server

tabs = dcc.Tabs(className='d-flex justify-content-center',
                children=[tab_map, tab_heat, tab_topics])

app.layout = html.Div([
    dbc.Container([
        header,
        dbc.Col(tabs),
    ], id='mainContainer'),
    footer
])


@app.callback(
    [
        Output('bar', 'figure'),
        Output('map', 'figure'),
        Output('map-selection', 'data'),
        Output('topic-map-selection', 'children'),
        Output('map-store', 'data')
    ],
    [
        Input('region-select', 'value'),
        Input('map', 'selectedData'),
        Input('bar', 'clickData'),
        Input('rel_slider', 'value'),
        Input('barfilter-0', 'n_clicks'),
        Input('barfilter-1', 'n_clicks'),
        Input('barfilter-2', 'n_clicks'),
        Input('barfilter-3', 'n_clicks'),
        Input('barfilter-4', 'n_clicks'),
        Input('bar', 'relayoutData'),
        Input('clear-topics-map-selection', 'n_clicks')
    ],
    [
        State('map-store', 'data'),

    ]
)
def region_interaction(
        i, selectedData, clickData, relThreshold,
        bf_0, bf_1, bf_2, bf_3, bf_4,
        relayoutData, clearTopics, storeData):
    rel_ids = doc_df.loc[doc_df['prediction'] >= 1 - relThreshold, 'id']

    ctx = dash.callback_context

    if 'region-select' in ctx.triggered[0]['prop_id']:
        relayoutData = None
        selectedData = None

    topic_selection = 'No topics selected'
    place_ids = []

    # did we just, or have we cleared topics without since clicking on them?
    if 'clear-topics' in ctx.triggered[0]['prop_id']:
        storeData['topics'] = []
        storeData['cleared'] = True

    # have we just clicked on a topic bar
    if 'bar.clickData' in ctx.triggered[0]['prop_id']:
        storeData['cleared'] = False
        if clickData is not None:
            cd = clickData['points'][0]['label']
            if cd in storeData['topics']:
                storeData['topics'] = [x for x in storeData['topics'] if x != cd]
            else:
                storeData['topics'] += [cd]

    topicids = set([])
    for j, bf in enumerate([bf_0, bf_1, bf_2, bf_3, bf_4]):
        if bf is None:
            continue
        elif bf % 2 == 1:
            topicids = topicids | set(topic_df.loc[topic_df['Aggregated meta-topic'] == meta_topics[j], 'id'])

    if selectedData is not None:
        place_ids = [x['id'] for x in selectedData['points'] if 'id' in x]
        if len(place_ids) == 1:
            place = df.loc[df['place_doc_id'] == place_ids[0]]
            place_ids = df.loc[
                (df['lat'] == place.lat.values[0]) &
                (df['lon'] == place.lon.values[0]),
                'place_doc_id'
            ]
        docids = df.loc[df['place_doc_id'].isin(place_ids), 'doc_id']
        rel_df = table_df[
            (table_df['id'].isin(docids)) &
            (table_df['id'].isin(rel_ids))
            ]
    else:
        docids = df.loc[df['DFID region'] == labels[i], 'doc_id']
        rel_df = table_df[
            (table_df['id'].isin(docids)) &
            (table_df['id'].isin(rel_ids))
            ]

    sel_df = df
    sel_df['subset'] = 0
    sel_df.loc[sel_df['id'].isin(rel_df['id']), 'subset'] = 1

    gdt = (sel_df[['id', 'subset']]
           .merge(dts, left_on='id', right_on='doc_id')
           .groupby(['topic_id', 'subset'])['score']
           .sum()
           .reset_index()
           )

    # How many documents are there in each topic
    tns = (
        rel_df[['id']]
        .merge(dts, left_on='id', right_on='doc_id')
        .query('score>0.01')
        .groupby('topic_id')['score']
        .count()
        .to_frame(name='count')
        .sort_values('count')
        .reset_index()
    )

    gdt['share'] = gdt['score'] / gdt.groupby('subset')['score'].transform('sum')
    gdt = gdt.merge(dt_sum)
    gdt['deviation'] = gdt['share'] / gdt['total_share']
    gdt['ldev'] = np.log(gdt['deviation'])
    gdt = gdt[gdt['subset'] == 1]
    if len(topicids) > 0:
        gdt = gdt[gdt.topic_id.isin(topicids)]

    cr = (gdt
          .merge(topic_df, left_on='topic_id', right_on='id')
          .merge(tns, how='left')
          .sort_values('ldev')
          )

    if len(storeData['topics']) > 0:
        topics = topic_df[topic_df['short_title'].isin(storeData['topics'])]['id'].values
        topic_selection = ', '.join(storeData['topics'])
        for top in topics:
            rel_df = rel_df[
                (rel_df[top] > 0.01)
            ]
        rel_df['topics'] = rel_df[topics].sum()
        rel_df = rel_df.sort_values('topics', ascending=False)
        if len(place_ids) > 0:
            place_ids = set(place_ids) & set(df.loc[df['doc_id'].isin(rel_df['id']), 'place_doc_id'])
        else:
            place_ids = set(df.loc[df['doc_id'].isin(rel_df['id']), 'place_doc_id'])

    cr = cr.reset_index(drop=True)
    sbar = cr.loc[cr['short_title'].isin(storeData['topics'])].index

    bar = draw_bar(cr, sbar)

    if 'barfilter' not in ctx.triggered[0]['prop_id']:
        if relayoutData is not None:
            if 'autosize' not in relayoutData:
                if 'xaxis.range[0]' in relayoutData:
                    bar.update_xaxes(range=[
                        relayoutData['xaxis.range[0]'],
                        relayoutData['xaxis.range[1]']
                    ])
                if 'yaxis.range[0]' in relayoutData:
                    bar.update_yaxes(range=[
                        relayoutData['yaxis.range[0]'],
                        relayoutData['yaxis.range[1]']
                    ])

    mapFig, mapTitle = draw_map(
        region_groups[i], extents[i], geojson,
        country_shapes, df[df['id'].isin(rel_ids)], labels[i],
        place_ids
    )

    if rel_df is not None:
        rel_df = rel_df.to_dict('records')

    return bar, mapFig, rel_df, topic_selection, storeData


@app.callback(
    [
        Output('heatmap', 'figure'),
        Output('heatmap-selection', 'data'),
        Output('topic-heatmap-selection', 'children'),
        Output('heatmap-store', 'data')
    ],
    [
        Input('heatmap-select', 'value'),
        Input('heatmap', 'clickData'),
        # Input('rel_slider_heatmap', 'value'),
        Input('bnorm-1', 'n_clicks'),
        Input('bnorm-2', 'n_clicks'),
        Input('bnorm-3', 'n_clicks'),
        Input('clear-topics-heatmap-selection', 'n_clicks')
        # clear topics
    ],
    [
        State('heatmap-store', 'data')
    ]
)
def heatmap_click(
        i, clickData,
        # relThreshold,
        bn1, bn2, bn3, clearTopics, storeData
):
    t1, t2, topic_selection, rel_df = None, None, None, None
    ctx = dash.callback_context

    # rel_ids = doc_df.loc[doc_df['prediction']>=1-relThreshold,'id']

    # did we just, or have we cleared topics without since clicking on them?
    if 'clear-topics' in ctx.triggered[0]['prop_id']:
        clickData = None
        storeData['cleared'] = True
    if ctx.triggered[0]['prop_id'] != 'heatmap.clickData':
        if storeData['cleared']:
            clickData = None
    else:
        storeData['cleared'] = False

    for button, bnorm in zip(['bnorm-1', 'bnorm-2', 'bnorm-3'], [-1, 0, 1]):
        if button in ctx.triggered[0]['prop_id']:
            storeData['bnorm'] = bnorm

    # Have we just or have we since clearing, clicked on a topic combination
    if clickData is not None:
        t1 = clickData['points'][0]['x']
        t2 = clickData['points'][0]['y']
        topic_selection = f'{t1} & {t2}'
        sub_df = heat_dfs[i]
        # sub_df = sub_df[sub_df['id'].isin(rel_ids)]
        if t1 in sub_df.columns and t2 in sub_df.columns:
            thresh = 0.015
            sub_df = sub_df[
                (sub_df[t1] > thresh) &
                (sub_df[t2] > thresh)
                ]
            sub_df['tp'] = sub_df[t1] * sub_df[t2]

            rel_df = (
                sub_df
                .sort_values('tp', ascending=False)
                .reset_index(drop=True)
                .merge(table_df, left_on='doc_id', right_on='id')
            ).to_dict('records')
        else:
            # We must have changed heatmap
            t1, t2, topic_selection = None, None, None

    heatmap = draw_heatmap(m[i], xticks[i], yticks[i], storeData['bnorm'], t1, t2)

    return heatmap, rel_df, topic_selection, storeData


if __name__ == '__main__':
    host = os.getenv('CHA_HOST', '127.0.0.1')
    port = os.getenv('CHA_PORT', 8058)
    debug = os.getenv('CHA_DEBUG', 'off')

    app.run_server(debug=debug == 'on',
                   port=port,
                   host=host)
