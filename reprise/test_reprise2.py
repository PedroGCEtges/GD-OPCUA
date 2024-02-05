import sqlite3
import pandas as pd

# Função para converter o formato do timestamp
def converter_timestamp(timestamp):
    return pd.to_datetime(timestamp)

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('exemplo.db')

# Lista de nomes de tabelas
tabelas = ['entrada1', 'saida1', 'entrada2', 'saida2', 'entrada3', 'saida3']

# Verificar se as tabelas têm o mesmo número de dados e comparar datas de início e fim
for i in range(0, len(tabelas), 2):
    tabela_inicio = tabelas[i]
    tabela_fim = tabelas[i + 1]

    # Consulta SQL para obter dados ordenados por data de início e fim
    query_inicio = f'SELECT * FROM {tabela_inicio} ORDER BY Inicio, Fim;'
    query_fim = f'SELECT * FROM {tabela_fim} ORDER BY Inicio, Fim;'

    # Ler os dados em DataFrames Pandas
    df_inicio = pd.read_sql_query(query_inicio, conn, parse_dates=['Inicio', 'Fim'])
    df_fim = pd.read_sql_query(query_fim, conn, parse_dates=['Inicio', 'Fim'])

    # Verificar se estão em ordem crescente com base na data de início
    if (df_inicio['Inicio'].diff().dt.total_seconds() >= 0).all():
        print(f'As tabelas {tabela_inicio} estão em ordem crescente com base na data de início.')
    else:
        print(f'As tabelas {tabela_inicio} NÃO estão em ordem crescente com base na data de início.')

    # Comparar datas de início e fim entre Equipamento 1 e Equipamento 2
    if (df_inicio['Fim'] <= df_fim['Inicio']).all():
        print(f'Datas de fim em {tabela_inicio} são sempre anteriores ou iguais às datas de início em {tabela_fim}.')
    else:
        print(f'Datas de fim em {tabela_inicio} não são sempre anteriores ou iguais às datas de início em {tabela_fim}.')

# Fechar a conexão com o banco de dados
conn.close()
