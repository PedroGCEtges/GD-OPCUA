# Importar a classe Client e a classe Node da biblioteca opcua
from opcua import Client, Node

# Criar uma instância do Client passando o endereço do servidor opcua
client = Client("opc.tcp://localhost:4840")

# Conectar-se ao servidor
client.connect()

# Obter o nó raiz do servidor
root = client.get_root_node()

print(root.get_children()[0].get_children()[1].get_children()[0].get_browse_name())
# # Obter o nó dos objetos do servidor
# objects = client.get_objects_node()

# # Obter o nó do objeto que contém as tags que você quer acessar
# # Você pode usar o método get_child passando o identificador do nó, por exemplo:
# myobj = objects.get_child("ns=2;i=1")

# # Você também pode usar o método get_children para obter uma lista de todos os nós filhos do objeto, por exemplo:
# myobj_children = myobj.get_children()

# # Para acessar as tags dentro do nó do objeto, você pode usar o método get_variables, que retorna uma lista de nós que são variáveis, por exemplo:
# mytags = myobj.get_variables()

# # Você também pode usar o método get_children para obter uma lista de todos os nós filhos do objeto, e filtrar os que são variáveis usando o método is_variable, por exemplo:
# mytags = [node for node in myobj_children if node.is_variable()]

# # Para ler o valor de cada tag, você pode usar o método get_value, por exemplo:
# for tag in mytags:
#     value = tag.get_value()
#     # Imprimir o nome e o valor da tag
#     print(tag, value)

# # Desconectar-se do servidor
# client.disconnect()
