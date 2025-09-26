#Los estudiantes desarrollarán una aplicación con interfaz gráfica que permita 
# mostrar por pantalla la hora, la fecha, la temperatura, el clima, la velocidad 
# del viento. También debe contar con un botón que al momento de presionarlo, 
# muestre una alerta con un dato al azar sobre gatos, o puede ser también un consejo.#

import requests#libreria para hacer peticiones a una API
from customtkinter import *#
import customtkinter#interfaz grafica
from datetime import date# libreria para fechas y horas

app = CTk()
app.title("Reloj Nacional")
app.resizable(False, False)
mi_fuente = customtkinter.CTkFont(family="Arial", size=55)
fontm=mi_fuente
# Etiquetas iniciales
etiqueta1 = CTkLabel(app, text="", font=fontm)
etiqueta1.grid(row=0, column=0, padx=5, pady=5)

#fecha Hoy
FechaHoy = date.today()
etiqueta2 = CTkLabel(app, text=f"Fecha: {FechaHoy}", font=fontm)
etiqueta2.grid(row=1, column=0, padx=5, pady=5)
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