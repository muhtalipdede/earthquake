from flask import render_template
from app.api.get_total_building_map import get_total_building_map
from app.api.load_building_data import load_building_data
from app.api.load_coordinates import load_coordinates
from app.api.merge_building_data import merge_building_data

def building_page():
    df_building = load_building_data()
    df_coordinates = load_coordinates()
    df = merge_building_data(df_building=df_building, df_coordinates=df_coordinates)
    _total_building_map = get_total_building_map(df=df, row_name="total_building")
    _before_1980_map = get_total_building_map(df=df, row_name="before_1980")
    _between_1980_2000_map = get_total_building_map(df=df, row_name="between_1980_2000")
    _after_2000_map = get_total_building_map(df=df, row_name="after_2000")
    _unknown_map = get_total_building_map(df=df, row_name="unknown")
    return render_template("building.html", total_building_map=_total_building_map, before_1980_map=_before_1980_map, between_1980_2000_map=_between_1980_2000_map, after_2000_map=_after_2000_map, unknown_map=_unknown_map)
