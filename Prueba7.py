# Aqui ya reemplaza el jpg por el gif pero no se mueve

import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import openai
from gtts import gTTS
from pygame import mixer
import os
import time as ti
import random
import sys
import threading

openai.api_key = "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"

def transformar_audio_a_texto():
    r = sr.Recognizer()
    with sr.Microphone() as origen:
        r.pause_threshold = 0.8
        print("Ya puedes hablar!")
        audio = r.listen(origen)
        try:
            pedido = r.recognize_google(audio, language="es-HN")
            print("You: " + pedido)
            return pedido

        except sr.UnknownValueError:
            print("Ups, no entendi!")
            return "Sigo esperando"

        except sr.RequestError:
            print("Ups, no hay servicio!")
            return "Sigo esperando"

        except:
            print("Ups, algo salio mal!")
            return "Sigo esperando"

def hablar(mensaje):
    volume = 0.7
    tts = gTTS(mensaje, lang="es", slow=False)
    ran = random.randint(0, 9999)
    filename = 'Temp' + format(ran) + '.mp3'
    tts.save(filename)
    mixer.init()
    mixer.music.load(filename)
    mixer.music.set_volume(volume)
    mixer.music.play()

    while mixer.music.get_busy():
        ti.sleep(0.3)

    mixer.quit()
    os.remove(filename)

def main():
    conversation = ""

    hablar("Hola! Soy Demo tu asistente personal, ¿en qué puedo ayudarte?")

    while True:
        question = transformar_audio_a_texto().lower()
        if question == "salir demo":
            break
        conversation += "\nYou: " + question + "\nDemo:"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=conversation,
            temperature=0.5,
            max_tokens=1000,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["\n", " You:", " Demo:"]
        )
        answer = response.choices[0].text.strip()
        conversation += answer
        print("Demo: " + answer + "\n")
        hablar(answer)

def iniciar_asistente():
    etiqueta.config(text="¡Hola, has clicado el botón!")
    imagen_path = "Micro.gif"
    imagen_gif = Image.open(imagen_path)
    imagen_gif = imagen_gif.resize((100, 100), Image.BICUBIC)
    imagen_gif = ImageTk.PhotoImage(imagen_gif)
    boton.config(image=imagen_gif)  # Configurar la imagen del botón
    boton.image = imagen_gif  # Actualizar referencia de la imagen
    sys.stdout = TerminalWriter(terminal)
    threading.Thread(target=main).start()

class TerminalWriter:
    def __init__(self, terminal):
        self.terminal = terminal

    def write(self, text):
        self.terminal.insert(tk.END, text)
        self.terminal.see(tk.END)

# Crear la ventana y los elementos
ventana = tk.Tk()
ventana.title("Asistente De Voz")
etiqueta = tk.Label(ventana, text="¡Hola, bienvenido!")
etiqueta.pack()
ventana.geometry("400x400")
archivo_png = "Micro.png"
imagen = Image.open(archivo_png)
imagen = imagen.resize((100, 100), Image.BICUBIC)
imagen = ImageTk.PhotoImage(imagen)
boton = tk.Button(ventana, image=imagen, command=iniciar_asistente)
boton.pack()
terminal = tk.Text(ventana, height=10, width=40)
terminal.pack(fill=tk.BOTH, expand=True)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
