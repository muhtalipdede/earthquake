from flask import render_template
from app.api.get_population_map import get_population_map
from app.api.load_coordinates import load_coordinates
from app.api.load_population_data import load_population_data
from app.api.merge_data import merge_data

def population_page():
    df_population = load_population_data()
    df_coordinates = load_coordinates()
    df = merge_data(df_population=df_population, df_coordinates=df_coordinates)    
    _population_map = get_population_map(df=df)
    return render_template("population.html", population_map=_population_map)