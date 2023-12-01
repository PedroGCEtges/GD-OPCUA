# Criando um servidor gRPC
from opcua_servicer import OpcuaService
import opcua_pb2
import opcua_pb2_grpc
import grpc

server = grpc.server(grpc.thread_pool_executor(max_workers=10))
# Adicionando o serviço OpcuaService ao servidor
opcua_pb2_grpc.add_OpcuaServiceServicer_to_server(OpcuaService(), server)
# Definindo a porta que o servidor irá escutar
server.add_insecure_port("[::]:50051")
# Iniciando o servidor
server.start()
# Mantendo o servidor em execução
server.wait_for_termination()
