import pandas as pd
import requests
import msal
import base64
from datetime import datetime
import random
import os
from dotenv import load_dotenv


# ============================================================
# DESCRIPCIÓN DEL CÓDIGO (VERSIÓN SEGURA PARA GITHUB)
# ============================================================
# Este script es SEGURO para subir a GitHub porque:
# 1. Lee las credenciales desde un archivo .env
# 2. El archivo .env está en .gitignore (no se sube)
# 3. Las credenciales nunca aparecen en el código
#
# Funcionalidad:
#   - Obtiene un Pokémon aleatorio de PokeAPI
#   - Guarda los datos en un Excel
#   - Envía el Excel por correo usando OAuth2 en Outlook
# ============================================================


# Cargar variables de entorno desde .env
load_dotenv()

# --- CONFIGURACIÓN DESDE VARIABLES DE ENTORNO ---
TENANT_ID = os.getenv("TENANT_ID", "*****")
CLIENT_ID = os.getenv("CLIENT_ID", "*****")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "*****")
CORREO_EMISOR = os.getenv("CORREO_EMISOR", "tu_correo@outlook.com")
CORREO_RECEPTOR = os.getenv("CORREO_RECEPTOR", "destinatario@outlook.com")

# Autoridad de autenticación
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
# Scope para enviar correos
SCOPES = ["https://graph.microsoft.com/.default"]


def validar_configuracion():
    """Valida que las credenciales estén configuradas correctamente."""
    if TENANT_ID == "*****" or CLIENT_SECRET == "*****":
        print(" Error: Credenciales no configuradas.")
        print("\nPasos para configurar:")
        print("1. Crea un archivo llamado '.env' en el directorio del script")
        print("2. Rellena con tus valores:")
        print("   TENANT_ID=tu_tenant_id")
        print("   CLIENT_ID=tu_client_id")
        print("   CLIENT_SECRET=tu_client_secret")
        print("   CORREO_EMISOR=tu_correo@outlook.com")
        print("   CORREO_RECEPTOR=destinatario@outlook.com")
        print("\n3. Instala python-dotenv: pip install python-dotenv")
        return False
    return True


def obtener_token_de_acceso():
    """Obtiene un token de acceso usando MSAL con credenciales de cliente."""
    try:
        app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            client_credential=CLIENT_SECRET
        )

        resultado = app.acquire_token_for_client(scopes=SCOPES)

        if "access_token" in resultado:
            return resultado["access_token"]
        else:
            error = resultado.get('error_description', 'Desconocido')
            print(f" Error al obtener el token: {error}")
            return None
    except Exception as e:
        print(f" Error en autenticación: {e}")
        return None


def obtener_datos_de_la_api():
    """Obtiene los datos de un Pokémon aleatorio desde la API de PokeAPI."""
    id_pokemon = random.randint(1, 1025)
    url = f"https://pokeapi.co/api/v2/pokemon/{id_pokemon}"

    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            return {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Nombre": datos['name'].capitalize(),
                "ID": datos['id'],
                "Altura (dm)": datos['height'],
                "Peso (hg)": datos['weight'],
                "Tipo": ", ".join([t['type']['name'] for t in datos['types']])
            }
        else:
            print(f" Error en PokeAPI: código {respuesta.status_code}")
            return None
    except requests.exceptions.Timeout:
        print(" Timeout al conectar con PokeAPI")
        return None
    except Exception as e:
        print(f" Error al obtener datos: {e}")
        return None


def guardar_datos_en_excel(datos_pokemon):
    """Guarda el diccionario de datos del Pokémon en un archivo Excel."""
    nombre_archivo = "pokemon_del_dia.xlsx"
    try:
        tabla = pd.DataFrame([datos_pokemon])
        tabla.to_excel(nombre_archivo, index=False)
        return nombre_archivo
    except Exception as e:
        print(f" Error al guardar Excel: {e}")
        return None


def leer_archivo_como_base64(ruta_archivo):
    """Lee un archivo y lo convierte a base64 para adjuntarlo."""
    try:
        with open(ruta_archivo, 'rb') as archivo:
            contenido = archivo.read()
            return base64.b64encode(contenido).decode('utf-8')
    except Exception as e:
        print(f" Error al leer archivo: {e}")
        return None


