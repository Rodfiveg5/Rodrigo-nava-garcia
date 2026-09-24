import pymongo
import random
import os 
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import quote_plus

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

user = os.getenv("Mongo_User")
password = quote_plus(os.getenv("Mongo_password"))
cluster = os.getenv("Mongo_cluster")
database = os.getenv("Mongo_db")
colleccion_name = os.getenv("Mongo_colleccion")

mongo_uri = f"mongodb+srv://{user}:{password}@{cluster}"


producto = ["laptop", "telefono"]

for _ in range (10):
    producto_random = random.choice(producto)
    cantidad_random = random.randint(1, 10)

    data = {
        "producto": producto_random,
        "cantidad": cantidad_random
    }

    client = pymongo.MongoClient(mongo_uri)
    db = client[database]
    collection = db[colleccion_name]
    collection.insert_one(data)
    
print("Datos Guardados")
