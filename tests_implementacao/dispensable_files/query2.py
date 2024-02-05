from datetime import datetime, timedelta

from utils.db_utils import mongo_client
# definindo o nome da coleção
client = mongo_client()
db = client["Teste"]
colecao = db["teste"]

# definindo o formato do timestamp
formato = "%Y-%m-%dT%H:%M:%S.%fZ"
# definindo o intervalo de datas
inicio = datetime.now() - timedelta(days=1) # ano, mês, dia
fim = datetime.now() # ano, mês, dia
# construindo a consulta para filtrar os documentos por timestamp e ordená-los
query = {"timestamp": {"$gte": inicio, "$lt": fim}}
resultados = colecao.find(query).sort("timestamp")
# inicializando a variável para armazenar o tempo total
tempo_total = timedelta()
# inicializando a variável para armazenar o valor anterior da tag M_STATUS
valor_anterior = None
# inicializando a variável para armazenar o timestamp anterior da tag M_STATUS
tempo_anterior = None
# percorrendo os documentos resultantes da consulta
for doc in resultados:
    # obtendo o timestamp do documento
    tempo = doc["timestamp"]
    # obtendo o valor da tag M_STATUS
    valor = doc["tags"]
    for tag in valor:
        if tag["name"] == "M_STATUS":
            value = tag["value"]
    # verificando se o valor mudou de 0 para 1
    if valor_anterior == 0 and value == 1:
        # calculando a diferença entre o timestamp atual e o anterior
        diferenca = tempo - tempo_anterior
        # adicionando a diferença ao tempo total
        tempo_total += diferenca
    # atualizando o valor anterior e o tempo anterior
    valor_anterior = value
    tempo_anterior = tempo
# imprimindo o tempo total
print(f"O tempo total que a tag M_STATUS teve o valor 1 foi de {tempo_total}")