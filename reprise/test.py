import pandas as pd

# Exemplo de dados
dados_1 = {'Inicio': ['2020-02-11 17:45:10.000665', '2020-02-13 15:56:41.000790', '2020-02-16 10:38:56.000607'],
           'Fim': ['2020-01-01 16:24:28.000978', '2020-01-10 17:07:42.000550', '2020-02-04 23:24:47.000613']}
df_1 = pd.DataFrame(dados_1)

dados_2 = {'Inicio': ['2020-02-12 17:45:10.000665', '2020-02-14 15:56:41.000790', '2020-02-17 10:38:56.000607'],
           'Fim': ['2020-01-02 16:24:28.000978', '2020-01-11 17:07:42.000550', '2020-02-05 23:24:47.000613']}
df_2 = pd.DataFrame(dados_2)

# Converter as colunas para datetime
df_1['Inicio'] = pd.to_datetime(df_1['Inicio'])
df_1['Fim'] = pd.to_datetime(df_1['Fim'])

df_2['Inicio'] = pd.to_datetime(df_2['Inicio'])
df_2['Fim'] = pd.to_datetime(df_2['Fim'])

# Ordenar os DataFrames
df_1 = df_1.sort_values(by='Inicio').reset_index(drop=True)
df_2 = df_2.sort_values(by='Inicio').reset_index(drop=True)

# Filtrar df_2 com base na condição
df_2_filtrado = pd.DataFrame(columns=df_2.columns)

for index, row in df_2.iterrows():
    idx_df1 = (df_1['Fim'] - row['Inicio']).abs().idxmin()
    if df_1.loc[idx_df1, 'Fim'] < row['Inicio']:
        df_2_filtrado = pd.concat([df_2_filtrado, row.to_frame().T])

# Exibir os DataFrames resultantes
print("DataFrame df_1:")
print(df_1)

print("\nDataFrame df_2_filtrado:")
print(df_2_filtrado.reset_index(drop=True))
