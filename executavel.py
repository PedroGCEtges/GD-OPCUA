from tkinter import *
from tkcalendar import DateEntry
import subprocess

# Criar a janela principal
janela = Tk()
janela.title("Exemplo de interface gráfica")

# Definir uma função para abrir a segunda janela
def abrir_segunda_janela():
    # Criar a segunda janela
    segunda_janela = Toplevel()
    segunda_janela.title("Reprise")

    # Criar os elementos da segunda janela
    label_inicio = Label(segunda_janela, text="Data de início:")
    label_fim = Label(segunda_janela, text="Data de fim:")
    entrada_inicio = DateEntry(segunda_janela, format="%d/%m/%Y")
    entrada_fim = DateEntry(segunda_janela, format="%d/%m/%Y")
    botao_ok = Button(segunda_janela, text="OK")

    # Posicionar os elementos na segunda janela
    label_inicio.grid(row=0, column=0, padx=10, pady=10)
    label_fim.grid(row=1, column=0, padx=10, pady=10)
    entrada_inicio.grid(row=0, column=1, padx=10, pady=10)
    entrada_fim.grid(row=1, column=1, padx=10, pady=10)
    botao_ok.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Definir uma função para abrir a terceira janela
def abrir_terceira_janela():
    # Criar a terceira janela
    terceira_janela = Toplevel()
    terceira_janela.title("Running")

    # Criar um elemento de texto na terceira janela
    texto = Label(terceira_janela, text="Running GD")
    texto.pack(padx=10, pady=10)

    texto2 = Label(terceira_janela, text="Texto 2")
    texto2.pack(padx=10, pady=10)

    texto3 = Label(terceira_janela, text="Texto 3")
    texto3.pack(padx=10, pady=10)

    texto4 = Label(terceira_janela, text="Texto 4")
    texto4.pack(padx=10, pady=10)

    # Executar o código python que está na mesma pasta do projeto
    subprocess.run(["python", "main.py"])

# Criar os botões da janela principal
botao_iniciar = Button(janela, text="Iniciar GD",command=abrir_terceira_janela)
botao_reprise = Button(janela, text="Reprise", command=abrir_segunda_janela)

# Posicionar os botões na janela principal
botao_iniciar.pack(side=LEFT, padx=10, pady=10)
botao_reprise.pack(side=RIGHT, padx=10, pady=10)

# Iniciar o loop principal da janela
janela.mainloop()
