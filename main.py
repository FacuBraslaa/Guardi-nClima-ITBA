import os
from dotenv import load_dotenv
from autenticacion import login, registrar
from clima import obtener_clima, mostrar_clima
from historial import guardar_consulta, historial_usuario, mostrar_historial
from estadisticas import mostrar_estadisticas
from consejo_ia import obtener_consejo, mostrar_consejo

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def menu_acceso() -> str | None:
    while True:
        print("\n╔══════════════════════════════╗")
        print("║       GuardiánClima ITBA     ║")
        print("╠══════════════════════════════╣")
        print("║  1. Iniciar sesión           ║")
        print("║  2. Registrarse              ║")
        print("║  3. Acerca de la aplicación  ║")
        print("║  4. Salir                    ║")
        print("╚══════════════════════════════╝")
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            usuario = login()
            if usuario:
                return usuario
        elif opcion == "2":
            usuario = registrar()
            if usuario:
                return usuario
        elif opcion == "3":
            mostrar_acerca()
        elif opcion == "4":
            print("\nHasta luego!\n")
            return None
        else:
            print("[!] Opción inválida.")


def menu_principal(usuario: str):
    while True:
        print(f"\n╔══════════════════════════════════════╗")
        print(f"║   Bienvenido, {usuario:<22}║")
        print(f"╠══════════════════════════════════════╣")
        print(f"║  1. Consultar clima de una ciudad    ║")
        print(f"║  2. Ver mi historial                 ║")
        print(f"║  3. Estadísticas globales            ║")
        print(f"║  4. Consejo de vestimenta (IA)       ║")
        print(f"║  5. Cerrar sesión                    ║")
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
        print("[!] Falta configurar OPENWEATHER_API_KEY en las variables de entorno.")
        return

    datos = obtener_clima(ciudad, OPENWEATHER_API_KEY)
    if datos:
        mostrar_clima(datos)
        guardar_consulta(usuario, datos)


def consejo_ia_interactivo(usuario: str):
    registros = historial_usuario(usuario)
    if not registros:
        print("\n[i] Primero consultá el clima de alguna ciudad (opción 1).")
        return

    print("\nCiudades en tu historial:")
    ciudades_unicas = list(dict.fromkeys(r["ciudad"] for r in registros))
    for i, c in enumerate(ciudades_unicas, 1):
        print(f"  {i}. {c}")

    eleccion = input("Elegí el número de ciudad (o Enter para la última): ").strip()

    if eleccion == "":
        ultimo = registros[-1]
    else:
        try:
            idx = int(eleccion) - 1
            ciudad_elegida = ciudades_unicas[idx]
            ultimo = next(r for r in reversed(registros) if r["ciudad"] == ciudad_elegida)
        except (ValueError, IndexError):
            print("[!] Selección inválida.")
            return

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
        print("[!] Falta configurar GEMINI_API_KEY en las variables de entorno.")
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
║  NOTA DE SEGURIDAD:                                          ║
║  Las contraseñas se almacenan en texto plano en un          ║
║  archivo CSV con fines educativos. En un sistema real,      ║
║  deberían aplicarse técnicas de hashing (ej. bcrypt o       ║
║  SHA-256 con salt) para proteger las credenciales.          ║
║                                                              ║
║  VALIDACIÓN DE CONTRASEÑAS:                                  ║
║  El sistema exige que la contraseña cumpla al menos 3 de    ║
║  los siguientes criterios: longitud ≥ 8, mayúscula,         ║
║  minúscula, número y carácter especial.                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    input("Presioná Enter para volver al menú...")


if __name__ == "__main__":
    usuario_activo = menu_acceso()
    if usuario_activo:
        menu_principal(usuario_activo)
