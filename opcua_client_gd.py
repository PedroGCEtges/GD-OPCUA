import datetime
import logging
import sqlite3
import sys

from utils.db_utils import add_tags_to_sqlite, create_collection, create_sqlite, mongo_client
from log.logs_config import set_log
import opcua
import time
from log.log_utils import log_map_opc


def connect_to_gd_opcua(opc="opc.tcp://localhost:4840"):
    client = opcua.Client(opc)
    try:
        client.connect()
        root = client.get_root_node()
        logging.critical(f"Conexão estabelecida com o servidor OPC UA da bancada {log_map_opc[opc]}")
        return root
    except ConnectionRefusedError as e:
        print(e, opc)
        return 0

    except Exception as e:
        print(e)
        exit()
        # client.disconnect()

def read_tags_from_gd(sqlite, mongodb, mongocol, opc="opc.tcp://localhost:4840"):   
    if mongodb == None or mongocol == None:
        mongo_db = mongo_client()["Teste"]
        mongo_col = mongo_db["teste"] 
    else:
        mongo_db = mongo_client()[mongodb]
        mongo_col = mongo_db[mongocol] 
    
    try:
        root = connect_to_gd_opcua(opc)

        while True:
            tags_dict, tags_sqlite = get_tags(root)
            set_log(tags_dict)
            
            
            doc = {"timestamp": datetime.datetime.now(),
               "stations": log_map_opc[opc],
               "tags": tags_dict}
            mongo_col.insert_one(doc)

            add_tags_to_sqlite(tags_sqlite, create_sqlite(sqlite))
            # time.sleep(0.2)
            # print(tags[23]) #Stop tag
    except AttributeError as e:
        print(e)
        return 0
    
def get_tags(root_node):
    tags = []
    tags_sqlite = []

    children = root_node.get_children()[0].get_children()[1].get_children() ## TEST OPCUA SERVER
    # children = root_node.get_child(["0:Objects","3:ServerInterfaces"]).get_children()[0].get_children() #OFFICAL PATH
    
    # print(children)
    for child in children:
        if child.get_node_class() == opcua.ua.NodeClass.Variable:
            tags.append({"timestamp": child.get_data_value().SourceTimestamp.isoformat(), 
                         "name":child.get_display_name().Text, 
                         "value": child.get_value()})
            
            tags_sqlite.append([child.get_data_value().SourceTimestamp.isoformat(), 
                               child.get_display_name().Text,
                               child.get_value()])
        elif child.get_node_class() == opcua.ua.NodeClass.Object:
            tags.extend(get_tags(child))
            tags_sqlite.extend(get_tags(child))

    return tags, tags_sqlite

# connect_to_gd_opcua('opc.tcp://192.168.1.10:4840')
# read_tags_from_gd()