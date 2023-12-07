import time
import opcua

from alarms.alarm import mostrar_alerta
from utils.db_utils import create_collection


def check_inserted_documents(collection, interval=1 ):
    previous_count = collection.count_documents({})
    while True:
        current_count = collection.count_documents({})
        if current_count != previous_count:
            difference = current_count - previous_count
            if difference > 0:
                # logger_mongodb.info(f"Comando enviado via API")
                try:
                    station = collection.find().limit(1).sort([('$natural',-1)])
                    set_stop_station(station)
                except Exception as e:
                    raise e
            else:
                print(f"{-difference} documento(s) foi/foram removido(s) da coleção")
            previous_count = current_count
        time.sleep(interval)

def set_stop_station(station):
        stations = {"Distributing":"opc.tcp://localhost:4840", #"opc.tcp://192.168.1.10:4840", 
            "PickAndPlace":"opc.tcp://localhost:4840",#"opc.tcp://192.168.1.20:4840",
            "Sorting":"opc.tcp://localhost:4840"} #"opc.tcp://192.168.1.30:4840"}
        
        client = opcua.Client(stations[station[0]["station"]])
        client.connect()
        node = client.get_node("ns=2;i=25") # Get in Stop Tag
        # tag1 = node.set_value(False) # Write Stop Tag
        node.set_value(False)
        # logger_mongodb.critical(f"Comando enviado para bancada: {station[0]['station']}")
        mostrar_alerta(station[0]["station"])

def check_documents():
    while True:
        value = check_inserted_documents(create_collection())
        yield value