from flask import Flask, render_template
import folium
import folium.plugins as plugins
import pandas as pd
import xml.etree.ElementTree as ET
import requests
import plotly.express as px

app = Flask(__name__, template_folder='template')

def get_maps():
    r = requests.get('http://udim.koeri.boun.edu.tr/zeqmap/xmlt/son24saat.xml')
    root = ET.fromstring(r.content)
    data = []
    
    for child in root.iter('*'):
        if (child.tag == "earhquake"):
            date = child.items()[0][1]
            address = child.items()[1][1]
            magnitude = float(child.items()[4][1])
            latitude = float(child.items()[2][1])
            longitude = float(child.items()[3][1])
            dept = -float(child.items()[5][1])
            data.append([magnitude, latitude, longitude, date, address, dept])
    
    df = pd.DataFrame(data, columns=['magnitude', 'latitude', 'longitude', 'date', 'address', 'dept'])
    df = df.sort_values('date', ascending=False)

    magnitude_map = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=7)
    magnitude_map_data = zip(df['latitude'], df['longitude'], df['magnitude'])
    plugins.HeatMap(data=magnitude_map_data, min_zoom=7, max_zoom=7).add_to(magnitude_map)

    ## last 10 earthquake
    for i in range(0, 10):
        folium.Marker([df.iloc[i]['latitude'], df.iloc[i]['longitude']], popup=df.iloc[i]['address'] + " " + df.iloc[i]['date']).add_to(magnitude_map)

    fig = px.scatter_3d(df, x='longitude', y='latitude', z='dept', color='magnitude', size='magnitude', size_max=18, opacity=0.7)

    fig.update_layout(xaxis=dict(range=[26, 45]), yaxis=dict(range=[36, 42]))

    return magnitude_map._repr_html_(), fig.to_html(full_html=False)

@app.route("/")
def index():
    _magnitude_map, _threed_map = get_maps()
    return render_template("index.html", magnitude_map=_magnitude_map, threed_map=_threed_map)

if __name__ == "__main__":
    app.run()
