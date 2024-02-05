# def start_program(program_name):
#     try:
#         os.system('python {}'.format(program_name))
#         status = {'nome': program_name, 'status': 'Concluído'}
#     except Exception as e:
#         print(f"Error running {program_name}: {e}")
#         status = {'nome': program_name, 'status': 'Erro'}

#     return status

# def main():
#     files = ["client_dist.py", "client_pp.py", "client_sort.py", "middleware.py"]
#     resultados = []

#     threads = []
#     try:
#         for file in files:
#             t = threading.Thread(target=start_program, args=(file,))
#             threads.append(t)
#             t.start()

#         for t in threads:
#             t.join()
#             # Obter o status da thread
#             resultado = t._result if hasattr(t, '_result') else {'nome': None, 'status': 'Erro ao obter resultado'}
#             resultados.append(resultado)

#         # Exibir ou processar os resultados conforme necessário
#         for resultado in resultados:
#             print(f"Programa: {resultado['nome']}, Status: {resultado['status']}")

#     except Exception as e:
#         print(f"Erro geral: {e}")
#         os._exit(0)

# if __name__ == "__main__":
#     main()
