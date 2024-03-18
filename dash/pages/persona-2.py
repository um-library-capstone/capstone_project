from dash import html, dcc, callback, Output, Input, __version__, register_page
import plotly.express as px
import functions
from d3blocks import D3Blocks

register_page(__name__)

unique_functional_areas = functions.get_unique_functional_areas()
unique_decision_making_authorities = functions.get_unique_decision_making_authorities()
unique_work_attribute_categories = functions.get_unique_work_attribute_categories()

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
                    children=[
                        html.Div(
                            className="selector",
                            children=[
                                html.Label(["Functional Area"]),
                                dcc.Dropdown(
                                    id="functional-areas",
                                    className="drop-down",
                                    options=unique_functional_areas,
                                    value=unique_functional_areas[0],
                                ),
                            ],
                        ),
                        html.Div(
                            className="selector",
                            children=[
                                html.Label(["Decision Making Authority"]),
                                dcc.Dropdown(
                                    id="decision-making-authorities",
                                    className="drop-down",
                                    options=unique_decision_making_authorities,
                                    value=unique_decision_making_authorities[0],
                                ),
                            ],
                        ),
                        html.Div(
                            className="selector",
                            children=[
                                html.Label(["Work Attribute Categories"]),
                                dcc.Dropdown(
                                    id="work-attribute-categories",
                                    className="drop-down",
                                    options=unique_work_attribute_categories,
                                    value=unique_work_attribute_categories[0],
                                ),
                            ],
                        ),
                        html.Div(
                            className="selector",
                            id="p-selector",
                            children=[
                                html.P(
                                    [
                                    '''The size of the circle indicates the importance of each work attribute category. 
                                    The bigger circles have higher importance for the given functional area and the given tier level.'''
                                    ]
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="iframe-selector",
                    children=[
                        html.Label(["Skills You Should Have"]),
                        html.Iframe(id="iframe", srcDoc=""),
                    ],
                ),
            ],
        ),
    ],
)


@callback(
    Output(component_id="iframe", component_property="srcDoc"),
    Input(component_id="functional-areas", component_property="value"),
    Input(component_id="decision-making-authorities", component_property="value"),
    Input(component_id="work-attribute-categories", component_property="value"),
)
def update_graph(functional_area, decision_making_authority, work_attribute_category):

    print(functional_area, decision_making_authority, work_attribute_category)

    df = functions.get_network_data(
        functional_area=functional_area,
        decision_making_authority=decision_making_authority,
        work_attribute_category=work_attribute_category,
    )

    print(df.shape)

    if df.shape[0] == 0:

        return f"""<h1 class="no-data" style="text-align:center;border:2px solid black;font-family: sans-serif;padding:10px;">Your query did not turn up any data.</h1>"""

    d3 = D3Blocks(chart="tree", frame=False, support=False)

    d3.set_node_properties(df)

    d3.set_edge_properties(df)

    d3.node_properties.get(work_attribute_category)["color"] = "red"

    for index, source, target, weight in df.to_records():
        d3.node_properties.get(target)["size"] = weight
        d3.node_properties.get(target)["color"] = "#FFCB05"
        d3.node_properties.get(target)["edge_color"] = "#00274C"

    tree_html = d3.show(
        filepath=None, figsize=(1024, 550), save_button=False, margin={"left": 200, "top": 10, "right": 0, "bottom": 0}
    )

    return tree_html
