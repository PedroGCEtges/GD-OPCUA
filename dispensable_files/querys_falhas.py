result = db.collection.aggregate([
    {"$match": {"tags": {"$elemMatch": {"name": "M_STATUS", "value": 1}}}}, # Filtra os documentos que têm pelo menos um dicionário com name = "M_STATUS" e value = 1 na lista tags
    {"$unwind": "$tags"}, # Separa cada dicionário da lista tags em um documento separado
    {"$match": {"tags.name": "M_STATUS", "tags.value": 1}}, # Filtra os documentos que têm name = "M_STATUS" e value = 1 no dicionário tags
    {"$sort": {"tags.timestamp": 1}}, # Ordena os documentos por ordem crescente de timestamp
    {"$group": {"_id": "$_id", "timestamps": {"$push": "$tags.timestamp"}}}, # Agrupa os documentos por _id e cria uma lista com os timestamps
    {"$project": {"_id": 1, "time": {"$reduce": { # Projeta os documentos com _id e time
        "input": {"$range": [0, {"$subtract": [{"$size": "$timestamps"}, 1]}]}, # Cria uma lista de índices de 0 até o tamanho da lista de timestamps menos 1
        "initialValue": 0, # Define o valor inicial da soma como 0
        "in": {"$add": ["$$value", {"$divide": [{"$subtract": [{"$arrayElemAt": ["$timestamps", {"$add": ["$$this", 1]}]}, {"$arrayElemAt": ["$timestamps", "$$this"]}]}, 1000]}]} # Soma o valor atual com a diferença entre dois timestamps consecutivos dividida por 1000 (para converter de milissegundos para segundos)
    }}}}
])

print(result.next())



# # Suponha que você queira o tempo total em segundos
# result = db.collection.aggregate( [
#   # Filtra os documentos pelo intervalo de datas
#   { "$match": {
#     "timestamp": {
#       "$gte": datetime.datetime.now() - datetime.timedelta(days=1),# ("2023-01-01T00:00:00Z"),
#       "$lt": datetime.datetime.now()# ("2024-01-01T00:00:00Z")
#     }
#   }},
  # Separa os documentos em subdocumentos, um para cada elemento da lista tags
#   { "$unwind": "$tags" },
  # Filtra os subdocumentos pela condição name = M_STATUS e value = 1
#   { "$match": {
#     "tags.name": "M_STATUS",
#     "tags.value": 1
#   }},
#   # Agrupa os subdocumentos por _id e soma os valores da chave timestamp
#   { "$group": {
#     "_id": "$_id",
#     "total_time": { "$sum": "$timestamp" }
#   }}
# ])

# print(result.next())
# # Definir o intervalo de datas
# start_date = "2023-12-04"
# end_date = "2023-12-05"

# # Construir a agregação
# pipeline = [
#     # Filtrar os documentos pelo intervalo de datas
#     {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
#     # Projetar um novo campo chamado "total_duration" que calcula o tempo total que a tag M_STATUS teve o valor 1
#     {"$project": {
#         "total_duration": {
#             # Usar o operador $reduce para iterar sobre o array "tags" e acumular o resultado em uma variável chamada "sum"
#             "$reduce": {
#                 "input": "$tags",
#                 "initialValue": 0,
#                 "in": {
#                     # Usar o operador $cond para verificar se o nome e o valor da tag são M_STATUS e 1, respectivamente
#                     "$cond": [
#                         {"$and": [
#                             {"$eq": ["$$this.name", "M_STATUS"]},
#                             {"$eq": ["$$this.value", 1]}
#                         ]},
#                         # Se for verdadeiro, usar o operador $dateDiff para calcular a diferença entre o timestamp atual e o próximo, em horas, e somar com o valor acumulado
#                         {"$add": [
#                             "$$value",
#                             {"$dateDiff": {
#                                 "startDate": "$$this.timestamp",
#                                 "endDate": {"$arrayElemAt": ["$tags.timestamp", {"$add": [{"$indexOfArray": ["$tags", "$$this"]}, 1]}]},
#                                 "unit": "hour"
#                             }}
#                         ]},
#                         # Se for falso, retornar o valor acumulado sem alteração
#                         "$$value"
#                     ]
#                 }
#             }
#         }
#     }}
# ]

# # Executar a agregação e imprimir o resultado
# result = collection.aggregate(pipeline)
# print(result.next())
# for doc in result:
#     print("ols")
