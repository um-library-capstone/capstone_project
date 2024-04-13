from dash import html, dcc, callback, Input, Output, register_page, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import re
import random
import functions
from d3blocks import D3Blocks

register_page(__name__)

unique_functional_areas = functions.get_unique_functional_areas()
unique_decision_making_authorities = functions.get_unique_decision_making_authorities()
unique_work_attribute_categories = functions.get_unique_work_attribute_categories()
unique_specific_attribute_categories = functions.get_unique_special_work_attributes()
unique_position_titles = functions.get_unique_position_titles()

layout = html.Div(
    className="whole-page",
    children=[
        html.Header(
            className="header-all-persona",
            id="all-persona",
            children=[
                html.Nav(
                    className="nav-panel",
                    children=[
                        html.A(
                            className="home-icon",
                            href="/",
                            children=[html.Img(src="./assets/home.png"), html.Span("Home")],
                        ),
                        html.H1(className="heading-for-all-persona", children="Scholarly Publishing Career Exploration Tool"),
                    ],
                ),
            ],
        ),
        html.Main(
            className="main-selector",
            children=[
                html.Div(
                    className="persona1-main-div",
                    children=[
                        html.H2(children="Explore Career Options", style={"textAlign": "center"}),
                        html.Div(
                            className="selector-container",
                            children=[
                                html.Div(
                                    className="selector",
                                    children=[
                                        html.Label(["Current Skills:"]),
                                        dcc.Dropdown(
                                            id="specific_skills",
                                            className="drop-down",
                                            options=unique_specific_attribute_categories,
                                            value=["Achievement/Effort"],
                                            multi=True,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="rating-container",
                            children=[
                                html.Div(id="rating-section"),
                                html.Div(  # Wrap the button in a new Div for easier styling
                                    html.Button("Explore Career Areas", id="submit-ratings", n_clicks=0),
                                    style={
                                        "textAlign": "center",
                                        "marginTop": "20px",
                                    },  # Apply text-align style to center the button
                                ),
                            ],
                        ),
                        dcc.Store(id="ratings-store"),
                        html.Div(
                            className="functional-area-out",
                            children=[
                                html.H3(
                                    "Career Areas to Explore:",
                                    style={"textAlign": "center", "marginBottom": "20px"},
                                ),
                                html.Div(id="top-functional-areas-output", style={"textAlign": "center"}),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="iframe-one-selector",
                    children=[
                        html.Label(["Career Areas To Explore"]),
                        html.Iframe(id="iframe-one", srcDoc=""),
                    ],
                ),
            ],
        ),
    ],
)


@callback(
    Output("specific_skills", "value"),
    Input("specific_skills", "value"),
)
def limit_skills_selection(selected_skills):
    limited_skills = selected_skills[:10] if len(selected_skills) > 10 else selected_skills
    return limited_skills


@callback(Output("ratings-store", "data"), Input("submit-ratings", "n_clicks"), State("specific_skills", "value"))
def store_ratings(n_clicks, selected_skills):
    n_clicks = 1
    if n_clicks is None:
        raise PreventUpdate
    return selected_skills


@callback(
    Output("top-functional-areas-output", "children"),
    Output(component_id="iframe-one", component_property="srcDoc"),
    Input("submit-ratings", "n_clicks"),
    State("ratings-store", "data"),
)
def update_dataframe_with_ratings(n_clicks, selected_skills):
    if not n_clicks or not selected_skills:
        raise PreventUpdate

    df = functions.get_data()

    filtered_df = df[(df["Specific Work Attribute"].isin(selected_skills)) & (df["Rating Value"] == 1)]

    df = filtered_df.groupby(["Functional Area"])["Position Title"].count().sort_values(ascending=False)

    output = [html.Li(f"{area}") for area, size in df.items()]

    df = functions.circle_packing_data(selected_skills)

    d3 = D3Blocks(chart="Circlepacking", frame=False, support=False)

    d3.set_node_properties(df)
    d3.set_edge_properties(df)

    circlepacking_html = d3.show(
        filepath=None,
        save_button=False,
        border={'color': '#74d7ca', 'width': 1.5, 'fill': '#74d7ca', "padding": 100},
        # 'wrapwidth': 100
        font = {'size': 20, "type": "sans-serif", 'color': "black", 'outlinecolor': 'none', 'wrapwidth': 50},
        figsize = [1000, 1700],
    )

    circlepacking_html = re.sub(r'<body>', '<body><style>svg {background:white !important;}</style>', circlepacking_html)

    return output, circlepacking_html

