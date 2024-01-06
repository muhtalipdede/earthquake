import folium
from folium.plugins import HeatMap

def get_population_map(df):
    population_map = folium.Map(
        location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=7)

    ## heatmap
    heat_data = [[row['latitude'], row['longitude'], row['population']] for _, row in df.iterrows()]
    HeatMap(heat_data, radius=50
        ).add_to(population_map)

    return population_map._repr_html_()