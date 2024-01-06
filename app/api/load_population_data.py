import pandas as pd

def load_population_data():
    csv_data = pd.read_csv("datas/population.csv")
    csv_data = csv_data.dropna()
    return csv_data