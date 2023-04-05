import pandas as pd
import numpy as np
import pickle
import json

dfid_topics = pd.read_csv('data/dfid_topics.csv')
dt_sum = pd.read_csv('data/dt_sum.csv')
topic_df = pd.read_csv('data/topic_info.csv')
dfid_topics['ldev'] = np.log(dfid_topics['deviation'])
country_shapes = pd.read_csv('data/country_shapes.csv')
dts = pd.read_csv('data/doctopic.csv')
df = pd.read_csv('data/df_places.csv')
doc_df = pd.read_csv('data/doc_information.csv')

table_df = doc_df.merge(
    dts.pivot(index='doc_id', columns='topic_id', values='score').fillna(0),
    left_on='id',
    right_on='doc_id'
)

with open('data/dfid.geojson', 'r') as f:
    geojson = json.load(f)

heat_dfs = [
    pd.read_csv('data/impact_driver_map.csv'),
    pd.read_csv('data/impact_income_map.csv')
]

m = []
xticks = []
yticks = []

heatfiles = [
    'data/impact_driver_map.pickle',
    'data/impact_income_map.pickle'
]

for fname in heatfiles:
    with open(fname, 'rb') as f:
        p = pickle.load(f)
        m.append(p[0])
        xticks.append(p[1])
        yticks.append(p[2])
