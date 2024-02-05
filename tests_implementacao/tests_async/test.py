import asyncio

# Criar a primeira função assíncrona que roda um while True
async def funcao1():
    # Criar uma variável para armazenar o resultado da função
    resultado1 = 0
    # Criar um loop infinito
    while True:
        # Incrementar o resultado em 1
        resultado1 += 1
        # Imprimir o resultado
        print(f"Função 1: {resultado1}")
        # Aguardar um segundo antes de repetir o loop
        await asyncio.sleep(1)
        # Retornar o resultado
        return resultado1

# Criar a segunda função assíncrona que roda um while True
async def funcao2():
    # Criar uma variável para armazenar o resultado da função
    resultado2 = 0
    # Criar um loop infinito
    while True:
        # Incrementar o resultado em 2
        resultado2 += 2
        # Imprimir o resultado
        print(f"Função 2: {resultado2}")
        # Aguardar um segundo antes de repetir o loop
        await asyncio.sleep(1)
        # Retornar o resultado
        return resultado2

# Criar uma função assíncrona que executa as duas funções assíncronas e interfere uma na outra
async def funcao3():
    # Criar um loop infinito
    while True:
        # Executar a primeira função assíncrona e obter o seu retorno
        r1 = await funcao1()
        # Executar a segunda função assíncrona e obter o seu retorno
        r2 = await funcao2()
        # Se o retorno da primeira função for par, multiplicar o retorno da segunda função por 2
        if r1 % 2 == 0:
            r2 *= 2
        # Se o retorno da primeira função for ímpar, dividir o retorno da segunda função por 2
        else:
            r2 /= 2
        # Imprimir o novo resultado da segunda função
        print(f"Função 2 alterada: {r2}")
        # Aguardar um segundo antes de repetir o loop
        await asyncio.sleep(1)

# Executar a função assíncrona que executa as duas funções assíncronas e interfere uma na outra
# asyncio.run(funcao3())
