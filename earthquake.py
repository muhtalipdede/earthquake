from flask import Flask, render_template, request
import folium
import folium.plugins as plugins
import pandas as pd
import xml.etree.ElementTree as ET
import requests
import plotly.express as px
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='template', static_folder='static')

def fetch_afad_data():
    url = "https://deprem.afad.gov.tr/EventData/GetEventsByFilter"

    last = datetime.now() - timedelta(hours=240)
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
        "Take": 1000,
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

    return df, data


def get_magnitude_map(df):

    magnitude_map = folium.Map(
        location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=5)
    magnitude_map_data = zip(df['latitude'], df['longitude'], df['magnitude'])
    plugins.HeatMap(data=magnitude_map_data, min_zoom=7,
                    max_zoom=7).add_to(magnitude_map)

    return magnitude_map._repr_html_()


def get_threed_map(df):
    fig = px.scatter_3d(df, x='longitude', y='latitude',
                        z='dept', color='magnitude', size='magnitude')

    fig.update_layout(scene=dict(xaxis=dict(
        range=[26, 45]), yaxis=dict(range=[36, 42])))

    return fig.to_html(full_html=False)


def get_earthquake(data):
    return data


@app.route("/")
def index():
    df, data = fetch_afad_data()
    _magnitude_map = get_magnitude_map(df=df)
    _threed_map = get_threed_map(df=df)
    _earthquakes = get_earthquake(data=data)
    return render_template("index.html", magnitude_map=_magnitude_map, threed_map=_threed_map, earthquakes=_earthquakes)


if __name__ == "__main__":
    app.run()
