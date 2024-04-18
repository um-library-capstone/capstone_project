import pandas as pd

# Read the data
def read_data():
    df = pd.read_csv("./data/PJDD_CodingData_Clean_Anon_Long_CatNum.csv")

    tier_map = {
    'Tier 5': 'Entry Level',
    'Tier 4': 'Associate',
    'Tier 3': 'Mid-Senior',
    'Tier 2': 'Manager',
    'Tier 1': 'Department Head',
    'Tier 0': 'Senior Executive'
    }

    df['Decision-Making Authority'] = df['Decision-Making Authority'].map(tier_map)

    return df

# Get the data
def get_data():

    df = read_data()

    df = df[
        [
            "Functional Area",
            "Position Title",
            "Product Area",
            "Decision-Making Authority",
            "Work Attribute Category",
            "General Work Attribute",
            "Specific Work Attribute",
            "Rating Value",
        ]
    ]

    df[
        [
            "Functional Area",
            "Position Title",
            "Product Area",
            "Decision-Making Authority",
            "Work Attribute Category",
            "General Work Attribute",
            "Specific Work Attribute",
        ]
    ] = df[
        [
            "Functional Area",
            "Position Title",
            "Product Area",
            "Decision-Making Authority",
            "Work Attribute Category",
            "General Work Attribute",
            "Specific Work Attribute",
        ]
    ].apply(
        lambda x: x.str.title()
    )

    df = df.loc[df["Functional Area"] != "Other"]
    df['Functional Area'] = df['Functional Area'].str.replace('It', 'IT')
    df['Product Area'] = df['Product Area'].str.replace('It', 'IT')


    return df

# Rename columns
def rename_columns():
    df = get_data()
    df = df.rename(columns={"Functional Area": "Career Area", 
                       "Decision-Making Authority": "Position Level", 
                       "Work Attribute Category": "Skill Category", 
                       "Specific Work Attribute": "Specific Skill",
                       "General Work Attribute": "General Skill"})
    return df

# Get data for the table
def get_data_for_job_description_table():
    df = read_data()
    df = df.rename(columns={"Functional Area": "Career Area", 
                       "Decision-Making Authority": "Position Level", 
                       "Work Attribute Category": "Skill Category", 
                       "Specific Work Attribute": "Specific Skill",
                       "General Work Attribute": "General Skill"})
    return df

# Get unique skill category
def get_unique_work_attribute_categories():
    df = get_data()
    return df["Work Attribute Category"].drop_duplicates().sort_values(ascending=False).tolist()

# Get unique position level
def get_unique_decision_making_authorities():
    df = get_data()
    return df["Decision-Making Authority"].drop_duplicates().sort_values(ascending=False).tolist()

# Get unique career area
def get_unique_functional_areas():
    df = get_data()
    return df["Functional Area"].drop_duplicates().sort_values(ascending=False).tolist()

# Get unique special skill
def get_unique_special_work_attributes(): 
    df = get_data()
    return df["Specific Work Attribute"].drop_duplicates().sort_values(ascending = True)

# Get unique postiton title
def get_unique_position_titles():
    df = get_data()
    return df['Position Title'].drop_duplicates().sort_values(ascending = True)

# Get data to create tree diagram
def get_network_data(functional_area, decision_making_authority, work_attribute_category):
    df = get_data()

    df = df.loc[
        (df["Functional Area"] == functional_area)
        & (df["Decision-Making Authority"] == decision_making_authority)
        & (df["Work Attribute Category"] == work_attribute_category)
    ]

    df = df.loc[df["Rating Value"].notna()]

    df["Rating Value"] = df["Rating Value"] + 1

    df = df.groupby(
        [
            "Functional Area",
            "Decision-Making Authority",
            "Work Attribute Category",
            "General Work Attribute",
            "Specific Work Attribute",
        ]
    )["Rating Value"].agg(["mean"])

    df = df.reset_index()

    df = df.sort_values(df.columns.tolist())

    df["Specific Work Attribute"] = "➤ " + df["Specific Work Attribute"]

    df_data = df.copy()
    df = df_data.copy()

    # summing up the mean values for each General Work Attribute
    df = df.groupby(["Work Attribute Category", "General Work Attribute"])["mean"].agg(["sum"]).reset_index()
    df.columns = ["source", "target", "weight"]

    df_level_1 = df.copy()
    df = df_data.copy()
    # summing up the mean values for each Specific Work Attribute
    df = df.groupby(["General Work Attribute", "Specific Work Attribute"])["mean"].agg(["sum"]).reset_index()
    df.columns = ["source", "target", "weight"]

    # concatenating the two dataframes
    df_level_2 = df.copy()
    df = pd.concat([df_level_1, df_level_2])

    # removing rows with weight = 0
    df = df.loc[df["weight"] != 0]

    # scaling the weight values
    df["weight"] = (df["weight"] + .5) * 5

    df = df.reset_index(drop=True)

    df = df.groupby(['source'], sort=False).apply(lambda x: x.sort_values(['weight'], ascending=False))

    df = df.reset_index(drop=True)
    
    return df

# Get data to create bubble chart diagram
def circle_packing_data(selected_skills):

    print("Selected Skills:", selected_skills)

    df = get_data()
    # Filtering the data based on the selected skills
    df = df[(df["Specific Work Attribute"].isin(selected_skills)) & (df["Rating Value"] == 1)]
    # checking for nans
    df = df.loc[df["Rating Value"].notna()]
    # Adding 1 to the Rating Value to scale
    df["Rating Value"] = df["Rating Value"] + 1

    # Grouping by Functional Area, Position Title, Product Area, and Specific Work Attribute
    df = df.groupby(["Functional Area", "Position Title", "Product Area", "Specific Work Attribute"])["Rating Value"].agg(["mean"]).reset_index()
    df = df.sort_values(df.columns.tolist())

    # Adding some characters to the columns for formatting
    df["Position Title"] = df["Position Title"] + "."
    df["Product Area"] = df["Product Area"] + "."
    df["Specific Work Attribute"] = df["Specific Work Attribute"] + "-"

    df_data = df.copy()
    df = df_data.copy()
    df = df.groupby(["Specific Work Attribute", "Functional Area"])["mean"].agg(["sum"]).reset_index()
    df.columns = ["source", "target", "weight"]

    df_level_1 = df.copy()
    df = df_data.copy()
    df = df.groupby(["Functional Area", "Position Title"])["mean"].agg(["sum"]).reset_index()
    df.columns = ["source", "target", "weight"]

    df_level_2 = df.copy()
    df = pd.concat([df_level_1, df_level_2])

    df = df.loc[df["weight"] != 0]
    df["weight"] = (df["weight"] + .5) * 5

    # group by source and sort by weight
    df = df.reset_index(drop=True)
    df = df.groupby(['source'], sort=False).apply(lambda x: x.sort_values(['weight'], ascending=False))
    df = df.reset_index(drop=True)

    return df