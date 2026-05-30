from google import genai


def obtener_consejo(datos_clima: dict, api_key: str) -> str | None:
    try:
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

        respuesta = cliente.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return respuesta.text.strip()

    except Exception as e:
        print(f"[!] Error al consultar la IA: {e}")
        return None


def mostrar_consejo(consejo: str):
    print(f"\n{'='*45}")
    print("       CONSEJO DE VESTIMENTA (IA)")
    print(f"{'='*45}")
    print(f"\n{consejo}\n")
    print(f"{'='*45}")
