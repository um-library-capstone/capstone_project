from dash import html, dcc, callback, Output, Input, __version__, register_page, no_update, dash_table, Dash, callback_context
from dash.exceptions import PreventUpdate
import functions
import pandas as pd


register_page(__name__)

unique_functional_areas = functions.get_unique_functional_areas()
unique_decision_making_authorities = functions.get_unique_decision_making_authorities()
unique_work_attribute_categories = functions.get_unique_work_attribute_categories()
unique_specific_work_attribute_categories = functions.get_unique_special_work_attributes()

df = functions.read_data()

columns_to_keep = [
        "Description Number",
        "Position Title",
        "Functional Area",
        "Product Area",
        "Decision-Making Authority",
        "Years of Experience",
        "Education Credentials",
    ]

df = df[columns_to_keep].drop_duplicates(keep="last")

def generate_table(dataframe):
    columns_to_keep = [
        "Description Number",
        "Position Title",
        "Functional Area",
        "Product Area",
        "Decision-Making Authority",
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
        df = functions.get_data()

        print(f"DataFrame before filtering: {df.head()}")

        filtered_df = df[(df["Specific Work Attribute"].isin(selected_skills)) & (df["Rating Value"] == 1)]

        if filtered_df.empty:
            print("Filtered DataFrame is empty. Check selected skills and rating values.")
            return []

        top_3 = filtered_df.groupby("Functional Area").size().sort_values(ascending=False).head(3)
        top_3_df = top_3.to_frame()
        top_3_areas = top_3_df.index.tolist()
        print(f"Top 3 functional areas: {top_3_areas}")

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
                                html.Label(["Current Functional Area"]),
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
                                html.Label(["Specific Work Attribute Categories"]),
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
                                html.Label(["Work Attribute Categories"]),
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
                                # html.Label(
                                #     ["Current Functional Area"],
                                #     style={"font-weight": "bold", "display": "block", "margin-bottom": "5px"},
                                # ),
                                html.Div(
                                    id="current-functional-area",
                                    className="drop-down",
                                    children=unique_functional_areas[0],
                                    style={"padding": "10px", "margin-bottom": "20px", "border": "1px solid #ccc", "font-weight": "bold"}, 
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
                                # html.Label(
                                #     ["Functional Area 1"],
                                #     style={"font-weight": "bold", "display": "block", "margin-bottom": "5px"},
                                # ),
                                html.Div(
                                    id="functional-area",
                                    className="info-display",
                                    children=unique_functional_areas[0],
                                    style={"padding": "10px", "margin-bottom": "20px", "border": "1px solid #ccc", "font-weight": "bold",}
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
                                # html.Label(
                                #     ["Functional Area 2"],
                                #     style={"font-weight": "bold", "display": "block", "margin-bottom": "5px"},
                                # ),
                                html.Div(
                                    id="functional-area-two",
                                    className="info-display",
                                    children=unique_functional_areas[0],
                                    style={"padding": "10px", "margin-bottom": "20px", "border": "1px solid #ccc", "font-weight": "bold",}
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
                                # html.Label(
                                #     ["Functional Area 3"],
                                #     style={"font-weight": "bold", "display": "block", "margin-bottom": "5px"},
                                # ),
                                html.Div(
                                    id="functional-area-three",
                                    className="info-display",
                                    children=unique_functional_areas[0],
                                    style={"padding": "10px", "margin-bottom": "20px", "border": "1px solid #ccc", "font-weight": "bold",}
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
                html.H4("Job Descriptions Based on Your Skills and Functional Area"),
                dash_table.DataTable(
                    id='table-sorting-filtering',
                    # columns=[{"name": i, "id": i} for i in columns_to_keep],
                    columns=[{"name": i, "id": i} for i in columns_to_keep],
                    data=df.to_dict('records'),
                    filter_action='custom',
                    filter_query='',
                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[],
                    # style_table={'overflowX': 'scroll', 'maxHeight': '75vh', 'overflowY': 'auto'},
                    style_table={'minWidth': '100%', 'overflowX': 'auto', 'overflowY': 'scroll', 'maxHeight': '500px',},
                    style_cell={
                    'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                    'whiteSpace': 'normal',
                    'fontSize': '12px',
                    'padding': '5px'
                    }, 
                    style_header={  # Styling for the header to match cell styles
                            'fontWeight': 'bold',
                            'padding': '5px'
                        },
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
        Input("current-functional-area", "children"),
        Input("current-tier", "value"),
        Input("work-attribute-categories", "value"),
    ],
)
def update_skills_1(functional_area, tier, work_attribute):
    df = functions.get_data()

    filtered_df = df[
        (df["Functional Area"] == functional_area)
        & (df["Decision-Making Authority"] == tier)
        & (df["Rating Value"] == 1)
        & (df["Work Attribute Category"] == work_attribute)
    ]

    skills = filtered_df["General Work Attribute"].unique().tolist()[:5]

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
    [Input("functional-area", "children"), Input("tier-two", "value"), Input("work-attribute-categories", "value")],
)
def update_skills_2(functional_area, tier, work_attribute):
    df = functions.get_data()

    filtered_df = df[
        (df["Functional Area"] == functional_area)
        & (df["Decision-Making Authority"] == tier)
        & (df["Rating Value"] == 1)
        & (df["Work Attribute Category"] == work_attribute)
    ]

    skills = filtered_df["General Work Attribute"].unique().tolist()[:5]

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
    [Input("functional-area-two", "children"), Input("tier-three", "value"), Input("work-attribute-categories", "value")],
)
def update_skills_3(functional_area, tier, work_attribute):
    df = functions.get_data()
    filtered_df = df[
        (df["Functional Area"] == functional_area)
        & (df["Decision-Making Authority"] == tier)
        & (df["Rating Value"] == 1)
        & (df["Work Attribute Category"] == work_attribute)
    ]

    skills = filtered_df["General Work Attribute"].unique().tolist()[:5]

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
    [Input("functional-area-three", "children"), Input("tier-four", "value"), Input("work-attribute-categories", "value")],
)
def update_skills_4(functional_area, tier, work_attribute):
    df = functions.get_data()
    filtered_df = df[
        (df["Functional Area"] == functional_area)
        & (df["Decision-Making Authority"] == tier)
        & (df["Rating Value"] == 1)
        & (df["Work Attribute Category"] == work_attribute)
    ]

    skills = filtered_df["General Work Attribute"].unique().tolist()[:5]

    skills.extend([""] * (5 - len(skills)))

    return skills


@callback(
    [
        Output("functional-area", "children"),
        Output("functional-area-two", "children"),
        Output("functional-area-three", "children"),
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
    Output('table-sorting-filtering', 'data'),
    [
        Input('current-functional-area', 'children'),
        Input('functional-area', 'children'),
        Input('functional-area-two', 'children'),
        Input('functional-area-three', 'children'),
        Input('current-tier', 'value'),
        Input('tier-two', 'value'),
        Input('tier-three', 'value'),
        Input('tier-four', 'value'),
        Input('table-sorting-filtering', 'sort_by'),
        Input('table-sorting-filtering', 'filter_query')
    ],
)

def update_table_data(fa0, fa1, fa2, fa3, t0, t1, t2, t3, sort_by, filter_query):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    dff = df.copy()
    print(f"Original DataFrame size: {len(dff)}")
    dff = apply_dropdown_filters(fa0,fa1, fa2, fa3, t0, t1, t2, t3, dff)
    print(f"Size after dropdown filtering: {len(dff)}")

    dff = apply_filtering(filter_query, dff)
    dff = apply_sorting(sort_by, dff)

    return dff.to_dict('records')


def apply_dropdown_filters(fa0, fa1, fa2, fa3, t0, t1, t2, t3, df):
    filtered_dfs = [] 

    df_fa0_t0 = df[(df["Functional Area"] == fa0.lower()) & (df["Decision-Making Authority"] == t0)]
    filtered_dfs.append(df_fa0_t0)

    df_fa1_t1 = df[(df["Functional Area"] == fa1.lower()) & (df["Decision-Making Authority"] == t1)]
    filtered_dfs.append(df_fa1_t1)


    df_fa2_t2 = df[(df["Functional Area"] == fa2.lower()) & (df["Decision-Making Authority"] == t2)]
    filtered_dfs.append(df_fa2_t2)


    df_fa3_t3 = df[(df["Functional Area"] == fa3.lower()) & (df["Decision-Making Authority"] == t3)]
    filtered_dfs.append(df_fa3_t3)

    result_df = pd.concat(filtered_dfs).drop_duplicates()

    return result_df

def apply_filtering(filter_query, df):
    filtering_expressions = filter_query.split(' && ')
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator == 'eq':
            df = df[df[col_name] == filter_value]
        elif operator == 'ne':
            df = df[df[col_name] != filter_value]
        elif operator == 'gt':
            df = df[df[col_name] > filter_value]
        elif operator == 'ge':
            df = df[df[col_name] >= filter_value]
        elif operator == 'lt':
            df = df[df[col_name] < filter_value]
        elif operator == 'le':
            df = df[df[col_name] <= filter_value]
        elif operator == 'contains':
            df = df[df[col_name].astype(str).str.contains(filter_value)]
        elif operator == 'datestartswith':
            df = df[df[col_name].astype(str).str.startswith(filter_value)]
    return df

def split_filter_part(filter_part):
    operators = [['ge ', '>='],
                 ['le ', '<='],
                 ['lt ', '<'],
                 ['gt ', '>'],
                 ['ne ', '!='],
                 ['eq ', '='],
                 ['contains '],
                 ['datestartswith ']]
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                value_part = value_part.strip()

                # Removing quotes and handling if it's not a numeric value
                if value_part[0] == value_part[-1] and value_part[0] in ("'", '"', '`'):
                    value = value_part[1:-1]
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part
                
                return name, operator_type[0].strip(), value
    return [None] * 3

def apply_sorting(sort_by, df):
    if sort_by:
        for sort_term in sort_by:
            col_name = sort_term["column_id"]
            direction = sort_term["direction"]
            df = df.sort_values(by=col_name, ascending=(direction == "asc"))
    return df