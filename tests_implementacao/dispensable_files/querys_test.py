import datetime
from  utils.db_utils import mongo_client
import isodate

# Conectar ao banco de dados MongoDB
client = mongo_client()
db = client["Teste"]
collection = db["teste"]

def status_quey():
    # Fazer a consulta usando os passos descritos acima
    resultado = collection.aggregate([
        {"$sort": {"timestamp": -1}}, # Ordenar os documentos pelo timestamp em ordem decrescente
        {"$limit": 1}, # Limitar o número de documentos retornados para apenas um
        {"$project": {"tags": 1}}, # Retornar apenas o campo tags do documento selecionado
        {"$project": {"tags": {"$filter": {"input": "$tags", "as": "tag", "cond": {"$eq": ["$$tag.name", "M_STATUS"]}}}}}, # Filtrar a lista de tags pelo nome da tag desejada
        {"$project": {"value": {"$first": "$tags.value"}}}
        # {"$project": {"value": {"$arrayElemAt": [{"$arrayElemAt": ["$tags.value", 0]}, 0]}}} # Extrair o valor da tag filtrada
    ])

    # Imprimir o valor da tag "M_STATUS" do documento mais recente
    for doc in resultado:
        print(doc["value"])

def interval_tags():
    start = datetime.datetime.now() - datetime.timedelta(days=20)
    end = datetime.datetime.now()
    filter = {"timestamp": {"$gte": start, "$lte": end}}
    cursor = collection.find(filter)
    documents = []
        
    for document in cursor:
        documents.append(document)
    print(documents)    

# result = collection.aggregate([
#     {"$match": {"tags": {"$elemMatch": {"name": "M_STATUS", "value": 1}}}}, # Filtra os documentos que têm pelo menos um dicionário com name = "M_STATUS" e value = 1 na lista tags
#     {"$unwind": "$tags"}, # Separa cada dicionário da lista tags em um documento separado
#     {"$match": {"tags.name": "M_STATUS", "tags.value": 1}}, # Filtra os documentos que têm name = "M_STATUS" e value = 1 no dicionário tags
#     {"$sort": {"tags.timestamp": 1}}, # Ordena os documentos por ordem crescente de timestamp
#     {"$group": {"_id": "$stations", "timestamps": {"$push": "$tags.timestamp"}}}, # Agrupa os documentos por stations e cria uma lista com os timestamps
#     {"$project": {"_id": 1, "time": {"$reduce": { # Projeta os documentos com _id e time
#         "input": {"$range": [0, {"$subtract": [{"$size": "$timestamps"}, 1]}]}, # Cria uma lista de índices de 0 até o tamanho da lista de timestamps menos 1
#         "initialValue": 0, # Define o valor inicial da soma como 0
#         "in": {"$add": ["$$value", 
#                         {"$divide": [
#                             {"$subtract": [
#                                 {"$arrayElemAt": 
#                                     ["$timestamps", {"$add": ["$$this", 1]}]
#                                 },
#                                 {"$arrayElemAt": ["$timestamps", "$$this"]}
#                                 ]
#                             }, 1000]
#                         }
#                     ]
#                 } # Soma o valor atual com a diferença entre dois timestamps consecutivos dividida por 1000 (para converter de milissegundos para segundos)
#             }
#         }
#     }
# }
# ])

# print(result.next())
from datetime import datetime, timedelta
inicio = datetime(2023, 12, 4) # ano, mês, dia
fim = datetime(2023, 12, 6) # ano, mês, dia

query = {"timestamp": {"$gte": inicio, "$lt": fim}}
resultados = list(collection.find(query))
tempo_total = timedelta() # variável para armazenar o tempo total
for i, doc in enumerate(resultados):
    _id = doc["_id"] # identificador do documento
    tags = doc["tags"] # lista de dicionários
    for tag in tags: # loop para cada dicionário na lista
            if tag["name"] == "M_STATUS" and tag["value"] == 1: # condição para filtrar as tags desejadas
                tempo = tag["timestamp"] # timestamp da tag
                # verificando se a tag é a última da lista
                if tags.index(tag) == len(tags) - 1:
                    # tentando obter o documento seguinte na coleção
                    try:
                        proximo_doc = resultados[i + 1]
                        proximo_tempo = proximo_doc["timestamp"] # timestamp do documento seguinte
                    # se não houver documento seguinte, usando o timestamp atual
                    except IndexError:
                        proximo_tempo = datetime.now()
                    except Exception as e:
                        proximo_tempo = datetime.now()
                        print(e)
                        pass
                # se não for a última tag, usando a próxima tag na lista
                else:
                    proxima_tag = tags[tags.index(tag) + 1] # próxima tag na lista
                    proximo_tempo = proxima_tag["timestamp"] # timestamp da próxima tag
                # calculando a diferença entre os timestamps
                diferenca = proximo_tempo -  datetime.strptime(tempo, "%Y-%m-%dT%H:%M:%S.%f")
                # adicionando a diferença ao tempo total
                tempo_total += diferenca
                # imprimindo o tempo parcial para cada documento
                print(f"O tempo que a tag M_STATUS teve o valor 1 no documento {_id} foi de {diferenca}")
    # imprimindo o tempo total

print(f"O tempo total que a tag M_STATUS teve o valor 1 foi de {tempo_total}")
