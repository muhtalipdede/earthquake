import pandas as pd

def load_building_data():
    csv_data = pd.read_csv("datas/buildings.csv")
    csv_data = csv_data.dropna()
    return csv_data