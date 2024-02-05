# Importando os arquivos gerados pelo compilador do gRPC
import opcua_pb2
import opcua_pb2_grpc

# Importando o módulo grpc
import grpc

# Importando o módulo opcua-client
import opcua

# Criando uma classe que herda de OpcuaServiceServicer
class OpcuaService(opcua_pb2_grpc.OpcuaServiceServicer):
  # Implementando o método Notify
  def Notify(self, request, context):
    # Recebendo a mensagem com o valor da tag OPC UA
    tag = request.tag
    value = request.value
    # Conectando ao servidor OPC UA
    client = opcua.Client("opc.tcp://localhost:4840")
    client.connect()
    # Escrevendo o valor na tag OPC UA
    client.write_value(tag, value)
    # Desconectando do servidor OPC UA
    client.disconnect()
    # Retornando uma mensagem vazia
    return opcua_pb2.EmptyMessage()
