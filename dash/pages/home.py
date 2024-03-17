from dash import html, dcc, __version__, register_page, callback, Input, Output, State
from dash.exceptions import PreventUpdate

register_page(__name__, path="/")

layout = html.Div(
    [
        html.Header(
            id="home-header",
            children=[
                dcc.Location(id="main-url", refresh=True),
                html.H1(children="Skills Map Dashboard"),
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
                            className='Label-container', id='label-container-id',
                            children=[
                                html.Label(
                                    className="home-page-label",
                                    children=["What would you like to do today?"],
                                ),
                            ]
                        ),
                        dcc.RadioItems(
                            id="career-options",
                            options={
                                "persona-1": "Explore new career options based on my current skills",
                                "persona-2": "Identify necessary skills for the career I want to enter",
                                "persona-3": "Explore career advancement opportunities",
                            },
                        ),
                        html.Button(id="button", children="Explore", n_clicks=0),
                    ],
                ),
            ],
        ),
    ]
)


@callback(
    Output(component_id="main-url", component_property="pathname"),
    Input(component_id="button", component_property="n_clicks"),
    State(component_id="career-options", component_property="value"),
    prevent_initial_call=True,
)
def update_page(n_clicks, selected_option):
    if selected_option is None:
        raise PreventUpdate
    return selected_option
