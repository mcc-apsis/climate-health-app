import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from . import background_color


def draw_heatmap(m, xticks, yticks, norm=-1, t1=None, t2=None):
    if norm > -1:
        z = m / m.sum(axis=norm, keepdims=True)
    else:
        z = m
    heatmap = ff.create_annotated_heatmap(
        z, x=xticks, y=yticks,
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
