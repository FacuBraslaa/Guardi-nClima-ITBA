import csv
import hashlib
import os
from validador_contrasena import validar_con_feedback

_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_USUARIOS = os.path.join(_DIR, "usuarios_simulados.csv")

# tres columnas: usuario, salt y el hash de la contraseña (nunca guardamos la contraseña real)
CAMPOS = ["usuario", "salt", "contrasena"]


def _hashear(contrasena: str, salt: bytes) -> str:
    # hasheamos la contraseña con PBKDF2 con SHA-256, 200k iteraciones y salt aleatorio por usuario
    return hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), salt, 200_000).hex()


def _inicializar_csv():
    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=CAMPOS).writeheader()


def _leer_usuarios() -> list[dict]:
    _inicializar_csv()
    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _guardar_usuario(usuario: str, contrasena: str):
    _inicializar_csv()
    # generamos un salt único para este usuario antes de hashear
    salt = os.urandom(16)
    hash_contrasena = _hashear(contrasena, salt)
    with open(ARCHIVO_USUARIOS, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=CAMPOS).writerow({
            "usuario": usuario,
            "salt": salt.hex(),
            "contrasena": hash_contrasena,
        })


def _existe_usuario(nombre: str) -> bool:
    return any(u["usuario"] == nombre for u in _leer_usuarios())


def login() -> str | None:
    print("\n--- Iniciar Sesión ---")
    usuario = input("Usuario: ").strip()

    while True:
        contrasena = input("Contraseña: ").strip()

        for u in _leer_usuarios():
            if u["usuario"] == usuario:
                # reconstruimos el hash con el salt guardado y comparamos
                salt = bytes.fromhex(u["salt"])
                if _hashear(contrasena, salt) == u["contrasena"]:
                    print(f"\n[✓] Bienvenido, {usuario}!")
                    return usuario

        print("\n[!] Contraseña incorrecta.")
        reintentar = input("¿Querés intentar de nuevo? (s/n): ").strip().lower()
        if reintentar != "s":
            print("[i] Si no tenés cuenta, elegí la opción 2 para registrarte.")
            input("\nPresioná Enter para volver al menú...")
            return None


def registrar() -> str | None:
    print("\n--- Registro de Usuario ---")
    usuario = input("Elegí un nombre de usuario: ").strip()

    if not usuario:
        print("[!] El nombre de usuario no puede estar vacío.")
        input("\nPresioná Enter para volver al menú...")
        return None

    if _existe_usuario(usuario):
        print("[!] Ese nombre de usuario ya está en uso.")
        input("\nPresioná Enter para volver al menú...")
        return None

    # mostramos los requisitos antes de pedir la contraseña
    print("\nRequisitos de contraseña (debe cumplir al menos 3 de 5):")
    print("  • Mínimo 8 caracteres")
    print("  • Al menos una mayúscula")
    print("  • Al menos una minúscula")
    print("  • Al menos un número")
    print("  • Al menos un carácter especial (!@#$%&*...)")

    while True:
        contrasena = input("\nElegí una contraseña: ").strip()
        if validar_con_feedback(contrasena):
            break
        reintentar = input("¿Querés intentar con otra contraseña? (s/n): ").strip().lower()
        if reintentar != "s":
            print("[i] Registro cancelado.")
            input("\nPresioná Enter para volver al menú...")
            return None

    _guardar_usuario(usuario, contrasena)
    print(f"\n[✓] Usuario '{usuario}' registrado exitosamente. Iniciando sesión...")
    return usuario
