from dash import html, dcc, callback, Output, Input, __version__, register_page
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
                        html.H1(
                            className="heading-for-all-persona", children="Scholarly Publishing Career Exploration Tool"
                        ),
                    ],
                ),
            ],
        ),
        html.Main(
            className="main-selector",
            children=[
                html.Div(
                    className="persona2-main-div",
                    children=[
                        html.H2(children="Explore Skill Sets", style={"textAlign": "center"}),
                        html.Div(
                            children=[
                                html.Div(
                                    className="selector",
                                    children=[
                                        html.Label(["Career Area"]),
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
                                        html.Label(["Position Level"]),
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
                                        html.Label(["Skill Category"]),
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
                                                """The size of the circle indicates the importance of each skill category. 
                                                    The bigger circles have higher importance for the given career area and the 
                                                    given position level."""
                                            ]
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="selector",
                                    id="skill-selector-1",
                                ),
                                html.Div(
                                    className="selector",
                                    id="skill-selector-2",
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="iframe-selector",
                    children=[
                        html.Label(["Skills you should develop"]),
                        html.Iframe(id="iframe", srcDoc=""),
                    ],
                ),
            ],
        ),
    ],
)


@callback(
    Output(component_id="skill-selector-1", component_property="children"),
    Output(component_id="skill-selector-2", component_property="children"),
    Input(component_id="functional-areas", component_property="value"),
    Input(component_id="decision-making-authorities", component_property="value"),
    Input(component_id="work-attribute-categories", component_property="value"),
)
def update_summary_field(functional_area, decision_making_authority, work_attribute_category):

    df = functions.get_network_data(
        functional_area=functional_area,
        decision_making_authority=decision_making_authority,
        work_attribute_category=work_attribute_category,
    )
    top_5 = df.sort_values(by="weight", ascending=False).iloc[:5]

    skills = []
    for index, source, target, weight in top_5.to_records():
        if "➤ " not in target:
            output_target = html.Li(target)
            if output_target not in skills:
                skills.append(output_target)

    output = f"Within the career area ({functional_area}), in position level ({decision_making_authority}) for skill category ({work_attribute_category}), the top {len(skills)} skills you would need are listed below:"

    return output, skills


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

        return f"""<h1 class="no-data" style="text-align:center;border:1px solid black;
                border-radius:8px;background-color:#d3d3d3;font-family: sans-serif;padding:80px;
                margin:80px;">There is no data to show for this query.</h1>"""

    d3 = D3Blocks(chart="tree", frame=False, support=False)

    d3.set_node_properties(df)

    d3.set_edge_properties(df)

    d3.node_properties.get(work_attribute_category)["color"] = "#3B71FB"

    for index, source, target, weight in df.to_records():
        d3.node_properties.get(target)["size"] = weight
        d3.node_properties.get(target)["color"] = "#3B71FB"
        # d3.node_properties.get(target)["edge_color"] = "#FFCB05"

    tree_html = d3.show(
        filepath=None, figsize=(1024, 550), save_button=False, margin={"left": 200, "top": 10, "right": 0, "bottom": 0}
    )

    return tree_html
