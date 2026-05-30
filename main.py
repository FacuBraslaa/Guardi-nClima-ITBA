import os
from dotenv import load_dotenv
from autenticacion import login, registrar
from clima import obtener_clima, mostrar_clima
from historial import guardar_consulta, historial_usuario, mostrar_historial
from estadisticas import mostrar_estadisticas
from consejo_ia import obtener_consejo, mostrar_consejo

# Cargamos las API keys desde el archivo .env para no tener que escribirlas cada vez
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def menu_acceso() -> str | None:
    # Este es el primer menú que ve el usuario. Hasta que no inicie sesión o se registre, no sale de acá.
    while True:
        print("\n╔══════════════════════════════╗")
        print("║       GuardiánClima ITBA     ║")
        print("╠══════════════════════════════╣")
        print("║  1. Iniciar sesión           ║")
        print("║  2. Registrarse              ║")
        print("║  3. Salir                    ║")
        print("╚══════════════════════════════╝")
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            usuario = login()
            if usuario:
                return usuario  # Login exitoso, pasamos al menú principal
        elif opcion == "2":
            usuario = registrar()
            if usuario:
                return usuario  # Se registró y quedó logueado automáticamente
        elif opcion == "3":
            print("\nHasta luego!\n")
            return None
        else:
            print("[!] Opción inválida.")


def menu_principal(usuario: str):
    # Una vez logueado, el usuario se queda en este menú hasta que decida cerrar sesión
    while True:
        nombre_display = usuario[:19] + ".." if len(usuario) > 21 else usuario
        print(f"\n╔══════════════════════════════════════╗")
        print(f"║   Bienvenido, {nombre_display:<22}║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║  1. Consultar clima de una ciudad    ║")
        print(f"║  2. Ver mi historial                 ║")
        print(f"║  3. Estadísticas globales            ║")
        print(f"║  4. Consejo de vestimenta (IA)       ║")
        print(f"║  5. Acerca de la aplicación          ║")
        print(f"║  6. Cerrar sesión                    ║")
        print(f"╚══════════════════════════════════════╝")
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            consultar_clima(usuario)
            input("\nPresioná Enter para continuar...")
        elif opcion == "2":
            registros = historial_usuario(usuario)
            mostrar_historial(registros)
            input("\nPresioná Enter para continuar...")
        elif opcion == "3":
            mostrar_estadisticas()
            input("\nPresioná Enter para continuar...")
        elif opcion == "4":
            consejo_ia_interactivo(usuario)
            input("\nPresioná Enter para continuar...")
        elif opcion == "5":
            mostrar_acerca()
        elif opcion == "6":
            print(f"\n[✓] Sesión cerrada. Hasta pronto, {usuario}!")
            break
        else:
            print("[!] Opción inválida.")


def consultar_clima(usuario: str):
    ciudad = input("\nIngresá el nombre de la ciudad: ").strip()
    if not ciudad:
        print("[!] El nombre de la ciudad no puede estar vacío.")
        return

    if not OPENWEATHER_API_KEY:
        print("[!] Falta configurar OPENWEATHER_API_KEY en el archivo .env")
        return

    datos = obtener_clima(ciudad, OPENWEATHER_API_KEY)
    if datos:
        mostrar_clima(datos)
        # Guardamos la consulta en el historial global para que aparezca en estadísticas
        guardar_consulta(usuario, datos)


def consejo_ia_interactivo(usuario: str):
    # Para dar un consejo necesitamos datos de clima, así que los sacamos del historial
    registros = historial_usuario(usuario)
    if not registros:
        print("\n[i] Primero consultá el clima de alguna ciudad (opción 1).")
        return

    # Le mostramos las ciudades que ya consultó para que elija
    print("\nCiudades en tu historial:")
    ciudades_unicas = list(dict.fromkeys(r["ciudad"] for r in registros))
    for i, c in enumerate(ciudades_unicas, 1):
        print(f"  {i}. {c}")

    eleccion = input("Elegí el número de ciudad (o Enter para la última): ").strip()

    if eleccion == "":
        # Si no elige, usamos los datos de la última consulta
        ultimo = registros[-1]
    else:
        try:
            idx = int(eleccion) - 1
            ciudad_elegida = ciudades_unicas[idx]
            # Tomamos la consulta más reciente de esa ciudad
            ultimo = next(r for r in reversed(registros) if r["ciudad"] == ciudad_elegida)
        except (ValueError, IndexError):
            print("[!] Selección inválida.")
            return

    # Armamos el diccionario con los datos que necesita la función de IA
    datos_clima = {
        "ciudad": ultimo["ciudad"],
        "pais": ultimo["pais"],
        "temperatura": ultimo["temperatura"],
        "sensacion": ultimo["sensacion"],
        "humedad": ultimo["humedad"],
        "viento": ultimo["viento"],
        "descripcion": ultimo["descripcion"],
    }

    if not GEMINI_API_KEY:
        print("[!] Falta configurar GEMINI_API_KEY en el archivo .env")
        return

    print("\n[...] Consultando a la IA...")
    consejo = obtener_consejo(datos_clima, GEMINI_API_KEY)
    if consejo:
        mostrar_consejo(consejo)


def mostrar_acerca():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                   ACERCA DE GUARDIÁNCLIMA                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  GuardiánClima ITBA es una aplicación de consola que        ║
║  permite consultar el clima en tiempo real, registrar un    ║
║  historial personal de consultas y recibir consejos de      ║
║  vestimenta generados por Inteligencia Artificial.          ║
║                                                              ║
║  TECNOLOGÍAS UTILIZADAS:                                     ║
║  • Python 3.x           — lenguaje principal                ║
║  • OpenWeatherMap API   — datos meteorológicos en tiempo    ║
║                           real                              ║
║  • Google Gemini API    — consejos de IA generativa         ║
║  • CSV                  — almacenamiento de usuarios e      ║
║                           historial                         ║
║                                                              ║
║  SEGURIDAD DE CONTRASEÑAS:                                   ║
║  Las contraseñas se almacenan con hashing PBKDF2-SHA256     ║
║  y salt aleatorio por usuario. Esto garantiza que aunque    ║
║  el CSV sea comprometido, las contraseñas originales no     ║
║  puedan ser recuperadas.                                     ║
║                                                              ║
║  VALIDACIÓN DE CONTRASEÑAS:                                  ║
║  El sistema exige que la contraseña cumpla al menos 3 de    ║
║  los siguientes criterios: longitud ≥ 8, mayúscula,         ║
║  minúscula, número y carácter especial.                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    input("Presioná Enter para volver al menú...")


# Punto de entrada de la aplicación
if __name__ == "__main__":
    usuario_activo = menu_acceso()
    if usuario_activo:
        menu_principal(usuario_activo)
