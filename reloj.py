import requests
from customtkinter import *
import customtkinter
app = CTk()
app.title("Reloj Nacional")
app.resizable(False, False)
mi_fuente = customtkinter.CTkFont(family="Arial", size=55)
fontm=mi_fuente
# Etiquetas iniciales
etiqueta1 = CTkLabel(app, text="", font=fontm)
etiqueta1.grid(row=0, column=0, padx=5, pady=5)


# Función para actualizar la hora
def actualizar_reloj():
    url = "https://timeapi.io/api/time/current/zone?timeZone=America%2FGuatemala"
    datos = requests.get(url).json()
    hora = datos["hour"]
    minutos = datos["minute"]
    segundos = datos["seconds"]

    etiqueta1.configure(text=f"Hora: {hora}:{minutos}:{segundos}", font=fontm)
    # Llama a esta función de nuevo dentro de 1000 ms
    app.after(1000, actualizar_reloj)


# Llamar la función por primera vez
actualizar_reloj()

app.mainloop()