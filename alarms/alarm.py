# Importando as bibliotecas necessárias
from tkinter import *
from tkinter import messagebox
from pygame import mixer

janela = Tk()

def tocar_buzina():
    mixer.init()
    mixer.music.load("alarms/alarm.mp3")
    mixer.music.play(0)


def parar_buzina():
    mixer.music.stop()


def mostrar_alerta(station):
    tocar_buzina()
    janela.attributes("-topmost", True)
    janela.withdraw()

    messagebox.showwarning("Alerta", f"Bancada {station} parada via API.")

    parar_buzina()
    janela.deiconify()
    janela.destroy()

# janela.after(0, mostrar_alerta("Test"))

# janela.mainloop()
