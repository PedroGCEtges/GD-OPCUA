from pymongo import MongoClient
from datetime import datetime

from utils.db_utils import mongo_client
import matplotlib.pyplot as plt

# Conectando ao banco de dados
mongo_db = mongo_client()["Teste"]
mongo_col = mongo_db["teste"] 


# Definindo o intervalo de tempo
inicio = datetime(2023, 12, 1, 0, 0, 0)
fim = datetime(2023, 12, 13, 0, 0, 0)

# Construindo a consulta de agregação
pipeline = [
    # Filtrando os documentos pelo intervalo de tempo
    {'$match': {'timestamp': {'$gte': inicio, '$lte': fim}}},
    # Separando os elementos do array tags em documentos individuais
    {'$unwind': '$tags'},
    # Convertendo o campo timestamp de string para data
    {'$addFields': {
        'tags.timestamp': {
            '$dateFromString': {
                'dateString': {'$substr':["$tags.timestamp", 0, 23]},
                'format': '%Y-%m-%dT%H:%M:%S.%L' # O formato da string da data
        }
    }}},
    # Agrupando os documentos por tag e calculando a soma do tempo que cada tag teve o valor 1 ou 0
    {'$group': {
        '_id': '$tags.name', # O campo pelo qual vamos agrupar
        'WorkingTime': {'$sum': {'$cond': [{'$eq': ['$tags.value', 1]}, '$tags.value', 0]}},

        'TotalOperation': { '$sum': 1 },}},
        # 'tempo_1': {'$sum': {'$cond': [{'$eq': ['$tags.value', 1]}, '$tags.timestamp', 0]}}
         # A soma do tempo que a tag teve o valor 1
    #     'tempo_0': {'$sum': {'$cond': [{'$eq': ['$tags.value', 0]}, '$tags.timestamp', 0]}}, # A soma do tempo que a tag teve o valor 0
    # }},
    # Formatando o resultado
    # {'$project': {
    #     '_id': 0, # Não queremos mostrar o campo _id
    #     'tag': '$_id', # O nome da tag
    #     'tempo_1': .00001, # O tempo que a tag teve o valor 1
    #     'tempo_0': 1, # O tempo que a tag teve o valor 0
    # }}
]

# Executando a consulta e obtendo o resultado
resultado = mongo_col.aggregate(pipeline)

final_dict = {}
# Imprimindo o resultado
for doc in resultado:
    final_dict[doc["_id"]] = {
        "Working": doc['WorkingTime'] / doc['TotalOperation'],
        "Iddle": abs(doc['WorkingTime'] - doc['TotalOperation']) / doc['TotalOperation'],
    }

print(final_dict)

tempo_1 = 123456 # Em segundos
tempo_0 = 987654 # Em segundos

# Criando uma lista com os valores
valores = [tempo_1, tempo_0]

# Criando uma lista com os rótulos
rotulos = ['Valor 1', 'Valor 0']

# Criando o gráfico de pizza
plt.pie(valores, labels=rotulos, autopct='%1.1f%%')

# Adicionando um título
plt.title('Tempo que a tag G1BG1 teve o valor 1 ou 0')

# Mostrando o gráfico
plt.show()