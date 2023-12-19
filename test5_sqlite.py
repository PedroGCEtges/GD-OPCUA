import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import decimal

def converter_segundos(segundos):
    dias = segundos // 86400
    segundos = segundos % 86400
    horas = segundos // 3600
    segundos = segundos % 3600
    minutos = segundos // 60
    segundos = segundos % 60
    segundos = f"{segundos:.4f}"
    return f"{int(dias)}:{int(horas)}:{int(minutos)}:{segundos}"

conn = sqlite3.connect("opcua.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

names = cursor.fetchall()

#### QUERY PARA REMOVER TIMESTAMPS REPETIDOS ###########
for name in names[1:]:
    cursor.execute(f"DELETE FROM {name[0]} WHERE timestamp IN (SELECT timestamp FROM {name[0]} GROUP BY timestamp HAVING COUNT(*) > 1) AND rowid NOT IN (SELECT MIN(rowid) FROM {name[0]} GROUP BY timestamp HAVING COUNT(*) > 1)")
    conn.commit()
# cursor.execute(f'SELECT timestamp FROM G1')
# timestamps = cursor.fetchall()
# df = pd.DataFrame(timestamps, columns=['timestamp'])

### TRATAR TIMESTAMPS E NORMALIZAR #########
test2 = []
for name in names[1:]:
    cursor.execute(f'SELECT timestamp FROM {name[0]} ORDER BY timestamp ASC')
    timestamps = cursor.fetchall()
    
    dp = pd.read_sql_query(f"SELECT * FROM {name[0]}", conn)

    df = pd.DataFrame(timestamps, columns=['timestamp_delta'])
    data_inicial = df['timestamp_delta'].iloc[0]
    format_string = "%Y-%m-%dT%H:%M:%S.%f"
    test = []
    for i in range(len(df['timestamp_delta'])):
        seconds = (datetime.strptime(df['timestamp_delta'][i], format_string) -  datetime.strptime(data_inicial, format_string)).total_seconds()

        df['timestamp_delta'][i] = converter_segundos(seconds)
    
    add_timestamp = f"ALTER TABLE {name[0]} ADD COLUMN timestamp_delta TEXT"
    cursor.execute(add_timestamp)
    dp = dp.join(df["timestamp_delta"])
    print(dp.head())
    dp.to_sql(name[0], conn, if_exists='replace', index=False)




    # for i in test:
    #         print()
    #         cursor.execute(f"UPDATE {name[0]} SET timestamp = {i} WHERE id = {test.index(i)}") 

        
    # except Exception as e:
    #     print(e)
    #     pass



# for name in names[1:]:
#     writer = pd.ExcelWriter(f"{name[0]}.xlsx")
#     df = pd.read_sql(f'SELECT * FROM {name[0]} ORDER BY timestamp ASC', conn)
#     df.drop_duplicates(inplace=True)
#     df.reset_index(drop=True, inplace=True)
#     print(df.head())
#     df.to_excel(writer, sheet_name=f"{name[0]}", index=False)