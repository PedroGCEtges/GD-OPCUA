# importar as bibliotecas pandas e sqlite3
import pandas as pd
import sqlite3

# criar uma conexão com o banco de dados sqlite
conn = sqlite3.connect("opcua.db")
cursor = conn.cursor()

cursor.execute("SELECT tag, GROUP_CONCAT(value) AS value, GROUP_CONCAT(timestamp) AS timestamps FROM opcua_data GROUP BY tag")

df = pd.DataFrame(cursor.fetchall(), columns=["tag", "value", "timestamps"])

conn.close()
writer = pd.ExcelWriter("resultado.xlsx")

for tag in df["tag"].unique():
    # Filtrar o dataframe pela tag atual
    df_tag = df[df["tag"] == tag]
    # Separar os valores e os timestamps por vírgula
    df_tag.loc[:, "value"] = df_tag.loc[:, "value"].str.split(",")
    df_tag.loc[:, "timestamps"] = df_tag.loc[:, "timestamps"].str.split(",")
    # Expandir os valores e os timestamps em colunas
    df_tag = df_tag.explode("value")
    df_tag = df_tag.explode("timestamps")
    # Remover a coluna tag
    df_tag = df_tag.drop("tag", axis=1)
    # Escrever o dataframe em uma planilha com o nome da tag
    df_tag.to_excel(writer, sheet_name=tag, index=False)

# Escrever o dataframe em uma planilha chamada "resultado"
# df.to_excel(writer, sheet_name="resultado", index=False)
# Salvar e fechar o arquivo excel
writer._save()

