# Importar o módulo multiprocessing
import multiprocessing

# Criar um objeto Queue
queue = multiprocessing.Queue()

# Criar uma função que insere um item na fila
def put_item(item):
    queue.put(item)
    print(f"Processo {multiprocessing.current_process().name} inseriu {item} na fila")

# Criar uma função que remove um item da fila
def get_item():
    item = queue.get()
    print(f"Processo {multiprocessing.current_process().name} removeu {item} da fila")

# Criar uma lista de itens para inserir na fila
items = ["a", "b", "c", "d"]

# Criar quatro processos que executam a função put_item com um item da lista como argumento
processes = []
for item in items:
    process = multiprocessing.Process(target=put_item, args=(item,))
    processes.append(process)
    process.start()

# Esperar que os processos terminem
for process in processes:
    process.join()

# Criar quatro processos que executam a função get_item sem argumentos
processes = []
for i in range(4):
    process = multiprocessing.Process(target=get_item)
    processes.append(process)
    process.start()

# Esperar que os processos terminem
for process in processes:
    process.join()
