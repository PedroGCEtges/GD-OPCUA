import threading
import subprocess
import sys
import json
import os

# Evento para sinalizar a ocorrência de uma exceção
erro_detectado = threading.Event()

def start_program(program_name, resultado_compartilhado):
    global erro_detectado  # Declare a variável global

    try:
        if erro_detectado.is_set():
            print("Erro detectado em outra thread. Encerrando.")
            return

        # Obter o caminho do interpretador Python usado no script atual
        python_interpreter = sys.executable

        # Executar o script usando o mesmo interpretador Python
        process = subprocess.Popen([python_interpreter, program_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error running {program_name}. Stderr: {stderr}")
            status = {'nome': program_name, 'status': 'Erro'}
            erro_detectado.set()  # Define o evento de erro
        else:
            status = {'nome': program_name, 'status': 'Concluído'}

    except Exception as e:
        print(f"Error running {program_name}: {e}")
        status = {'nome': program_name, 'status': 'Erro'}
        erro_detectado.set()  # Define o evento de erro

    # Adiciona o status ao arquivo compartilhado
    resultado_compartilhado.append(status)
    print(f"Status adicionado para {program_name}")
# # Restante do código permanece o mesmo...
    
def main():
    files = ["client_dist.py", "client_pp.py", "client_sort.py", "middleware.py"]
    resultado_compartilhado = []
    thread_encerrar_evento = threading.Event()

    threads = []
    try:
        for file in files:
            t = threading.Thread(target=start_program, args=(file, resultado_compartilhado))
            threads.append(t)
            t.start()

        thread_encerrar_evento.set()
        # Aguarda até que todas as threads terminem ou ocorra um erro
        for t in threads:
            t.join()

        if erro_detectado.is_set():
            print("Uma exceção ocorreu em uma das threads. Encerrando todas as threads.")
            for t in threads:
                t.join(timeout=0)  # Força a finalização das threads restantes
            os._exit(0)

        # Grava o resultado compartilhado em um arquivo JSON
        with open('resultado_compartilhado.json', 'w') as file:
            json.dump(resultado_compartilhado, file)

        # Exibir ou processar os resultados conforme necessário
        for resultado in resultado_compartilhado:
            print(f"Programa: {resultado['nome']}, Status: {resultado['status']}")

    except Exception as e:
        print(f"Erro geral: {e}")
        os._exit(0)

if __name__ == "__main__":
    main()
