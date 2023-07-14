#Ya funciona la terminal y el asistente 
import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import openai
from gtts import gTTS
from pygame import mixer
import pyttsx3
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

    # Crea un hilo para ejecutar la función main() en segundo plano
    hilo_main = threading.Thread(target=main)
    hilo_main.start()

# Crear la ventana
ventana = tk.Tk()

# Añadir un título a la ventana
ventana.title("Asistente De Voz")

# Crear una etiqueta
etiqueta = tk.Label(ventana, text="¡Hola, bienvenido!")
etiqueta.pack()

# Establecer el tamaño de la ventana
ventana.geometry("400x400")

# Crear un botón con la función asignada
boton = tk.Button(ventana, text="Haz clic aquí", command=iniciar_asistente)
boton.pack()

# Crear un widget Text para mostrar el texto generado
terminal = tk.Text(ventana, height=10, width=40)
terminal.pack()

# Redirigir la salida estándar a la terminal
class TerminalRedirector:
    def __init__(self, terminal_widget):
        self.terminal_widget = terminal_widget

    def write(self, message):
        self.terminal_widget.insert(tk.END, message)
        self.terminal_widget.see(tk.END)

sys.stdout = TerminalRedirector(terminal)

# Cargar el archivo GIF
archivo_gif = "C:/Users/0w0/Documents/Code/Micro.gif"
imagen = Image.open(archivo_gif)
frame = ImageTk.PhotoImage(imagen)

# Crear una etiqueta y mostrar el GIF
etiqueta_imagen = tk.Label(ventana, image=frame)
etiqueta_imagen.pack()

# Ejecutar el bucle principal de la ventana
ventana.mainloop()


##romper el for y esperar que hasta que no vuelva a presiona el boton deje de oir, con un if condifciona
## Cuando diga la palabra de romper ciclo cierra tambien la interfaz 