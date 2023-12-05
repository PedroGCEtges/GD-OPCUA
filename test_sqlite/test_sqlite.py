import opcua
import sqlite3

from db_utils import mongo_client


# read_tags_from_gd()
# tags = get_tags()

client = opcua.Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()

# obter as tags do servidor OPC UA
tags = client.get_root_node().get_children()[0].get_children()[1].get_children() 

# criar um cliente MongoDB e se conectar ao banco de dados MongoDB
mongo_client = mongo_client()
mongo_db = mongo_client["opcua_db"]
mongo_col = mongo_db["opcua_data"]

# criar uma conexão SQLite e se conectar ao banco de dados SQLite
sqlite_conn = sqlite3.connect("opcua.db")
sqlite_cur = sqlite_conn.cursor()

# criar uma tabela SQLite se não existir
sqlite_cur.execute("CREATE TABLE IF NOT EXISTS opcua_data (tag TEXT, value TEXT, timestamp TEXT)")

# percorrer as tags e salvar os dados em ambos os bancos de dados
for tag in tags:
    # obter o nome, o valor e o carimbo de data/hora da tag
    name = tag.get_display_name().Text
    value = tag.get_value()
    timestamp = tag.get_data_value().SourceTimestamp.isoformat()

    # criar um documento MongoDB com os dados da tag
    mongo_doc = {"tag": name, "value": value, "timestamp": timestamp}

    # inserir o documento MongoDB na coleção MongoDB
    mongo_col.insert_one(mongo_doc)

    # criar uma tupla SQLite com os dados da tag
    sqlite_row = (name, value, timestamp)

    # inserir a tupla SQLite na tabela SQLite
    sqlite_cur.execute("INSERT INTO opcua_data VALUES (?,?,?)", sqlite_row)

    # confirmar as alterações na tabela SQLite
    sqlite_conn.commit()

# fechar a conexão SQLite
sqlite_conn.close()

# desconectar o cliente OPC UA
client.disconnect()
