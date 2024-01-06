import pandas as pd

def merge_building_data(df_building, df_coordinates):
    df = pd.merge(df_building, df_coordinates, on="city", how="inner", validate="many_to_many")
    return df