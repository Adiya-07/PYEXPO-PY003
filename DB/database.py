from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["astroguy"]
horoscope_predictions = db["horoscope_predictions"]
print("Database connection successful!")