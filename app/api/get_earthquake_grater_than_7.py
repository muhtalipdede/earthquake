import csv
import pandas as pd

def get_earthquake_grater_than_7():
    with open('datas/greater_than_7.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = []
        for line in csv_reader:
            data.append(line)
        df = pd.DataFrame(data, columns=["magnitude", "latitude", "longitude", "date", "address", "dept"])
        df = df.astype({"magnitude": float, "latitude": float, "longitude": float, "date": str, "address": str, "dept": float})

    return df