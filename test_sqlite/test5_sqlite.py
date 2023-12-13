import sqlite3
import pandas as pd

conn = sqlite3.connect("opcua.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

names = cursor.fetchall()
# print(names)

#### QUERY PARA REMOVER TIMESTAMPS REPETIDOS ###########
# for name in names[1:]:
#     print(name[0])
#     cursor.execute(f"DELETE FROM {name[0]} WHERE timestamp IN (SELECT timestamp FROM {name[0]} GROUP BY timestamp HAVING COUNT(*) > 1) AND rowid NOT IN (SELECT MIN(rowid) FROM {name[0]} GROUP BY timestamp HAVING COUNT(*) > 1)")
#     conn.commit()

for name in names[1:]:
    writer = pd.ExcelWriter(f"{name[0]}.xlsx")
    df = pd.read_sql(f'SELECT * FROM {name[0]} ORDER BY timestamp ASC', conn)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(df.head())
    df.to_excel(writer, sheet_name=f"{name[0]}", index=False)
# for name in names:
#     if 'opcua_data_filtered' == name[0]:
#         print(name[0])
#         cursor.execute(f"DROP TABLE \"{name[0]}\"")

