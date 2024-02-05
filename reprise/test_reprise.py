import sqlite3
import pandas as pd

# Conectar ao banco de dados SQLite (isso cria um arquivo chamado 'exemplo.db' no diretório atual)
conn = sqlite3.connect('exemplo.db')

# Criar tabelas de entrada e saída
entrada = pd.DataFrame({'valor': [1, 2, 3],
                        'timestamp_delta': [10, 20, 30]})

saida = pd.DataFrame({'valor': [4, 5, 6],
                      'timestamp_delta': [35, 45, 55]})

# Inserir dados nas tabelas do banco de dados
entrada.to_sql('entrada', conn, index=False, if_exists='replace')
saida.to_sql('saida', conn, index=False, if_exists='replace')

# Consulta SQL para criar a tabela 'Ciclo'
query = '''
    CREATE TABLE Ciclo AS
    SELECT
        e.timestamp_delta AS Inicio,
        s.timestamp_delta AS Fim,
        s.timestamp_delta - e.timestamp_delta AS Processamento
    FROM entrada e
    JOIN saida s ON e.valor = s.valor;
'''

# Executar a consulta para criar a tabela 'Ciclo'
conn.execute(query)

# Fechar a conexão com o banco de dados
conn.close()
