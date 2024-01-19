from pymongo import MongoClient

def get_database():
    client = MongoClient('localhost', 27017)
    db = client['earthquake']
    return db

def get_city_collection():
    db = get_database()
    return db['city']