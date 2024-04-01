from dash import html, dcc, callback, Input, Output, register_page, State
from dash.exceptions import PreventUpdate
import random
import functions
from d3blocks import D3Blocks

register_page(__name__)

unique_functional_areas = functions.get_unique_functional_areas()
unique_decision_making_authorities = functions.get_unique_decision_making_authorities()
unique_work_attribute_categories = functions.get_unique_work_attribute_categories()
unique_specific_attribute_categories = functions.get_unique_special_work_attributes()

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
                        html.H1(className="heading-for-all-persona", children="Skills Map Dashboard"),
                    ],
                ),
            ],
        ),
        html.Main(
            className="main-selector",
            children=[
                html.Div(
                    [
                        html.H2(children="Persona 1", style={"textAlign": "center"}),
                        html.Div(
                            className="selector-container",
                            children=[
                                html.Div(
                                    className="selector",
                                    children=[
                                        html.Label(["Skills that I have:"]),
                                        dcc.Dropdown(
                                            id="specific_skills",
                                            className="drop-down",
                                            options=unique_specific_attribute_categories,
                                            value=[],
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
                                    html.Button("Find my Functional Areas", id="submit-ratings", n_clicks=0),
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
                                    "Your Functional Areas to Explore:",
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
                        html.Label(["Areas You Should Explore"]),
                        html.Iframe(id="iframe-one", srcDoc="",),
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
    if n_clicks is None or n_clicks < 1:
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

    top_5 = filtered_df.groupby("Functional Area").size().sort_values(ascending=False).head(5)

    output = [html.Li(f"{area}: {size}") for area, size in top_5.items()]

    top_5_df = top_5.to_frame()

    top_5_df = top_5_df.reset_index().rename(columns={0: "weight", "Functional Area": "target"})

    top_5_df["source"] = "Functional Areas"

    top_5_df["weight"] = top_5_df["weight"].apply(lambda x: x / 5)

    d3 = D3Blocks(chart="Circlepacking", frame=False, support=False)

    d3.set_node_properties(top_5_df, size="sum")

    d3.set_edge_properties(top_5_df)

    for target in top_5_df["target"].unique():
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if target in d3.node_properties:
            d3.node_properties[target]["color"] = color

    circlepacking_html = d3.show(
        filepath=None,
        save_button=False,
        margin={"left": 200, "top": 10, "right": 0, "bottom": 0},
        zoom="mouseover",
        speed=1500,
        border={'color': '#FFFFFF', 'width': 1.5, 'fill': '#F2C83F', "padding": 10},
    )

    return output, circlepacking_html
