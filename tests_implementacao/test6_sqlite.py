from datetime import datetime 
import sqlite3
import pandas as pd

conn = sqlite3.connect("opcua.db")
cursor = conn.cursor()

def set_station_cycle(sensor_entrada="B_I4", sensor_saida="G3"):
    inicio = pd.read_sql_query(f'SELECT * FROM \"{sensor_entrada}\"', conn)
    fim =  pd.read_sql_query(f'SELECT * FROM \"{sensor_saida}\"', conn)
    fim.rename(columns={'value': 'value_fim'}, inplace=True)
    fim.rename(columns={'timestamp': 'timestamp_fim'}, inplace=True)
    fim.rename(columns={'timestamp_delta': 'timestamp_delta_fim'}, inplace=True)

    inicio.rename(columns={'value': 'value_inicio'}, inplace=True)
    inicio.rename(columns={'timestamp': 'timestamp_inicio'}, inplace=True)
    df = pd.concat([inicio, fim], axis=1)
    return df
'''Casos possíveis:
(Talvez seja possível pegar o estado do ciclo atual utilizando a tag de M_STATUS)
0 - 0: Intervalo começa com os dois sem pegar presença, então, se 0-0, buscar o próximo 1.
1 - 0: Ciclo perfeito, começa com disparo de entrada na bancada 
0 - 1: Fim de um ciclo anterior não registrado por inteiro
1 - 1: Fim de um ciclo anterior e início de outro

Assumirei que o caso 1 - 1 não seja possível de ocorrer, seria algo como uma falha no sistema.
'''

def search_first_cycle(df):
    index_first_init = (df['value_inicio'] == 1).idxmax()
    index_first_end = (df['value_fim'] == 1).idxmax()
    
    if index_first_init > index_first_end:
        #Indica que estava no meio do processo entre as datas.
        #Então o novo ciclo de simulação começa a partir do proximo first = 1
        #Pois posso não ter informações suficientes para determinar a peça.
        df.drop([i for i in range(index_first_end)], axis=0, inplace=True)
        return df, index_first_end

    if index_first_init < index_first_end:
        #ciclo ok
        print("Ciclo Ok")

    if index_first_init == index_first_end:
        print("Erro")
    
    return df, -1

def filter_false_start_end_values(df):
    for i, row in df.iterrows():
        if row['value_inicio'] == 0 and row['value_fim'] == 0:
            df.drop(i, axis=0, inplace=True)
            continue
    return df

def calculate_cycle_time(df):
    time_diff = {}
    format_string = '%H:%M:%S.%f'

    for i, row in df.iterrows():
        timer = datetime.strptime(row['timestamp_delta_fim'][2:], format_string) - datetime.strptime(row['timestamp_delta'][2:], format_string)
        if timer.total_seconds() < 0:
            print("Ciclo estranho")
        
        fim = int(row['timestamp_delta_fim'].split(':',)[0])
        inicio = int(row['timestamp_delta'].split(':',)[0])
        days = fim - inicio

        time_diff[i] = f'{days}:' + str(timer)

    return time_diff

def get_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    names = cursor.fetchall()
    return names

def create_df_for_every_table(cursor=cursor):
    all_df = {}
    tables = get_tables(cursor)
    for table in tables:
        if table[0] != 'opcua_data':
            x = pd.read_sql_query(f'SELECT * FROM \"{table[0]}\"', conn)
            all_df[table[0]] = x
    return all_df

def get_cycle(df):
    try:
        df_1, index = search_first_cycle(df)
        return df_1, index
    
    except Exception as e:
        print(str(e))
        df_1,index = search_first_cycle(df)
        return df_1, index

def filter_rows(dfs,df):    
    try:
        new_list = []
        df_1, index = get_cycle(df)
        for key, value in dfs.items():
            if index != -1:
                dfs[key] = value.drop([i for i in range(index)], axis=0, inplace=True)
                new_list.append((key, value))
        return new_list

    except Exception as e:
        print(e)
        pass

def generate_intervals_table(list_of_dfs_tuple):
    for df in list_of_dfs_tuple:
        df[1].to_sql(df[0]+'_intervaled', conn, if_exists='replace', index=False)

df = set_station_cycle()
df['value_inicio'][0:11] = 0
df['value_fim'][0:9] = 0
df['value_fim'][10] = 1

dfs = create_df_for_every_table()
new_df = filter_rows(dfs, df)
generate_intervals_table(new_df)

# query1 = "CREATE TABLE peca (inicio_ciclo TEXT,fim_ciclo TEXT, tampa BOOLEAN, material TEXT, cor TEXT);"
# query2 = "INSERT INTO peca (inicio_ciclo) SELECT timestamp FROM \"B_I4\";"
# query3 = "INSERT INTO peca (fim_ciclo) SELECT timestamp FROM \"G3\";"
# query4 = "UPDATE peca SET tampa = CASE WHEN (SELECT COUNT(*) FROM \"B_I4\" WHERE id = peca.id) > 0 THEN TRUE ELSE FALSE END;"
# query5="UPDATE peca SET tampa = CASE WHEN (SELECT COUNT(*) FROM \"G3\" WHERE id = peca.id) > 0 THEN TRUE ELSE FALSE END;"
# query6="DELETE FROM peca WHERE tampa = FALSE;"
# numeros = [query1,query2, query3]

# for i in numeros:
#     cursor.execute(i)
# conn.commit()
# cursor.execute(query3)
# cursor.execute(query4)
# cursor.execute(query5)
# cursor.execute(f"DROP TABLE \"peca\"")
