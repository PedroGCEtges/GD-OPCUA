from opcua import ua, Server
from utils.server_utils import create_variables_to_test, update_values

def create_gd_opcua_sim(opctcp="opc.tcp://localhost:4840", uri="https://example.com/opcua"):
    server = Server()
    server.set_endpoint(opctcp)

    idx = server.register_namespace(uri)

    root = server.get_objects_node()

    myobj = root.add_object(idx, "MyObject")

    lista = create_variables_to_test(myobj, idx)
    lista = lista[1:]


    server.start()

    try:
        print("Servidor OPC UA iniciado")
        while True:
            update_values(lista)

    finally:
        server.stop()
        print("Servidor OPC UA parado")
        
# create_gd_opcua_sim()
# create_gd_opcua_sim("opc.tcp://localhost:4841", "https://example.com/opcua1" )