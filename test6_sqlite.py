import sqlite3

import pandas as pd


conn = sqlite3.connect("opcua.db")
cursor = conn.cursor()
query1 = "CREATE TABLE peca (inicio_ciclo TEXT,fim_ciclo TEXT, tampa BOOLEAN, material TEXT, cor TEXT);"
query2 = "INSERT INTO peca (inicio_ciclo) SELECT timestamp FROM \"B_I4\";"
query3 = "INSERT INTO peca (fim_ciclo) SELECT timestamp FROM \"G3\";"
query4 = "UPDATE peca SET tampa = CASE WHEN (SELECT COUNT(*) FROM \"B_I4\" WHERE id = peca.id) > 0 THEN TRUE ELSE FALSE END;"
query5="UPDATE peca SET tampa = CASE WHEN (SELECT COUNT(*) FROM \"G3\" WHERE id = peca.id) > 0 THEN TRUE ELSE FALSE END;"
query6="DELETE FROM peca WHERE tampa = FALSE;"

numeros = [query1,query2, query3]#, query4, query5, query6]
inicio = pd.read_sql_query('SELECT * FROM \"B_I4\"', conn)
fim =  pd.read_sql_query('SELECT * FROM \"G3\"', conn)
fim.rename(columns={'value': 'value_fim'}, inplace=True)
fim.rename(columns={'timestamp': 'timestamp_fim'}, inplace=True)
fim.rename(columns={'timestamp_delta': 'timestamp_delta_fim'}, inplace=True)

inicio.rename(columns={'value': 'value_inicio'}, inplace=True)
inicio.rename(columns={'timestamp': 'timestamp_inicio'}, inplace=True)
df = pd.concat([inicio, fim], axis=1)

# df.loc[df['value_inicio'] == 0 and df['value_fim'] == 0]
# df = df.loc[~df['value_inicio'].isin ([0, 0]) & ~df['value_fim'].isin ([0, 0])]
# df = df.drop(df['value_inicio'].isin([0, 0]) & df['value_fim'].isin([0, 0]))
df.dropna(subset=['value_inicio', 'value_fim'], inplace=True)
print(df)

# for i in numeros:
#     cursor.execute(i)
# conn.commit()
# cursor.execute(query3)
# cursor.execute(query4)
# cursor.execute(query5)
# cursor.execute(f"DROP TABLE \"peca\"")