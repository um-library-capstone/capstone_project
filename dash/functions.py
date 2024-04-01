import pandas as pd

def read_data():
    df = pd.read_csv("./data/PJDD_CodingData_Clean_Anon_Long_CatNum.csv")

    return df

def get_data():

    df = pd.read_csv("./data/PJDD_CodingData_Clean_Anon_Long_CatNum.csv")

    df = df[
        [
            "Functional Area",
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
            "Decision-Making Authority",
            "Work Attribute Category",
            "General Work Attribute",
            "Specific Work Attribute",
        ]
    ] = df[
        [
            "Functional Area",
            "Decision-Making Authority",
            "Work Attribute Category",
            "General Work Attribute",
            "Specific Work Attribute",
        ]
    ].apply(
        lambda x: x.str.title()
    )

    df = df.loc[df["Functional Area"] != "Other"]

    return df


def get_unique_work_attribute_categories():

    df = get_data()

    return df["Work Attribute Category"].drop_duplicates().sort_values(ascending=False).tolist()


def get_unique_decision_making_authorities():

    df = get_data()

    return df["Decision-Making Authority"].drop_duplicates().sort_values(ascending=False).tolist()


def get_unique_functional_areas():

    df = get_data()

    return df["Functional Area"].drop_duplicates().sort_values(ascending=False).tolist()

def get_unique_special_work_attributes(): 

    df = get_data()

    return df["Specific Work Attribute"].drop_duplicates().sort_values(ascending = True)


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

    df = df.groupby(["Work Attribute Category", "General Work Attribute"])["mean"].agg(["sum"]).reset_index()

    df.columns = ["source", "target", "weight"]

    df_level_1 = df.copy()

    df = df_data.copy()

    df = df.groupby(["General Work Attribute", "Specific Work Attribute"])["mean"].agg(["sum"]).reset_index()

    df.columns = ["source", "target", "weight"]

    df_level_2 = df.copy()

    df = pd.concat([df_level_1, df_level_2])

    df = df.loc[df["weight"] != 0]

    df["weight"] = (df["weight"] + .5) * 5

    df = df.reset_index(drop=True)

    df = df.groupby(['source'], sort=False).apply(lambda x: x.sort_values(['weight'], ascending=False))

    df = df.reset_index(drop=True)
    
    return df