def enviar_correo_outlook(token_acceso, ruta_adjunto):
    """Envía un correo mediante Microsoft Graph API con el archivo adjunto."""
    
    headers = {
        "Authorization": f"Bearer {token_acceso}",
        "Content-Type": "application/json"
    }

    # Preparar el contenido del archivo adjunto en base64
    contenido_base64 = leer_archivo_como_base64(ruta_adjunto)
    
    if not contenido_base64:
        return False

    # Construir el payload del correo
    payload = {
        "message": {
            "subject": f" Tu Pokémon del día: {datetime.now().strftime('%d/%m/%Y')}",
            "body": {
                "contentType": "HTML",
                "content": """
                <div style="font-family: Arial, sans-serif; color: #333;">
                    <h2>¡Hazte con todos! </h2>
                    <p>Aquí tienes los datos del Pokémon del día en el archivo adjunto.</p>
                    <p style="color: #666; font-size: 12px;">Este correo ha sido enviado automáticamente.</p>
                </div>
                """
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": CORREO_RECEPTOR
                    }
                }
            ],
            "attachments": [
                {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": ruta_adjunto,
                    "contentBytes": contenido_base64
                }
            ]
        },
        "saveToSentItems": True
    }

    # Endpoint de Microsoft Graph para enviar correos
    url = "https://graph.microsoft.com/v1.0/me/sendMail"

    try:
        respuesta = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if respuesta.status_code == 202:
            print(f" Correo enviado correctamente a {CORREO_RECEPTOR}")
            return True
        else:
            print(f" Error al enviar correo: {respuesta.status_code}")
            try:
                error_info = respuesta.json()
                print(f"   Detalles: {error_info.get('error', {}).get('message', 'Desconocido')}")
            except:
                print(f"   Respuesta: {respuesta.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print(" Timeout al enviar correo")
        return False
    except Exception as e:
        print(f" Error en conexión: {e}")
        return False


def limpiar_archivos(ruta_archivo):
    """Elimina el archivo Excel después de enviarlo (opcional)."""
    try:
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
            print(f"  Archivo temporal eliminado: {ruta_archivo}")
    except Exception as e:
        print(f"  No se pudo eliminar el archivo: {e}")


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print(" POKÉMON DAILY MAILER - OAuth2/MSAL")
    print("="*50 + "\n")
    
    # Validar configuración
    if not validar_configuracion():
        exit(1)
    
    # Paso 1: Obtener el token de acceso
    print("1️  Autenticando con Azure...")
    token = obtener_token_de_acceso()
    
    if not token:
        print("\n No se pudo obtener el token de acceso.")
        print("   Verifica que tus credenciales sean correctas en el archivo .env")
        exit(1)
    print(" Autenticación exitosa\n")
    
    # Paso 2: Obtener datos del Pokémon
    print("Obteniendo datos del Pokémon de PokeAPI...")
    info_pokemon = obtener_datos_de_la_api()
    
    if not info_pokemon:
        print("\n No se pudieron obtener los datos del Pokémon.")
        exit(1)
    
    print(f"Pokémon obtenido: {info_pokemon['Nombre']} (ID: {info_pokemon['ID']})\n")
    
    # Paso 3: Guardar en Excel
    print("Guardando datos en Excel...")
    ruta_archivo = guardar_datos_en_excel(info_pokemon)
    
    if not ruta_archivo:
        print("\n Error al guardar en Excel.")
        exit(1)
    print(f" Archivo guardado: {ruta_archivo}\n")
    
    # Paso 4: Enviar por correo
    print("Enviando correo por Outlook...")
    exito = enviar_correo_outlook(token, ruta_archivo)
    
    print("\n" + "="*50)
    if exito:
        print("¡PROCESO COMPLETADO EXITOSAMENTE!")
        # Opcional: eliminar archivo después de enviar
        # limpiar_archivos(ruta_archivo)
    else:
        print("   ERROR: No se pudo enviar el correo.")
        print("   El archivo Excel se encuentra en:", ruta_archivo)
        exit(1)
    print("="*50 + "\n")