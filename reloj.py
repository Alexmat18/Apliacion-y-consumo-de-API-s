#Los estudiantes desarrollarán una aplicación con interfaz gráfica que permita 
# mostrar por pantalla la hora, la fecha, la temperatura, el clima, la velocidad 
# del viento. También debe contar con un botón que al momento de presionarlo, 
# muestre una alerta con un dato al azar sobre gatos, o puede ser también un consejo.#
import requests  # libreria para hacer peticiones a una API
from customtkinter import *
import customtkinter  # interfaz grafica
from datetime import date  # libreria para fechas
from tkinter import messagebox  # libreria para mostrar mensajes emergentes
from PIL import Image, ImageTk
import io  # Para manejar datos binarios de la imagen descargada
import random  # libreria para generar numeros aleatorios


# -----------------------------------------------------------------------------
# FUCNCIONES
# Función auxiliar para cargar y actualizar la imagen
def cargar_imagen_clima(url_imagen):
    """Descarga, procesa y actualiza la imagen del clima en la etiqueta."""
    try:
        global imagen_tk  # Usamos global para mantener la referencia

        # 1. Descargar la imagen
        respuesta = requests.get(url_imagen)
        respuesta.raise_for_status()

        # 2. Abrir y redimensionar
        imagen_original = Image.open(io.BytesIO(respuesta.content))
        imagen_redimensionada = imagen_original.resize(medida)

        # 3. Convertir y asignar a la etiqueta
        # Nota: Usamos ImageTk.PhotoImage porque es lo que estaba en tu código original
        imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
        etiqueta_imagen.configure(image=imagen_tk, text="")
        etiqueta_imagen.image = imagen_tk  # Previene que la imagen sea borrada

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar o procesar la imagen: {e}")
        etiqueta_imagen.configure(image=None, text="[Error al cargar imagen]", fg_color="gray")
    except Exception as e:
        print(f"Error desconocido en carga de imagen: {e}")


# Función para actualizar la hora
def actualizar_reloj():
    url = "https://timeapi.io/api/time/current/zone?timeZone=America%2FGuatemala"
    datos = requests.get(url).json()
    hora = datos["hour"]
    minutos = datos["minute"]
    segundos = datos["seconds"]

    etiqueta1.configure(text=f"Hora: {hora}:{minutos}:{segundos}", font=fontm)
    app.after(1000, actualizar_reloj)


# -----------------------------------------------------------------------------
# Función para obtener datos del clima (MODIFICADA CON IF/ELIF)
def obtenerClima():
    url = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    lat = "14.634915"
    lon = "-90.506882"
    url = url.replace("{lat}", lat).replace("{lon}", lon)

    datos = requests.get(url).json()
    temperatura = datos["current_weather"]["temperature"]  # grados celsius
    viento = datos["current_weather"]["windspeed"]  # km/h
    # 1. OBTENER EL CÓDIGO DE CONDICIÓN (WMO)
    wmo_code = datos["current_weather"]["weathercode"]

    # 2. MAPEO DEL CÓDIGO A DESCRIPCIÓN Y URL USANDO IF/ELIF

    # URLS DE EJEMPLO: Sol, Nubes, Lluvia, Niebla/Nieve
    URL_SOL = "https://es.pngtree.com/freepng/sunny-sky-with-sun-light-and-clouds_8624520.html"
    URL_NUBES = "https://i.imgur.com/qzfX84g.jpeg"
    URL_LLUVIA = "https://www.bing.com/images/search?view=detailV2&ccid=TkPUhhXk&id=A80C5BA23B96000363233059DF445800D8405496&thid=OIP.TkPUhhXk8YbVPjtkq7WIyAHaE7&mediaurl=https%3a%2f%2fimg.freepik.com%2ffoto-gratis%2fcomposicion-efectos-meteorologicos_23-2149853295.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.4e43d48615e4f186d53e3b64abb588c8%3frik%3dllRA2ABYRN9ZMA%26pid%3dImgRaw%26r%3d0&exph=417&expw=626&q=imgende+de+un+cielo+lluvioso+jpg&FORM=IRPRST&ck=A599C744BE7D4EE59E26DB5F7FDBD0AE&selectedIndex=18&itb=0"
    URL_TORMENTA = "https://www.bing.com/images/search?view=detailV2&ccid=cs28hoab&id=434BF60EEDA588F6A999856D5C35733F97CD6694&thid=OIP.cs28hoabBX5ifFz_wNUmYQHaE7&mediaurl=https%3a%2f%2fcdn.pixabay.com%2fphoto%2f2023%2f03%2f29%2f21%2f25%2fthunderstorm-7886349_1280.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.72cdbc86869b057e627c5cffc0d52661%3frik%3dlGbNlz9zNVxthQ%26pid%3dImgRaw%26r%3d0&exph=853&expw=1280&q=imgende+de+un+cielo+con+tormenta++jpg&FORM=IRPRST&ck=944165C86574EC632BBC904AD06A558A&selectedIndex=0&itb=0"
    URL_DEFAULT = "https://th.bing.com/th/id/OIP.Jj-8evhY4Ey7tcQAtJAcBwAAAA?w=214&h=180&c=7&r=0&o=5&cb=12&pid=1.7"

    # Lógica de if/elif
    if wmo_code in [0, 1]:
        descripcion = "Despejado / Mayormente Despejado"
        url_imagen_clima = URL_SOL
    elif wmo_code in [2]:
        descripcion = "Parcialmente Nublado"
        url_imagen_clima = URL_SOL  # Usamos sol/nube
    elif wmo_code in [3]:
        descripcion = "Nublado"
        url_imagen_clima = URL_NUBES
    elif wmo_code in [45, 48]:
        descripcion = "Niebla"
        url_imagen_clima = URL_NUBES  # Usamos la de nubes para niebla
    elif wmo_code in [51, 61, 63, 80]:
        descripcion = "Lluvia o Llovizna"
        url_imagen_clima = URL_LLUVIA
    elif wmo_code in [95]:
        descripcion = "Tormenta Eléctrica"
        url_imagen_clima = URL_TORMENTA
    elif wmo_code in [71, 73, 75, 77]:
        descripcion = "Nieve"
        url_imagen_clima = URL_LLUVIA  # Usamos la de lluvia/nieve
    else:
        descripcion = "Condición Desconocida"
        url_imagen_clima = URL_DEFAULT

    # 3. ACTUALIZAR LA ETIQUETA DEL CLIMA
    etiqueta3.configure(text=f"Clima: {descripcion}\nTemperatura: {temperatura}°C\nViento: {viento} km/h", font=fontm)

    # 4. LLAMAR A LA FUNCIÓN PARA CAMBIAR LA IMAGEN
    cargar_imagen_clima(url_imagen_clima)

    app.after(60000, obtenerClima)  # actualiza cada 60 segundos
# -----------------------------------------------------------------------------
# Función para mostrar un consejo
def consejo():
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
# INICIALIZACIÓN DE LA IMAGEN
# -----------------------------------------------------------------------------

# Inicializamos la etiqueta de imagen con un texto placeholder.
etiqueta_imagen = CTkLabel(app, text="Cargando clima...", font=fontm, fg_color="gray")
etiqueta_imagen.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

# Se define la variable global para el tamaño de la imagen.
medida = (450, 250)

# -----------------------------------------------------------------------------
# INICIO DE FUNCIONES CÍCLICAS Y MAINLOOP
# -----------------------------------------------------------------------------
actualizar_reloj()
obtenerClima()  # Esta función inicializará el clima y la imagen.
app.mainloop()