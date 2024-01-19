from app.models.city import city
from app.repository.database import get_city_collection

def get_city(id: city):
    city = get_city_collection().find_one({"_id": id})
    return city

def add_city(city: city):
    get_city_collection().insert_one(city)

def update_city(city: city):
    get_city_collection().update_one({"_id": city.id}, {"$set": city.to_json()})

def delete_city(id: city):
    get_city_collection().delete_one({"_id": id})

def get_all_cities():
    cities = get_city_collection().find()
    return cities

def get_cities_by_country(country: str):
    cities = get_city_collection().find({"country": country})
    return cities
