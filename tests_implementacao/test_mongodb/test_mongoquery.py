from pymongo import MongoClient
from datetime import datetime

from utils.db_utils import mongo_client

# Conectando ao banco de dados
mongo_db = mongo_client()["Teste"]
mongo_col = mongo_db["teste"] 


# Definindo o intervalo de tempo
inicio = datetime(2023, 12, 5, 0, 0, 0)
fim = datetime(2023, 12, 6, 0, 0, 0)

# Construindo a consulta de agregação
pipeline = [
    # Filtrando os documentos pelo intervalo de tempo
    {'$match': {'timestamp': {'$gte': inicio, '$lte': fim}}},
    # Separando os elementos do array tags em documentos individuais
    {'$unwind': '$tags'},
    # Agrupando os documentos por tag e calculando a soma do tempo que cada tag teve o valor 1 ou 0
    {'$group': {
        '_id': '$tags.name', # O campo pelo qual vamos agrupar
        'tempo_1': {'$sum': {'$cond': [{'$eq': ['$tags.value', 1]}, '$tags.timestamp', 0]}}, # A soma do tempo que a tag teve o valor 1
        'tempo_0': {'$sum': {'$cond': [{'$eq': ['$tags.value', 0]}, '$tags.timestamp', 0]}}, # A soma do tempo que a tag teve o valor 0
    }},
    # Formatando o resultado
    {'$project': {
        '_id': 0, # Não queremos mostrar o campo _id
        'tag': '$_id', # O nome da tag
        'tempo_1': 1, # O tempo que a tag teve o valor 1
        'tempo_0': 1, # O tempo que a tag teve o valor 0
    }}
]

# Executando a consulta e obtendo o resultado
resultado = mongo_col.aggregate(pipeline)

# Imprimindo o resultado
for doc in resultado:
    print(doc)
