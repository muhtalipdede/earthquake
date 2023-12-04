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

    last = datetime.now() - timedelta(hours=24 * 365)
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
        if float(earthquake["magnitude"]) < 2.0:
            continue;
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
        location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=7)

    plugins.Fullscreen(
        position='topright',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True
    ).add_to(magnitude_map)

    folium.plugins.TimestampedGeoJson({
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [row['longitude'], row['latitude']],
            },
            'properties': {
                'time': row['date'].replace('T', ' ').replace('Z', ''),
                'icon': 'circle',

                'iconstyle': {
                    'fillColor': 'red',
                    'fillOpacity': 1,
                    'stroke': 'true',
                    'radius': row['magnitude'] * 0.8,
                }
            }
        } for _, row in df.iterrows()]
    }, 
    period='PT24H', 
    add_last_point=True).add_to(magnitude_map)

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=True,
        control=True,
        show=False
    ).add_to(magnitude_map)

    folium.plugins.LocateControl(
        drawCircle=False,
        showPopup=False,
        locateOptions={'maxZoom': 10}
    ).add_to(magnitude_map)

    folium.LayerControl().add_to(magnitude_map)

    return magnitude_map._repr_html_()

def get_earthquake(data):
    return data

@app.route("/")
def index():
    df, data = fetch_afad_data()
    _magnitude_map = get_magnitude_map(df=df)
    return render_template("index.html", magnitude_map=_magnitude_map)


if __name__ == "__main__":
    app.run()
