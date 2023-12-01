# Importando os arquivos gerados pelo compilador do gRPC
import opcua_pb2
import opcua_pb2_grpc

# Importando o módulo grpc
import grpc

# Importando o módulo pymongo
import pymongo

# Criando um cliente gRPC que se conecta ao serviço OpcuaService
channel = grpc.insecure_channel("localhost:50051")
stub = opcua_pb2_grpc.OpcuaServiceStub(channel)

# Criando um cliente MongoDB que se conecta ao banco de dados
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test"]
collection = db["users"]

# Abrindo um fluxo de mudanças na coleção "users" usando o método watch
change_stream = collection.watch()

# Iterando sobre o cursor do fluxo de mudanças e enviando as notificações ao serviço OpcuaService
for change in change_stream:
  # Verificando se o evento é uma operação de inserção
  if change["operationType"] == "insert":
    # Obtendo o documento inserido
    document = change["fullDocument"]
    # Obtendo o valor da tag OPC UA
    tag = document["tag"]
    value = document["value"]
    # Criando uma mensagem com o valor da tag OPC UA
    message = opcua_pb2.OpcuaMessage(tag=tag, value=value)
    # Invocando o método Notify do serviço OpcuaService
    response = stub.Notify(message)
    # Imprimindo a resposta
    print(response)
