import folium
from folium.plugins import HeatMap
def get_total_building_map(df, row_name):
    total_building_map = folium.Map(
        location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=5)

    ## heatmap
    heat_data = [[row['latitude'], row['longitude'], row[row_name]] for _, row in df.iterrows()]
    HeatMap(heat_data, radius=30).add_to(total_building_map)

    return total_building_map._repr_html_()