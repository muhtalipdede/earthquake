from flask import Blueprint, request
from app.hooks.is_mobile import is_mobile
from app.pages.about import about_page
from app.pages.building import building_page
from app.pages.earthquake import earthquake_page
from app.pages.grater_than_5 import grater_than_5_page
from app.pages.grater_than_6 import grater_than_6_page
from app.pages.grater_than_7 import grater_than_7_page
from app.pages.index import index_page
from app.pages.mobile.earthquake import earthquake_mobile_page
from app.pages.mobile.index import index_mobile_page
from app.pages.mobile.three_d import three_d_mobile_page
from app.pages.not_found import not_found_page
from app.pages.population import population_page
from app.pages.three_d import three_d_page

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    if is_mobile(request):
        return index_mobile_page()
    else:
        return index_page()

@main_blueprint.route('/earthquake')
def earthquake():
    last_day = request.args.get("last_day", 1, type=int)
    if last_day > 360:
        last_day = 360
    if is_mobile(request):
        return earthquake_mobile_page(last_day)
    else:
        return earthquake_page(last_day)

@main_blueprint.route('/population')
def population():
    return population_page()

@main_blueprint.route('/building')
def building():
    return building_page()

@main_blueprint.route('/about')
def about():
    return about_page()

@main_blueprint.route('/grater_than_5')
def grater_than_5():
    return grater_than_5_page()

@main_blueprint.route('/grater_than_6')
def grater_than_6():
    return grater_than_6_page()

@main_blueprint.route('/grater_than_7')
def grater_than_7():
    return grater_than_7_page()

@main_blueprint.route('/3d_earthquake')
def three_d():
    if is_mobile(request):
        return three_d_mobile_page()
    else:
        return three_d_page()
    
@main_blueprint.route('/3d_population')
def three_d_population():
    if is_mobile(request):
        return three_d_population_mobile_page()
    else:
        return three_d_population_page()


@main_blueprint.errorhandler(404)
def not_found(e):
    return not_found_page(e)