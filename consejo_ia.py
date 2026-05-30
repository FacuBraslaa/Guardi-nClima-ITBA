from google import genai

# probamos los modelos en orden, si uno tiene cuota agotada pasamos al siguiente
_MODELOS = ["gemini-2.5-flash", "gemini-2.0-flash-lite", "gemini-2.0-flash"]


def obtener_consejo(datos_clima: dict, api_key: str) -> str | None:
    cliente = genai.Client(api_key=api_key)

    prompt = (
        f"Sos un asistente de clima amigable que habla en español latinoamericano. "
        f"Basándote en las siguientes condiciones climáticas actuales, "
        f"dá un consejo breve y práctico sobre qué ropa usar hoy:\n\n"
        f"- Ciudad: {datos_clima['ciudad']}, {datos_clima['pais']}\n"
        f"- Condición: {datos_clima['descripcion']}\n"
        f"- Temperatura: {datos_clima['temperatura']}°C\n"
        f"- Sensación térmica: {datos_clima['sensacion']}°C\n"
        f"- Humedad: {datos_clima['humedad']}%\n"
        f"- Viento: {datos_clima['viento']} m/s\n\n"
        f"Respondé en 3 o 4 oraciones como máximo, de forma directa y útil."
    )

    for modelo in _MODELOS:
        try:
            respuesta = cliente.models.generate_content(model=modelo, contents=prompt)
            return respuesta.text.strip()
        except Exception as e:
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower():
                continue  # cuota agotada, probamos con el siguiente
            print(f"[!] Error al consultar la IA: {e}")
            return None

    print("[!] La API de Gemini alcanzó el límite de uso. Intentá de nuevo en unos minutos.")
    return None


def mostrar_consejo(consejo: str):
    print(f"\n{'='*45}")
    print("       CONSEJO DE VESTIMENTA (IA)")
    print(f"{'='*45}")
    print(f"\n{consejo}\n")
    print(f"{'='*45}")
