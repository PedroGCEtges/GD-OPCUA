import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import dateutil.parser 
import copy

def converter_segundos(segundos):
    dias = segundos // 86400
    segundos = segundos % 86400
    horas = segundos // 3600
    segundos = segundos % 3600
    minutos = segundos // 60
    segundos = segundos % 60
    segundos = f"{segundos:.4f}"
    return f"{int(dias)}:{int(horas)}:{int(minutos)}:{segundos}"

def get_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    names = cursor.fetchall()
    return names


def remove_repeatead_timestamps(names, cursor, conn):
#### QUERY PARA REMOVER TIMESTAMPS REPETIDOS ###########
    for name in names[1:]:
        cursor.execute(f"DELETE FROM {name[0]} WHERE timestamp IN (SELECT timestamp FROM {name[0]} GROUP BY timestamp HAVING COUNT(*) > 1) AND rowid NOT IN (SELECT MIN(rowid) FROM {name[0]} GROUP BY timestamp HAVING COUNT(*) > 1)")
        conn.commit()
# cursor.execute(f'SELECT timestamp FROM G1')
# timestamps = cursor.fetchall()
# df = pd.DataFrame(timestamps, columns=['timestamp'])

def get_cursor_and_conn(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    return cursor, conn

def get_first_time_in_interval_from_station_tables(tables, cursor, start='2023-12-10', end='2023-12-19'):
    start = dateutil.parser.parse(start).strftime("%Y-%m-%dT%H:%M:%S.%f")
    end = dateutil.parser.parse(end).strftime("%Y-%m-%dT%H:%M:%S.%f")
    first_value_tables = {}

    for name in tables:
        if name[0] != 'opcua_data':
            cursor.execute(f'SELECT MIN(timestamp) FROM {name[0]} WHERE timestamp BETWEEN \"{start}\" AND \"{end}\"')
            timestamps = cursor.fetchall()
            first_value_tables[name[0]] = timestamps[0][0]
    return first_value_tables

def get_first_value_in_interval(intervals):
    d = copy.deepcopy(intervals)
    for key, value in intervals.items():
        d[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
    oldest = min(d.items(), key=lambda x: x[1])
    return oldest

### TRATAR TIMESTAMPS E NORMALIZAR #########
def normalize_timestamps(tables, cursor, conn, first_time):
    for name in tables:
        if name[0] != 'opcua_data':
            cursor.execute(f'SELECT timestamp FROM {name[0]} ORDER BY timestamp ASC')
            timestamps = cursor.fetchall()
            
            dp = pd.read_sql_query(f"SELECT * FROM {name[0]}", conn)

            df = pd.DataFrame(timestamps, columns=['timestamp_delta'])
            # data_inicial = df['timestamp_delta'].iloc[0]
            format_string = "%Y-%m-%dT%H:%M:%S.%f"
            for i in range(len(df['timestamp_delta'])):
                seconds = (datetime.strptime(df['timestamp_delta'][i], format_string) -  datetime.strptime(first_time[1].strftime(format_string), format_string)).total_seconds()

                df['timestamp_delta'][i] = converter_segundos(seconds)
            
            add_timestamp = f"ALTER TABLE {name[0]} ADD COLUMN timestamp_delta TEXT"
            cursor.execute(add_timestamp)
            dp = dp.join(df["timestamp_delta"])
            dp.to_sql(name[0], conn, if_exists='replace', index=False)


cursor, conn = get_cursor_and_conn("opcua.db")
names = get_tables(cursor)
d = get_first_time_in_interval_from_station_tables(names,cursor)
x = get_first_value_in_interval(d)
normalize_timestamps(names, cursor, conn, x)

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