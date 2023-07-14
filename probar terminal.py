import tkinter as tk

def verificar_texto():
    texto = terminal.get("1.0", "end-1c")  # Obtener el texto ingresado sin el carácter de nueva línea
    if texto == "hola":
        terminal.insert(tk.END, "\nEs un éxito")  # Agregar el mensaje con un salto de línea antes

ventana = tk.Tk()

terminal = tk.Text(ventana, height=10, width=40)
terminal.pack()

terminal.bind("<Return>", lambda event: verificar_texto())

ventana.mainloop()
