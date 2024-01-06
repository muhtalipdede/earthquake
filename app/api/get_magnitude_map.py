import folium
import folium.plugins 


def get_magnitude_map(df, fault_line):
    magnitude_map = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=7)
    for index, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['magnitude'] * 2,
            popup=row['address'],
            color='#3186cc',
            fill=True,
            fill_color='#3186cc'
        ).add_to(magnitude_map)

    folium.GeoJson(
        fault_line,
        name='geojson',
        style_function=lambda feature: {
            'fillColor': '#ff0000',
            'color': '#ff0000',
            'weight': 1,
            'dashArray': '5, 5',
        }
    ).add_to(magnitude_map)

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

    folium.plugins.Fullscreen(
        position='topright',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True
    ).add_to(magnitude_map)

#     folium.plugins.TimestampedGeoJson({
#         'type': 'FeatureCollection',
#         'features': [{
#             'type': 'Feature',
#             'geometry': {
#                 'type': 'Point',
#                 'coordinates': [row['longitude'], row['latitude']],
#             },
#             'properties': {
#                 'time': row['date'].replace('T', ' ').replace('Z', ''),
#                 'icon': 'circle',

#                 'iconstyle': {
#                     'fillColor': 'red',
#                     'fillOpacity': 1,
#                     'stroke': 'true',
#                     'radius': row['magnitude'] * 0.8,
#                 }
#             }
#         } for _, row in df.iterrows()]
#     }, 
#     period='PT24H', 
#     add_last_point=True).add_to(magnitude_map)

    return magnitude_map._repr_html_()
