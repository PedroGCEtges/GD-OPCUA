import pymongo
import datetime

def create_collection(collection_name):
    client = pymongo.MongoClient("mongodb+srv://pedroetges11:PedroEtges11@pfc.0hhrvpi.mongodb.net/?retryWrites=true&w=majority")
    db = client["GD"]
    collection = db[collection_name]
    return collection

def mongo_client():
    return pymongo.MongoClient("mongodb+srv://pedroetges11:PedroEtges11@pfc.0hhrvpi.mongodb.net/?retryWrites=true&w=majority")

def get_tags_interval_date(start, end, collection):

    filter = {"date": {"$gte": start, "$lte": end}}
    cursor = collection.find(filter)
    documents = []
    
    for document in cursor:
        documents.append(document)
        print(document)