import sqlite3

def create_tag_tables(cursor, conn):
    cursor.execute("SELECT tag, GROUP_CONCAT(value) AS value, GROUP_CONCAT(timestamp) AS timestamps FROM opcua_data GROUP BY tag")
    results = cursor.fetchall()
    # Iterar sobre as tags únicas do resultado
    for row in results:
        try:
            # Obter o nome da tag
            tag = row[0]
            # Separar os valores e os timestamps por vírgula
            values = row[1].split(",")
            timestamps = row[2].split(",")
            if not(tag == "0" or tag == "1"):
                
                # Criar uma nova tabela com o nome da tag
                cursor.execute(f"CREATE TABLE \"{tag}\" (id INTEGER PRIMARY KEY, value INTEGER, timestamp TEXT)")
                # Inserir os valores e os timestamps na nova tabela
                count = 0
                for i in range(len(values)):
                    cursor.execute(f"INSERT INTO \"{tag}\" VALUES (?, ?, ?)", (count,values[i], timestamps[i]))
                    count += 1
                    
        except sqlite3.OperationalError as e:
            if str(e) == f'table "{tag}" already exists':
                count = 0
                for i in range(len(values)):
                    cursor.execute(f"INSERT INTO {tag} VALUES (?, ?,?)", (count, values[i], timestamps[i]))
                    # cursor.execute(f"ALTER TABLE {tag} ADD COLUMN id INTEGER PRIMARY KEY")
                    count += 1
            else:
                print(e)
                
    # Salvar as alterações no banco de dados
    conn.commit()
