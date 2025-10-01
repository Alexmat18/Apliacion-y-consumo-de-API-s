#Los estudiantes desarrollarán una aplicación con interfaz gráfica que permita 
# mostrar por pantalla la hora, la fecha, la temperatura, el clima, la velocidad 
# del viento. También debe contar con un botón que al momento de presionarlo, 
# muestre una alerta con un dato al azar sobre gatos, o puede ser también un consejo.#

import requests#libreria para hacer peticiones a una API
from customtkinter import *#
import customtkinter#interfaz grafica
from datetime import date# libreria para fechas y 
from tkinter import messagebox#libreria para mostrar mensajes emergentes
from PIL import Image
import io
import random#libreria para generar numeros aleatorios
# FUCNCIONES
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

# -----------------------------------------------------------------------------
# Función para obtener datos del clima
def obtenerClima():
    url = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    lat = "14.634915"
    lon = "-90.506882"
    url = url.replace("{lat}", lat).replace("{lon}", lon)
    datos = requests.get(url).json()
    temperatura = datos["current_weather"]["temperature"]  # grados celsius
    viento = datos["current_weather"]["windspeed"]  # km/h

    etiqueta3.configure(text=f"Temperatura: {temperatura}°C\nViento: {viento} km/h", font=fontm)
    # Llamar la función por primera vez
    app.after(60000, obtenerClima)  # actualiza cada 60 segundos

# -----------------------------------------------------------------------------
# Función para mostrar  un consejo
def consejo():
    url = "	https://api.adviceslip.com/advice"
    consejos = requests.get(url).json()
    consejo = consejos["slip"]["advice"]
    messagebox.showinfo("Consejo del día", consejo)
# funcion para cerrar la ventana
def cerrar():
    app.destroy()
app = CTk()
app.title("Reloj Nacional")
app.resizable(False, False)
mi_fuente = customtkinter.CTkFont(family="Arial", size=25)
fontm=mi_fuente
# etiqueta para mostrar la hora
etiqueta1 = CTkLabel(app, text="", font=fontm)
etiqueta1.grid(row=0, column=0, padx=5, pady=5, columnspan=1)

# fecha Hoy y etiqueta para mostrarla
FechaHoy = date.today()
etiqueta2 = CTkLabel(app, text=f"Fecha: {FechaHoy}", font=fontm)
etiqueta2.grid(row=1, column=0, padx=5, pady=5,columnspan=1)
# etiqueta para mostrar el clima
etiqueta3 = CTkLabel(app, text="", font=fontm)
etiqueta3.grid(row=2, column=0, padx=5, pady=5,columnspan=1)
# Botón para mostrar un consejo
boton1 = CTkButton(app, text="Mostrar consejo", font=fontm, command=consejo)
boton1.grid(row=3, column=0, padx=2, pady=5)
boton2=CTkButton(app, text="Salir",font=fontm, command=cerrar)
boton2.grid(row=3, column=1)
actualizar_reloj()
obtenerClima()
#-----------------------------------------------------------------------------

app.mainloop()