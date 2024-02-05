import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

def generate_random_timestamp():
    # Gerar valores aleatórios para ano, mês, dia, hora e minuto
    year = random.randint(2020, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Assumindo um valor máximo de 28 para simplificar
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    seconds = random.randint(0,59)
    mili = random.randint(0,999)

    # Criar um objeto de data e hora
    random_datetime = datetime(year, month, day, hour, minute, seconds, mili)

    # Formatar o objeto de data e hora como uma string no formato desejado
    formatted_timestamp = random_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')

    return formatted_timestamp

# Exemplo de uso
random_timestamp = generate_random_timestamp()

def random_loop(a=None, b=None):
    lista = []
    if a!= None:
        for i in range(a):
            lista.append(generate_random_timestamp())
        return lista
    
    if b!=None:
        # Gerar um número aleatório de iterações
        num_iterations = random.randint(b, 100)  # Pode ajustar o intervalo conforme necessário
        
        # Executar o loop
        for i in range(num_iterations):
            lista.append(generate_random_timestamp())
        return lista
    num_iterations = random.randint(50, 100)  # Pode ajustar o intervalo conforme necessário
        
    # Executar o loop
    for i in range(num_iterations):
        lista.append(generate_random_timestamp())
    return lista

def encontrar_mais_proximo(df):
    idx = np.searchsorted(df['Fim'], df['Inicio'])
    idx = np.clip(idx, 0, len(df['Fim']) - 1)
    df['MaisProximo'] = df['Fim'].iloc[idx]
    return df

# Supondo que você já tenha os DataFrames correspondentes às tabelas A, B e C
# Substitua A_df, B_df e C_df pelos seus DataFrames reais

# Exemplo de criação de DataFrames fictícios (substitua com seus DataFrames reais)
a = random_loop()
b = random_loop(b=len(a))
c = random_loop(b=len(a))

A_df = pd.DataFrame({'Inicio': a,
                     'Fim':  random_loop(len(a))})

A_df['Inicio'] = pd.to_datetime(A_df['Inicio'])
A_df['Fim'] = pd.to_datetime(A_df['Fim'])

A_df[['Inicio', 'Fim']] = A_df[['Inicio', 'Fim']].apply(lambda x: sorted(x)).reset_index(drop=True)


A_df['Fim'] = A_df['Inicio'].apply(lambda x: A_df['Fim'][A_df['Fim'] > x].min())
A_df = A_df.dropna(subset=['Fim']).reset_index(drop=True)

B_df = pd.DataFrame({'Inicio':  b,
                     'Fim':  random_loop(len(b))})

C_df = pd.DataFrame({'Inicio':  c,
                     'Fim':  random_loop(len(c))})

B_df['Inicio'] = pd.to_datetime(B_df['Inicio'])
B_df['Fim'] = pd.to_datetime(B_df['Fim'])

C_df['Inicio'] = pd.to_datetime(C_df['Inicio'])
C_df['Fim'] = pd.to_datetime(C_df['Fim'])

B_df[['Inicio', 'Fim']] = B_df[['Inicio', 'Fim']].apply(lambda x: sorted(x)).reset_index(drop=True)
B_df['Fim'] = B_df['Inicio'].apply(lambda x: B_df['Fim'][B_df['Fim'] > x].min())
B_df = B_df.dropna(subset=['Fim']).reset_index(drop=True)

C_df[['Inicio', 'Fim']] = C_df[['Inicio', 'Fim']].apply(lambda x: sorted(x)).reset_index(drop=True)
C_df['Fim'] = C_df['Inicio'].apply(lambda x: C_df['Fim'][C_df['Fim'] > x].min())
C_df = C_df.dropna(subset=['Fim']).reset_index(drop=True)

# A_df['min_date'] = A_df[['Inicio', 'Fim']].min(axis=1)
# A_df = A_df.sort_values(['min_date', 'Fim']).drop('min_date', axis=1).reset_index(drop=True)

print(len(A_df), len(B_df),len(C_df))

D_df = pd.DataFrame({'Inicio':  A_df['Fim'],
                     'Fim':  B_df['Inicio']})
D_df[['Inicio', 'Fim']] = D_df[['Inicio', 'Fim']].apply(lambda x: sorted(x)).reset_index(drop=True)
D_df['Fim'] = D_df['Inicio'].apply(lambda x: D_df['Fim'][D_df['Fim'] > x].min())
D_df = D_df.dropna(subset=['Fim']).reset_index(drop=True)
D_df.drop_duplicates(subset=['Inicio', 'Fim'])
print(D_df)

E_df = pd.DataFrame({'Inicio':  B_df['Fim'],
                     'Fim':  C_df['Inicio']})
E_df[['Inicio', 'Fim']] = E_df[['Inicio', 'Fim']].apply(lambda x: sorted(x)).reset_index(drop=True)
E_df['Fim'] = E_df['Inicio'].apply(lambda x: E_df['Fim'][E_df['Fim'] > x].min())
E_df = E_df.dropna(subset=['Fim']).reset_index(drop=True)
E_df.drop_duplicates(subset=['Inicio', 'Fim'])
print(E_df)
