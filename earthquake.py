from flask import Flask, render_template
import folium
import pandas as pd
import xml.etree.ElementTree as ET
import requests

app = Flask(__name__, template_folder='template')

def get_color(magnitude):
    if magnitude > 5:
        return 'red'
    elif magnitude > 4:
        return 'orange'
    elif magnitude > 3:
        return 'yellow'
    elif magnitude > 2:
        return 'green'
    else:
        return 'blue'

def get_map():
    r = requests.get('http://udim.koeri.boun.edu.tr/zeqmap/xmlt/son24saat.xml')
    root = ET.fromstring(r.content)
    data = []
    
    for child in root.iter('*'):
        if (child.tag == "earhquake"):
            magnitude = float(child.items()[4][1])
            latitude = float(child.items()[2][1])
            longitude = float(child.items()[3][1])
            data.append([magnitude, latitude, longitude])
    
    df = pd.DataFrame(data, columns=['mag', 'lat', 'lng'])
    df = df.sort_values('mag', ascending=False)

    m = folium.Map(location=[df['lat'].mean(), df['lng'].mean()], zoom_start=2)

    for i, row in df.iterrows():
        color = get_color(row['mag'])
        folium.CircleMarker(location=[row['lat'], row['lng']], radius=row['mag']*3, color=color, fill=True).add_to(m)

    return m._repr_html_()

@app.route("/")
def index():
    _map = get_map()
    return render_template("index.html", map=_map)

if __name__ == "__main__":
    app.run()
