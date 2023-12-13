import sqlite3
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

def create_sqlite():
    # criar uma conexão SQLite e se conectar ao banco de dados SQLite
    sqlite_conn = sqlite3.connect("opcua.db")
    sqlite_cur = sqlite_conn.cursor()

    # criar uma tabela SQLite se não existir
    sqlite_cur.execute("CREATE TABLE IF NOT EXISTS opcua_data (tag TEXT, value TEXT, timestamp TEXT)")
    return sqlite_cur, sqlite_conn

def add_tags_to_sqlite(tags, sqlite = create_sqlite()):
    sqlite_cur, sqlite_conn = sqlite
    
    for tag in tags:
        # obter o nome, o valor e o carimbo de data/hora da tag
        timestamp = tag[0]
        name = tag[1]
        value = tag[2]
    

        # criar uma tupla SQLite com os dados da tag
        sqlite_row = (name, value, timestamp)

        # inserir a tupla SQLite na tabela SQLite
        sqlite_cur.execute("INSERT INTO opcua_data VALUES (?,?,?)", sqlite_row)

        # confirmar as alterações na tabela SQLite
        sqlite_conn.commit()