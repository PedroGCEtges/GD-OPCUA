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
        cursor.execute(f"DELETE FROM \"{name[0]}\" WHERE timestamp IN (SELECT timestamp FROM \"{name[0]}\" GROUP BY timestamp HAVING COUNT(*) > 1) AND rowid NOT IN (SELECT MIN(rowid) FROM \"{name[0]}\" GROUP BY timestamp HAVING COUNT(*) > 1)")
        conn.commit()

def get_cursor_and_conn(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    return cursor, conn

def get_first_time_in_interval_from_station_tables(tables, cursor, start, end):
    start = dateutil.parser.parse(start).strftime("%Y-%m-%dT%H:%M:%S.%f")
    end = dateutil.parser.parse(end).strftime("%Y-%m-%dT%H:%M:%S.%f")
    first_value_tables = {}

    try:
        for name in tables:
            if name[0] != 'opcua_data':
                cursor.execute(f'SELECT MIN(timestamp) FROM \"{name[0]}\" WHERE timestamp BETWEEN \"{start}\" AND \"{end}\"')
                timestamps = cursor.fetchall()
                first_value_tables[name[0]] = timestamps[0][0]
        return first_value_tables
    
    except TypeError as e:
        print(e)
        raise Exception("Intervalo de datas sem dados ou inválido!")

def get_first_value_in_interval(intervals):
    try: 
        d = copy.deepcopy(intervals)
        for key, value in intervals.items():
            d[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        oldest = min(d.items(), key=lambda x: x[1])
        return oldest
    
    except TypeError as e:
        raise Exception("Sem dados no intervalo de datas informado!")

### TRATAR TIMESTAMPS E NORMALIZAR #########
def normalize_timestamps(tables, cursor, conn, first_time,start,end):
    try:
        for name in tables:
            if name[0] != 'opcua_data':
                cursor.execute(f'SELECT timestamp FROM \"{name[0]}\" WHERE timestamp BETWEEN \"{start}\" AND \"{end}\" ORDER BY timestamp ASC')
                timestamps = cursor.fetchall()
                
                dp = pd.read_sql_query(f"SELECT * FROM \"{name[0]}\" WHERE timestamp BETWEEN \"{start}\" AND \"{end}\"", conn)

                df = pd.DataFrame(timestamps, columns=['timestamp_delta'])
                # data_inicial = df['timestamp_delta'].iloc[0]
                format_string = "%Y-%m-%dT%H:%M:%S.%f"
                for i in range(len(df['timestamp_delta'])):
                    if verificar_formato(df['timestamp_delta'][i]):
                        df['timestamp_delta'][i] = datetime.strptime(df['timestamp_delta'][i], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S.%f')
                    seconds = (datetime.strptime(df['timestamp_delta'][i], format_string) -  datetime.strptime(first_time[1].strftime(format_string), format_string)).total_seconds()

                    df['timestamp_delta'][i] = converter_segundos(seconds)
                
                add_timestamp = f"ALTER TABLE \"{name[0]}\" ADD COLUMN timestamp_delta TEXT"
                cursor.execute(add_timestamp)
                dp = dp.join(df["timestamp_delta"])
                dp.to_sql(name[0], conn, if_exists='replace', index=False)
    
    except TypeError:
        raise Exception("Objeto nulo!")
    
    except sqlite3.OperationalError:
        print("Coluna já existente")
        pass


def verificar_formato(string):
  try:
    formato = '%Y-%m-%dT%H:%M:%S'
    data_hora = datetime.strptime(string, formato)
    print(data_hora)
    # Se a conversão for bem sucedida, retornar True
    return True
  except ValueError:
    # Se a conversão falhar, retornar False
    return False