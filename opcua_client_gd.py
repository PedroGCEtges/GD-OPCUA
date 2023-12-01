import logging
import sqlite3

from db_utils import create_collection, mongo_client
from logs_config import set_log
import opcua
import time
from log_utils import log_map_opc


# mongo_client = mongo_client()
# mongo_db = mongo_client["opcua_db"]
# mongo_col = mongo_db["opcua_data"]

# # criar uma conexão SQLite e se conectar ao banco de dados SQLite
# sqlite_conn = sqlite3.connect("opcua.db")
# sqlite_cur = sqlite_conn.cursor()

# # criar uma tabela SQLite se não existir
# sqlite_cur.execute("CREATE TABLE IF NOT EXISTS opcua_data (tag TEXT, value TEXT, timestamp TEXT)")

def connect_to_gd_opcua(opc="opc.tcp://localhost:4840"):
    client = opcua.Client(opc)
    try:
        client.connect()
        root = client.get_root_node()
        logging.critical(f"Conexão estabelecida com o servidor OPC UA da bancada {log_map_opc[opc]}")
        return root
    
    except Exception as e:
        print(e)
        client.disconnect()

def read_tags_from_gd(opc="opc.tcp://localhost:4840"):    
        root = connect_to_gd_opcua(opc)
        while True:
            tags = get_tags(root)
            set_log(tags)
            time.sleep(0.2)
            print(tags[23]) #Stop tag

def get_tags(root_node):
    tags = []

    children = root_node.get_children()[0].get_children()[1].get_children() ## TEST OPCUA SERVER
    # children = root_node.get_child(["0:Objects","3:ServerInterfaces"]).get_children()[0].get_children() #OFFICAL PATH
    
    # print(children)
    for child in children:
        if child.get_node_class() == opcua.ua.NodeClass.Variable:
            tags.append((child.get_display_name().Text, child.get_value()))
        elif child.get_node_class() == opcua.ua.NodeClass.Object:
            tags.extend(get_tags(child))
            
    return tags

# connect_to_gd_opcua('opc.tcp://192.168.1.10:4840')
read_tags_from_gd()