#Los estudiantes desarrollarán una aplicación con interfaz gráfica que permita 
# mostrar por pantalla la hora, la fecha, la temperatura, el clima, la velocidad 
# del viento. También debe contar con un botón que al momento de presionarlo, 
# muestre una alerta con un dato al azar sobre gatos, o puede ser también un consejo.#
import requests  # libreria para hacer peticiones a una API
from customtkinter import *
import customtkinter  # interfaz grafica
from datetime import date  # libreria para fechas
from tkinter import messagebox  # libreria para mostrar mensajes emergentes
from PIL import Image, ImageTk  # Importamos ImageTk para usar imágenes en Tkinter/customtkinter
import io  # Para manejar datos binarios de la imagen descargada
import random  # libreria para generar numeros aleatorios

# -----------------------------------------------------------------------------
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
# Función para mostrar un consejo
def consejo():
    # URL para obtener un dato al azar sobre gatos, como se solicitó originalmente,
    # aunque la API actual es de consejos generales.
    # Si quisieras datos de gatos, podrías usar: https://catfact.ninja/fact
    url = " https://api.adviceslip.com/advice"

    consejos = requests.get(url).json()
    consejo = consejos["slip"]["advice"]
    messagebox.showinfo("Consejo del día", consejo)
# funcion para cerrar la ventana
def cerrar():
    app.destroy()
# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA INTERFAZ
# -----------------------------------------------------------------------------

app = CTk()
app.title("Reloj Nacional")
app.resizable(False, False)
mi_fuente = customtkinter.CTkFont(family="Arial", size=25)
fontm = mi_fuente

# Etiquetas
etiqueta1 = CTkLabel(app, text="vacio porque si", font=fontm)
etiqueta1.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
FechaHoy = date.today()
etiqueta2 = CTkLabel(app, text=f"Fecha: {FechaHoy}", font=fontm)
etiqueta2.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

etiqueta3 = CTkLabel(app, text="", font=fontm)
etiqueta3.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

# Botones
boton1 = CTkButton(app, text="Mostrar consejo", font=fontm, command=consejo)
boton1.grid(row=3, column=0, padx=2, pady=5)
boton2 = CTkButton(app, text="Salir", font=fontm, command=cerrar)
boton2.grid(row=3, column=1, padx=2, pady=5)
# -----------------------------------------------------------------------------
# Carga de Imagen desde Internet
# -----------------------------------------------------------------------------

# URL de ejemplo para una imagen (puedes cambiarla por cualquier URL directa a una imagen .jpg/.png)
urlimagen = "https://tse3.mm.bing.net/th/id/OIP.-G-78rg-94vPDcdrceKXUgHaD4?rs=1&pid=ImgDetMain&o=7&rm=3"
medida = (450, 250)  # Tamaño deseado para la imagen

try:
    # 1. Descargar la imagen
    respuesta = requests.get(urlimagen)
    respuesta.raise_for_status()  # Verificar si la descarga fue exitosa
    imagen_original = Image.open(io.BytesIO(respuesta.content))

    # 3. Redimensionar y convertir para customtkinter
    imagen_redimensionada = imagen_original.resize(medida)
    global imagen_tk  # Hacemos global para evitar que Python la elimine (garbage collection)
    imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
    # 4. Crear widget de imagen
    etiqueta_imagen = CTkLabel(app, image=imagen_tk, text="")
    etiqueta_imagen.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

except requests.exceptions.RequestException as e:
    # Manejar errores de descarga (sin internet, URL incorrecta, etc.)
    print(f"Error al descargar la imagen: {e}")
    etiqueta_imagen = CTkLabel(app, text="[No se pudo cargar la imagen]", font=fontm, fg_color="gray")
    etiqueta_imagen.grid(row=4, column=0, padx=5, pady=5, columnspan=2)
actualizar_reloj()
obtenerClima()
app.mainloop()