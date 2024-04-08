from dash import html, dcc, callback, Output, Input, __version__, register_page, no_update
from dash.exceptions import PreventUpdate
import functions

register_page(__name__)

unique_functional_areas = functions.get_unique_functional_areas()
unique_decision_making_authorities = functions.get_unique_decision_making_authorities()
unique_work_attribute_categories = functions.get_unique_work_attribute_categories()
unique_specific_work_attribute_categories = functions.get_unique_special_work_attributes()

df = functions.get_data_for_job_description_table()


def generate_table(dataframe):
    columns_to_keep = [
        "Position Title",
        "Multifunctional Responsibilities",
        "Career Area",
        "Product Area",
        "Position Level",
        "Years of Experience",
        "Education Credentials",
    ]

    dataframe = dataframe[columns_to_keep].drop_duplicates(keep="last")

    return html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in dataframe.columns[:10]])),
            html.Tbody(
                [
                    html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns[:10]])
                    for i in range((len(dataframe)))
                ]
            ),
        ]
    )


def update_dataframe_with_ratings(selected_skills):
    if not selected_skills:
        raise PreventUpdate

    try:
        df = functions.rename_columns()

        print(f"DataFrame before filtering: {df.head()}")

        filtered_df = df[(df["Specific Skill"].isin(selected_skills)) & (df["Rating Value"] == 1)]

        if filtered_df.empty:
            print("Filtered DataFrame is empty. Check selected skills and rating values.")
            return []

        top_3 = filtered_df.groupby("Career Area").size().sort_values(ascending=False).head(3)
        top_3_df = top_3.to_frame()
        top_3_areas = top_3_df.index.tolist()
        print(f"Top 3 career areas: {top_3_areas}")

        return top_3_areas
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


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
                    children=[
                        html.Div(
                            className="selector",
                            children=[
                                html.Label(["Current Career Area"]),
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
                                html.Label(["Specific Skill"]),
                                dcc.Dropdown(
                                    id="specific-work-attribute-categories",
                                    className="drop-down",
                                    options=unique_specific_work_attribute_categories,
                                    value=unique_specific_work_attribute_categories[0],
                                    multi=True,
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
                    ],
                ),
                html.Div(
                    className="functional-areas-container",
                    children=[
                        html.Div(
                            className="functional-area-column",
                            children=[
                                html.Label(
                                    ["Current Career Area"],
                                    style={"font-weight": "bold", "display": "block", "margin-bottom": "10px"},
                                ),
                                dcc.Dropdown(
                                    id="current-functional-area",
                                    className="drop-down",
                                    options=unique_functional_areas,
                                    value=unique_functional_areas[0],
                                ),
                                dcc.Dropdown(
                                    id="current-tier",
                                    className="drop-down",
                                    options=unique_decision_making_authorities,
                                    value=unique_decision_making_authorities[0],
                                ),
                                html.P(id="skill-1-1"),
                                html.P(id="skill-1-2"),
                                html.P(id="skill-1-3"),
                                html.P(id="skill-1-4"),
                                html.P(id="skill-1-5"),
                            ],
                        ),
                        html.Div(
                            className="functional-area-column",
                            children=[
                                html.Label(
                                    ["Career Area 1"],
                                    style={"font-weight": "bold", "display": "block", "margin-bottom": "10px"},
                                ),
                                dcc.Dropdown(
                                    id="functional-area",
                                    className="drop-down",
                                    options=unique_functional_areas,
                                    value=unique_functional_areas[0],
                                ),
                                dcc.Dropdown(
                                    id="tier-two",
                                    className="drop-down",
                                    options=unique_decision_making_authorities,
                                    value=unique_decision_making_authorities[1],
                                ),
                                html.P(id="skill-1"),
                                html.P(id="skill-2"),
                                html.P(id="skill-3"),
                                html.P(id="skill-4"),
                                html.P(id="skill-5"),
                            ],
                        ),
                        html.Div(
                            className="functional-area-column",
                            children=[
                                html.Label(
                                    ["Career Area 2"],
                                    style={"font-weight": "bold", "display": "block", "margin-bottom": "10px"},
                                ),
                                dcc.Dropdown(
                                    id="functional-area-two",
                                    className="drop-down",
                                    options=unique_functional_areas,
                                    value=unique_functional_areas[0],
                                ),
                                dcc.Dropdown(
                                    id="tier-three",
                                    className="drop-down",
                                    options=unique_decision_making_authorities,
                                    value=unique_decision_making_authorities[2],
                                ),
                                html.P(id="skill-3-1"),
                                html.P(id="skill-3-2"),
                                html.P(id="skill-3-3"),
                                html.P(id="skill-3-4"),
                                html.P(id="skill-3-5"),
                            ],
                        ),
                        html.Div(
                            className="functional-area-column",
                            children=[
                                html.Label(
                                    ["Career Area 3"],
                                    style={"font-weight": "bold", "display": "block", "margin-bottom": "10px"},
                                ),
                                dcc.Dropdown(
                                    id="functional-area-three",
                                    className="drop-down",
                                    options=unique_functional_areas,
                                    value=unique_functional_areas[0],
                                ),
                                dcc.Dropdown(
                                    id="tier-four",
                                    className="drop-down",
                                    options=unique_decision_making_authorities,
                                    value=unique_decision_making_authorities[3],
                                ),
                                html.P(id="skill-4-1"),
                                html.P(id="skill-4-2"),
                                html.P(id="skill-4-3"),
                                html.P(id="skill-4-4"),
                                html.P(id="skill-4-5"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="table-container",
            className="skills-table-container",
            children=[
                html.H4("Job Descriptions Based on Your Skills and Career Area"),
                html.Div(
                    id="scrollable-table-container",
                    className="scrollable-table-container",
                    children=[generate_table(df)],
                    style={"maxHeight": "500px", "overflowY": "scroll"},
                ),
            ],
        ),
    ],
)


@callback(
    [
        Output("skill-1-1", "children"),
        Output("skill-1-2", "children"),
        Output("skill-1-3", "children"),
        Output("skill-1-4", "children"),
        Output("skill-1-5", "children"),
    ],
    [
        Input("current-functional-area", "value"),
        Input("current-tier", "value"),
        Input("work-attribute-categories", "value"),
    ],
)
def update_skills_1(functional_area, tier, work_attribute):
    df = functions.rename_columns()

    filtered_df = df[
        (df["Career Area"] == functional_area)
        & (df["Position Level"] == tier)
        & (df["Rating Value"] == 1)
        & (df["Skill Category"] == work_attribute)
    ]

    skills = filtered_df["General Skill"].unique().tolist()[:5]

    skills.extend([""] * (5 - len(skills)))
    return skills


@callback(
    [
        Output("skill-1", "children"),
        Output("skill-2", "children"),
        Output("skill-3", "children"),
        Output("skill-4", "children"),
        Output("skill-5", "children"),
    ],
    [Input("functional-area", "value"), Input("tier-two", "value"), Input("work-attribute-categories", "value")],
)
def update_skills_2(functional_area, tier, work_attribute):
    df = functions.rename_columns()

    filtered_df = df[
        (df["Career Area"] == functional_area)
        & (df["Position Level"] == tier)
        & (df["Rating Value"] == 1)
        & (df["Skill Category"] == work_attribute)
    ]

    skills = filtered_df["General Skill"].unique().tolist()[:5]

    skills.extend([""] * (5 - len(skills)))

    return skills


@callback(
    [
        Output("skill-3-1", "children"),
        Output("skill-3-2", "children"),
        Output("skill-3-3", "children"),
        Output("skill-3-4", "children"),
        Output("skill-3-5", "children"),
    ],
    [Input("functional-area-two", "value"), Input("tier-three", "value"), Input("work-attribute-categories", "value")],
)
def update_skills_3(functional_area, tier, work_attribute):
    df = functions.rename_columns()
    filtered_df = df[
        (df["Career Area"] == functional_area)
        & (df["Position Level"] == tier)
        & (df["Rating Value"] == 1)
        & (df["Skill Category"] == work_attribute)
    ]

    skills = filtered_df["General Skill"].unique().tolist()[:5]

    skills.extend([""] * (5 - len(skills)))
    return skills


@callback(
    [
        Output("skill-4-1", "children"),
        Output("skill-4-2", "children"),
        Output("skill-4-3", "children"),
        Output("skill-4-4", "children"),
        Output("skill-4-5", "children"),
    ],
    [Input("functional-area-three", "value"), Input("tier-four", "value"), Input("work-attribute-categories", "value")],
)
def update_skills_4(functional_area, tier, work_attribute):
    df = functions.rename_columns()
    filtered_df = df[
        (df["Career Area"] == functional_area)
        & (df["Position Level"] == tier)
        & (df["Rating Value"] == 1)
        & (df["Skill Category"] == work_attribute)
    ]

    skills = filtered_df["General Skill"].unique().tolist()[:5]

    skills.extend([""] * (5 - len(skills)))

    return skills


@callback(
    [
        Output("functional-area", "value"),
        Output("functional-area-two", "value"),
        Output("functional-area-three", "value"),
    ],
    [Input("specific-work-attribute-categories", "value")],
)
def set_default_functional_areas(selected_attributes):
    if not selected_attributes or len(selected_attributes) < 3:
        return no_update, no_update, no_update

    if not isinstance(selected_attributes, list):
        selected_attributes = [selected_attributes]

    top_3_areas = update_dataframe_with_ratings(selected_attributes)
    print(top_3_areas)
    return (
        top_3_areas[0] if top_3_areas else None,
        top_3_areas[1] if len(top_3_areas) > 1 else None,
        top_3_areas[2] if len(top_3_areas) > 2 else None,
    )


@callback(
    Output("scrollable-table-container", "children"),
    [
        Input("functional-area", "value"),
        Input("functional-area-two", "value"),
        Input("functional-area-three", "value"),
        Input("tier-two", "value"),
        Input("tier-three", "value"),
        Input("tier-four", "value"),
    ],
)
def update_table(fa1, fa2, fa3, t1, t2, t3):
    df_updated = functions.get_data_for_job_description_table()
    print(f"Received dropdown values: {fa1}, {fa2}, {fa3}")
    print(f"Received tier values: {t1}, {t2}, {t3}")

    conditions = []
    if fa1 and t1:
        conditions.append((df_updated["Career Area"].str.lower() == fa1.lower()) & (df_updated["Position Level"] == t1))
    if fa2 and t2:
        conditions.append((df_updated["Career Area"].str.lower() == fa2.lower()) & (df_updated["Position Level"] == t2))
    if fa3 and t3:
        conditions.append((df_updated["Career Area"].str.lower() == fa3.lower()) & (df_updated["Position Level"] == t3))

    if conditions:
        combined_conditions = conditions[0]
        for cond in conditions[1:]:
            combined_conditions |= cond
        filtered_df = df_updated[combined_conditions]
    else:
        filtered_df = df_updated

    print(f"Filtered DataFrame: {filtered_df['Career Area'].unique()}")
    return generate_table(filtered_df)
