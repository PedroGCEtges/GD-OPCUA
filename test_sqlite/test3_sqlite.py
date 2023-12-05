# importar as bibliotecas pandas e sqlite3
import pandas as pd
import sqlite3

# criar uma conexão com o banco de dados sqlite
conn = sqlite3.connect("opcua.db")

# criar um dataframe com os dados da tabela opcua_data usando o método read_sql
df = pd.read_sql("SELECT * FROM opcua_data", conn)

# salvar o dataframe em um arquivo xlsx usando o método to_excel
df.to_excel("opcua_data.xlsx", index=False)

# fechar a conexão com o banco de dados
conn.close()
