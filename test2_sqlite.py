# importar o módulo sqlite3
import sqlite3

# criar uma conexão com o banco de dados SQLite
conn = sqlite3.connect("opcua.db")

# criar um objeto cursor
cursor = conn.cursor()

# executar uma consulta SQL para selecionar todos os dados da tabela opcua_data
cursor.execute("SELECT * FROM opcua_data")

# obter todos os registros da tabela usando o método fetchall()
dados = cursor.fetchall()

# percorrer os registros e imprimir cada um
for registro in dados:
    print(registro)

# fechar a conexão com o banco de dados
conn.close()
