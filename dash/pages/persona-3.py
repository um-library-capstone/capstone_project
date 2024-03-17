from dash import html, register_page

register_page(__name__)

layout = html.Div(
    className="whole-page",
    children=[
        html.Header(
            className="header-all-persona", id="all-persona",
            children=[
                html.Nav(
                    className="nav-panel",
                    children=[
                        html.A(
                            className="home-icon",
                            href="/",
                            children=[html.Img(src="./assets/home.png"), html.Span("Home")],
                        ),
                        html.H1(className="heading-for-all-persona", children="Skills Map Dashboard"),
                    ],
                ),
            ],
        ),
        html.Main(
            className='main-selector',
            children=[
                html.H2(className="persona-text", children=["Persona 3"]),
                html.Div(children=[

                ]),
            ],
            ),
    ],
)
