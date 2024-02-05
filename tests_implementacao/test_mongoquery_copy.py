from datetime import datetime, timedelta

from utils.db_utils import mongo_client
import matplotlib.pyplot as plt

def query_time_and_value_in_mongo(db="Teste", collection="teste",start=datetime(2023, 12, 5, 0, 0, 0), end=datetime(2023, 12, 6, 0, 0, 0) ):
    mongo_db = mongo_client()[db]
    mongo_col = mongo_db[collection] 

    pipeline = [
        {'$match': {'timestamp': {'$gte': start, '$lte': end}}},
        {'$unwind': '$tags'},
        {'$group': {
            '_id': '$tags.name',
            "timestamp": {"$push": "$$ROOT.tags.timestamp"},
            "value":{"$push": "$$ROOT.tags.value"}
        }},
        {'$project': {
            '_id': 0,
            'tag': '$_id',
            "timestamp": 1,
            "value": 1,
        }}
    ]

    resultado = mongo_col.aggregate(pipeline)
    return resultado


def create_dict_with_tupled_values(resultado):
    aux_dict = {}

    for doc in resultado:
        teste = []
        for i in range(len(doc["timestamp"])):
            teste.append((doc["timestamp"][i],doc["value"][i]))
        aux_dict[doc["tag"]] = teste
    return aux_dict


def get_time_diff(aux_dict):
    final_dict = {}
    for key, value in aux_dict.items():
        tempo_total = timedelta()
        valor_anterior = None
        tempo_anterior = None
        for v in range(len(value)):
            intervalo_de_operacao = datetime.strptime(value[-1][0],"%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(value[0][0],"%Y-%m-%dT%H:%M:%S.%f") 

            if valor_anterior == None:
                valor_anterior = value[v][1]
            if tempo_anterior == None:
                tempo_anterior = datetime.strptime(value[v][0],"%Y-%m-%dT%H:%M:%S.%f")

            if value[v][1] != valor_anterior:  
                if value[v][1] == 1:
                    diff = datetime.strptime(value[v][0],"%Y-%m-%dT%H:%M:%S.%f") - tempo_anterior
                    tempo_total += diff

            valor_anterior = value[v][1]
            tempo_anterior = datetime.strptime(value[v][0],"%Y-%m-%dT%H:%M:%S.%f")

        if intervalo_de_operacao.total_seconds() !=0:
            final_dict[key] =  { "Tempos": {
                        "Tempo de Operação": f'{intervalo_de_operacao}',
                        "Tempo trabalhando": f'{tempo_total}',
                        "Tempo Ocioso": f'{intervalo_de_operacao - tempo_total}',
                        },
                        "Relativos" : {
                            "Tempo de Operação": f'{tempo_total/intervalo_de_operacao}',
                            "Tempo Ocioso": f'{(intervalo_de_operacao - tempo_total)/intervalo_de_operacao}'
                        }
                        }
        else:
            final_dict[key] = "Sem dados de operação"
    return final_dict

def generate_graphs(final_dict):
    fig, axes = plt.subplots(2, 3, figsize=(10, 6))
    for i in final_dict.keys():
        # try:
            value_1 = float(final_dict[i]["Relativos"]["Tempo de Operação"]) 
            value_2 = float(final_dict[i]["Relativos"]["Tempo Ocioso"]) 
            ax = axes[len(final_dict[i]) // 3, len(final_dict[i])% 3]
            row = row[row.gt(row.sum() * .01)]
            ax.pie(row, labels=row.index, startangle=30)
            ax.set_title(i)
            ax.pie([value_1, value_2], autopct=lambda x:str(round(x,2))+'%')

            # # Adicionando os nomes das categorias como rótulos
            # ax.xticks([0.1]*2, ["Working", "Idle"])
            # ax.set_title(i)
            # ax.legend(loc="best")
            # Mostrando o gráfico na tela
            plt.show()
        # except:
        #     pass



resultado = query_time_and_value_in_mongo()
aux_dict = create_dict_with_tupled_values(resultado)
time_diff =  get_time_diff(aux_dict)

generate_graphs(time_diff)