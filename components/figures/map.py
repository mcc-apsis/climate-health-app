import plotly.graph_objects as go
from . import background_color


def draw_map(regions, extent, geojson, country_shapes, df, label, place_ids=None):
    if place_ids is None:
        place_ids = []

    cs = country_shapes.loc[
        (country_shapes['UN statistical'].isin(regions))
    ]

    sub_df = df[
        (df["country_predicted"].isin(cs["SOV_A3"])) |
        (df["country_predicted"].isin(cs["ADM0_A3"]))
        ]
    fig = go.Figure()

    # Colour DFID priority countries in the region
    fig.add_trace(go.Choropleth(
        locations=cs["SOV_A3"],
        geojson=geojson,
        z=cs["DFID priority"],
        featureidkey='properties.id',
        colorscale=[[0, "#fed9a6"], [1, "#fed9a6"]],
        showscale=False,
    ))

    if len(place_ids) > 0:
        # Draw points for each study
        unselected = sub_df[~sub_df["place_doc_id"].isin(place_ids)]
        fig.add_trace(go.Scattergeo(
            lon=unselected['lon'],
            lat=unselected['lat'],
            ids=unselected.place_doc_id,
            marker=dict(
                size=10,
                opacity=0.1,
                line_width=0.5,
            ),
            text=unselected["word"],
            hovertemplate="""%{text}<extra></extra>""",
        ))
        sub_df = sub_df[sub_df["place_doc_id"].isin(place_ids)]
    fig.add_trace(go.Scattergeo(
        lon=sub_df['lon'],
        lat=sub_df['lat'],
        ids=sub_df.place_doc_id,
        marker=dict(
            size=10,
            opacity=0.5,
            line_width=0.5,
        ),
        text=sub_df["word"],
        hovertemplate="""%{text}<extra></extra>""",
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
        geo=go.layout.Geo(
            lonaxis_range=extent[0:2],
            lataxis_range=extent[2:],
            showcountries=True,
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
