from dash import html, dcc, __version__, register_page

register_page(__name__, path="/")

layout = html.Div(
    [
        html.Header(
            id="home-header",
            children=[
                dcc.Location(id="main-url", refresh=True),
                html.H1(children="Scholarly Publishing Career Exploration Tool"),
            ],
        ),
        html.Div(
            className="page-container",
            children=[
                html.Div(
                    className="home-page-container",
                    id="home-page",
                    children=[
                        html.Div(
                            className="Label-container",
                            id="label-container-id",
                            children=[
                                html.Label(
                                    className="home-page-label",
                                    children=["Select each card below to start exploring different career options!"],
                                ),
                            ],
                        ),
                        # Card Container
                        html.Div(
                            className="card-container",
                            id="card=container-id",
                            children=[
                                # Card 1
                                html.Div(
                                    [
                                        html.A(
                                            href="persona-1",
                                            children=[
                                                html.Img(src="./assets/career_icon.png", alt="Explore Careers"),
                                                html.H2("Explore Career Options"),
                                                html.P(
                                                    "Discover which job categories you are best suited for based on your current skills!"
                                                ),
                                            ],
                                        )
                                    ],
                                    className="card",
                                    id="card-1",
                                ),
                                # Card 2
                                html.Div(
                                    [
                                        html.A(
                                            href="persona-2",
                                            children=[
                                                html.Img(src="./assets/skills_photo.png", alt="Identify Skills"),
                                                html.H2("Explore Skill Sets"),
                                                html.P(
                                                    "Discover which skills you should develop and highlight based on your field of interest!"
                                                ),
                                            ],
                                        )
                                    ],
                                    className="card",
                                    id="card-2",
                                ),
                                # Card 3
                                html.Div(
                                    [
                                        html.A(
                                            href="persona-3",
                                            children=[
                                                html.Img(src="./assets/advancement_icon.png", alt="Career Advancement"),
                                                html.H2("Explore Career Advancement"),
                                                html.P(
                                                    "Find out what skills you should develop to advance your career and find out about other fields that might be a fit!"
                                                ),
                                            ],
                                        )
                                    ],
                                    className="card",
                                    id="card-3",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ]
)
