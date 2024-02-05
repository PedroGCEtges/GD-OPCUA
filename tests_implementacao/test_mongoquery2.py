from datetime import datetime, timedelta
from tags import Sorting

from utils.db_utils import mongo_client

mongo_db = mongo_client()["Teste"]
mongo_col = mongo_db["teste"] 

inicio = datetime(2023, 12, 1, 0, 0, 0)
fim = datetime(2023, 12, 13, 0, 0, 0)

query = {"timestamp": {"$gte": inicio, "$lt": fim}}
resultados = mongo_col.find(query).sort("timestamp")
   
tempo_total = timedelta()
valor_anterior = None
tempo_anterior = None

tags_and_times ={}

for doc in resultados:
    # tempo = doc["timestamp"]
    tags = doc["tags"]
    for tag in tags:
        if tag["name"] in Sorting:
            print(tag)
    # for tag in tags:
    #     tags_and_times[tag["name"]] = tag["value"]
    #     value = tag["value"]
    # if valor_anterior == 0 and value == 1:
    #     diferenca = tempo - tempo_anterior
    #     tempo_total += diferenca
    # valor_anterior = value
    # tempo_anterior = tempo
# print(tags_and_times)
