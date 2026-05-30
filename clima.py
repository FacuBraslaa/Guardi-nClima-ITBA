import requests

# Endpoint de la API de OpenWeatherMap para el clima actual
API_URL = "https://api.openweathermap.org/data/2.5/weather"


def obtener_clima(ciudad: str, api_key: str) -> dict | None:
    params = {
        "q": ciudad,
        "appid": api_key,
        "units": "metric",  # Para que la temperatura nos llegue en Celsius
        "lang": "es",       # Descripción del clima en español
    }
    try:
        respuesta = requests.get(API_URL, params=params, timeout=10)

        # Controlamos los errores más comunes antes de procesar la respuesta
        if respuesta.status_code == 401:
            print("[!] API key inválida. Verificá tu clave de OpenWeatherMap.")
            return None
        if respuesta.status_code == 404:
            print(f"[!] Ciudad '{ciudad}' no encontrada.")
            return None

        respuesta.raise_for_status()
        datos = respuesta.json()

        # Extraemos solo lo que nos interesa mostrar
        return {
            "ciudad": datos["name"],
            "pais": datos["sys"]["country"],
            "temperatura": datos["main"]["temp"],
            "sensacion": datos["main"]["feels_like"],
            "humedad": datos["main"]["humidity"],
            "viento": datos["wind"]["speed"],
            "descripcion": datos["weather"][0]["description"].capitalize(),
        }

    except requests.exceptions.ConnectionError:
        print("[!] Sin conexión a internet. Verificá tu red.")
        return None
    except requests.exceptions.Timeout:
        print("[!] La solicitud tardó demasiado. Intentá de nuevo.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[!] Error al consultar el clima: {e}")
        return None


def mostrar_clima(datos: dict):
    # Mostramos los datos del clima de forma ordenada
    print(f"\n{'='*40}")
    print(f"  {datos['ciudad']}, {datos['pais']}")
    print(f"{'='*40}")
    print(f"  Condición   : {datos['descripcion']}")
    print(f"  Temperatura : {round(datos['temperatura'])}°")
    print(f"  Sensación   : {round(datos['sensacion'])}°")
    print(f"  Humedad     : {datos['humedad']}%")
    print(f"  Viento      : {datos['viento']} m/s")
    print(f"{'='*40}")
