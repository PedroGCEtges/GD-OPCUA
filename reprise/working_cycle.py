from datetime import datetime, timedelta 
import sqlite3
import pandas as pd

'''Casos possíveis:
(Talvez seja possível pegar o estado do ciclo atual utilizando a tag de M_STATUS)
0 - 0: Intervalo começa com os dois sem pegar presença, então, se 0-0, buscar o próximo 1.
1 - 0: Ciclo perfeito, começa com disparo de entrada na bancada 
0 - 1: Fim de um ciclo anterior não registrado por inteiro
1 - 1: Fim de um ciclo anterior e início de outro

Assumirei que o caso 1 - 1 não seja possível de ocorrer, seria algo como uma falha no sistema.
'''

''' O que falta?
- Determinar as tags para classificar a montagem das peças
- Determinar a partir dessas tags uma tabela com status de montagem das peças

'''

def set_station_cycle(conn, sensor_entrada="B_I4", sensor_saida="G3"):
    inicio = pd.read_sql_query(f'SELECT * FROM \"{sensor_entrada}\"', conn)
    fim =  pd.read_sql_query(f'SELECT * FROM \"{sensor_saida}\"', conn)
    fim.rename(columns={'value': 'value_fim'}, inplace=True)
    fim.rename(columns={'timestamp': 'timestamp_fim'}, inplace=True)
    fim.rename(columns={'timestamp_delta': 'timestamp_delta_fim'}, inplace=True)

    inicio.rename(columns={'value': 'value_inicio'}, inplace=True)
    inicio.rename(columns={'timestamp': 'timestamp_inicio'}, inplace=True)
    df = pd.concat([inicio, fim], axis=1)
    return df

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

def create_df_for_every_table(cursor, conn):
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
                dfs[key] = value.drop(value.iloc[:index].index, axis=0, inplace=True)
                new_list.append((key, value))
                # print(len(dfs))
            else:
                new_list.append((key,value))
        return new_list

    except Exception as e:
        raise e

def generate_intervals_table(list_of_dfs_tuple, conn):
    try:
        for df in list_of_dfs_tuple:
            df[1].to_sql(df[0]+'_intervaled', conn, if_exists='replace', index=False)

    except TypeError as e:
        raise e
    
def check_piece_status(tag, conn, df, caracteristica = 'Tampada'):
    time = pd.read_sql_query(f'SELECT * FROM \"{tag}\"', conn)
    time.rename(columns={'timestamp_delta': 'timestamp_delta_meio'}, inplace=True)
    
    cycle_init = df.loc[(df['value_inicio'] == 1)].reset_index()
    cycle_end = df.loc[(df['value_fim'] == 1)].reset_index()
    cycle_mid = time.loc[(time['value'] == 1)].reset_index()
    
    cycle_dict = {}
    cycle_dict['start_datetime'] = cycle_init['timestamp_inicio'] 
    cycle_dict['start'] = cycle_init['timestamp_delta']
    cycle_dict['mid_datetime'] = cycle_mid['timestamp']
    cycle_dict['mid'] = cycle_mid['timestamp_delta_meio']
    cycle_dict['end_datetime'] = cycle_end['timestamp_fim'] 
    cycle_dict['end'] = cycle_end['timestamp_delta_fim']

    cycle_df = pd.DataFrame(cycle_dict)

    def check_cycle(start_, mid_, end_, row, lista_aux, peca, caracteristica):
            correct_cycle = (((mid_ - start_).total_seconds() >= 0) and ((end_ - mid_).total_seconds() >= 0))
            
            if correct_cycle:
                lista_aux.append({'time_operation':row['mid'], 'time_in': row['start'], 'time_out': row['end']})
            peca[caracteristica] = lista_aux
    

    peca = {}
    lista_aux = []
    for index,row in cycle_df.iterrows():
        start_, mid_, end_ = row['start'], row['mid'], row['end']
        if isinstance(start_,float):
            continue
        if isinstance(mid_,float):
            continue
        if isinstance(end_,float):
            continue

        start_ = datetime.strptime(start_[2:], "%H:%M:%S.%f")
        mid_ = datetime.strptime(mid_[2:], "%H:%M:%S.%f")
        end_ = datetime.strptime(end_[2:], "%H:%M:%S.%f")

        fim = int(row['end'].split(':',)[0])
        inicio = int(row['start'].split(':',)[0])
        days = fim - inicio

        if days == 0:
            check_cycle(start_, mid_, end_, row, lista_aux, peca, caracteristica)

        # if days == 1:
        #     diff = (end_ - start_).total_seconds()
        #     if diff < 0:
        #         diff = diff + 86400
                
    return peca

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
