from dash import html, dcc
import dash_bootstrap_components as dbc

logos = [
    'assets/University-of-Leeds-logo.png',
    'assets/lshtm-black.svg',
    'assets/MCC_Logo_RZ_rgb.svg'
]

footer = html.Footer(
    dbc.Container(
        [
            dbc.Row([
                html.Ul([
                    html.Li(html.A(
                        'About',
                        href='https://github.com/mcc-apsis/climate-health-app/wiki'
                    ), className='list-group-item border-0'),
                    html.Li(html.A(
                        'Github',
                        href='https://github.com/mcc-apsis/climate-health-app'
                    ), className='list-group-item border-0'),
                ], className='list-group list-group-horizontal')
            ], className='mb-2'),
            dbc.Row([
                dcc.Markdown(
                    '''
                    The climate and health interactive map is funded by the UK Foreign, Commonwealth
                    & Development Office (FCDO)
                    and carried out by researchers from the University of Leeds, the
                    London School of Health and Tropical Medicine and the Mercator Research Institute
                    on Global Commons and Climate Change.
                    '''
                )
            ]),
            dbc.Row([
                dbc.Col(
                    html.Img(src=logo, height='72px', className='justify-content-center'),
                    className='justify-content-center text-center'
                ) for logo in logos
            ], className='justify-center'),
        ],
        className='container-fluid p-5 p-md-5'
    ),
    className='bd-footer text-muted'
)
__all__ = ['footer']
