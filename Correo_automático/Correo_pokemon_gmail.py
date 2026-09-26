import pandas as pd
import requests
import smtplib
from email.message import EmailMessage
from datetime import datetime
import random


# ============================================================
# DESCRIPCIÓN DEL CÓDIGO
# ------------------------------------------------------------
# Este script realiza tres tareas automáticamente cada vez que
# se ejecuta:
#
#   1. OBTENER DATOS: Llama a la API pública de Pokémon
#      (pokeapi.co) y obtiene la información de un Pokémon
#      elegido al azar (entre los 1025 disponibles): nombre,
#      ID, altura, peso y tipo(s).
#
#   2. GUARDAR EN EXCEL: Almacena esa información en un archivo
#      Excel llamado "pokemon_of_the_day.xlsx".
#
#   3. ENVIAR POR CORREO: Adjunta el Excel en un correo
#      electrónico y lo envía al destinatario configurado,
#      usando Gmail como servidor de correo (SMTP).
#
# Para usarlo, rellena las tres variables de configuración:
#   - CORREO_EMISOR      → tu cuenta de Gmail
#   - CONTRASEÑA_CORREO  → contraseña de aplicación de Gmail
#   - CORREO_RECEPTOR    → correo del destinatario
# ============================================================


# --- CONFIGURACIÓN ---
CORREO_EMISOR = "correo_prueba@gmail.com"
CONTRASEÑA_CORREO = "*******"  # Usa una contraseña de aplicación, no la de tu cuenta
CORREO_RECEPTOR = "correo_prueba@gmail.com"


def obtener_datos_de_la_api():
    """Obtiene los datos de un Pokémon aleatorio desde la API de PokeAPI."""
    id_pokemon = random.randint(1, 1025)
    url = f"https://pokeapi.co/api/v2/pokemon/{id_pokemon}"

    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return {
            "Fecha": datetime.now().strftime("%Y-%m-%d"),
            "Nombre": datos['name'].capitalize(),
            "ID": datos['id'],
            "Altura": datos['height'],
            "Peso": datos['weight'],
            "Tipo": ", ".join([t['type']['name'] for t in datos['types']])
        }
    else:
        print("Error al obtener datos de la PokeAPI")
        return None


def guardar_datos_en_excel(datos_pokemon):
    """Guarda el diccionario de datos del Pokémon en un archivo Excel."""
    nombre_archivo = "pokemon_del_dia.xlsx"
    tabla = pd.DataFrame([datos_pokemon])
    tabla.to_excel(nombre_archivo, index=False)
    return nombre_archivo


def enviar_correo(ruta_adjunto):
    """Envía un correo electrónico con el archivo Excel adjunto."""
    mensaje = EmailMessage()
    mensaje['Subject'] = f"Tu Pokémon del día: {datetime.now().strftime('%Y-%m-%d')}"
    mensaje['From'] = CORREO_EMISOR
    mensaje['To'] = CORREO_RECEPTOR
    mensaje.set_content("¡Hazte con todos! Aquí tienes los datos del Pokémon del día en el archivo adjunto.")

    # Leer el archivo Excel y adjuntarlo al correo
    with open(ruta_adjunto, 'rb') as archivo:
        contenido_archivo = archivo.read()
        mensaje.add_attachment(
            contenido_archivo,
            maintype='application',
            subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=ruta_adjunto
        )

    # Enviar el correo mediante el servidor SMTP de Gmail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor_smtp:
        servidor_smtp.login(CORREO_EMISOR, CONTRASEÑA_CORREO)
        servidor_smtp.send_message(mensaje)
    print("¡Correo enviado correctamente!")


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    info_pokemon = obtener_datos_de_la_api()
    if info_pokemon:
        ruta_archivo = guardar_datos_en_excel(info_pokemon)
        enviar_correo(ruta_archivo)