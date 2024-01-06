from datetime import datetime, timedelta
import pandas as pd

import requests


def get_earthquake(last_day):
    url = "https://deprem.afad.gov.tr/EventData/GetEventsByFilter"
    last = datetime.now() - timedelta(hours=24 * last_day)
    now = datetime.now()

    request_payload = {
        "EventSearchFilterList": [
            {
                "FilterType": 1,
                "Value": "22.4502"
            },
            {
                "FilterType": 2,
                "Value": "52.7088"
            },
            {
                "FilterType": 3,
                "Value": "24.7742"
            },
            {
                "FilterType": 4,
                "Value": "47.6258"
            },
            {
                "FilterType": 8,
                "Value": last.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
            {
                "FilterType": 9,
                "Value": now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
        ],
        "Skip": 0,
        "Take": 100000,
        "SortDescriptor": {
            "field": "eventDate",
            "dir": "desc"
        }
    }
    response = requests.post(url, json=request_payload)
    response_data = response.json()["eventList"]

    data = []

    for earthquake in response_data:
        date = earthquake["eventDate"]
        address = earthquake["location"]
        magnitude = float(earthquake["magnitude"])
        latitude = float(earthquake["latitude"])
        longitude = float(earthquake["longitude"])
        dept = -float(earthquake["depth"])
        data.append([magnitude, latitude, longitude, date, address, dept])

    df = pd.DataFrame(
        data, columns=['magnitude', 'latitude', 'longitude', 'date', 'address', 'dept'])

    return df