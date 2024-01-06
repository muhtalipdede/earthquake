from flask import Blueprint, request
from app.pages.building import building_page
from app.pages.earthquake import earthquake_page
from app.pages.index import index_page
from app.pages.not_found import not_found_page
from app.pages.population import population_page

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return index_page()

@main_blueprint.route('/earthquake')
def earthquake():
    last_day = request.args.get("last_day", 1, type=int)
    if last_day > 360:
        last_day = 360
    return earthquake_page(last_day)

@main_blueprint.route('/population')
def population():
    return population_page()

@main_blueprint.route('/building')
def building():
    return building_page()

@main_blueprint.errorhandler(404)
def not_found(e):
    return not_found_page(e)