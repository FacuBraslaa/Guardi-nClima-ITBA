import csv
import os
from validador_contrasena import validar_con_feedback

ARCHIVO_USUARIOS = "usuarios_simulados.csv"
CAMPOS = ["usuario", "contrasena"]


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
    with open(ARCHIVO_USUARIOS, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=CAMPOS).writerow({"usuario": usuario, "contrasena": contrasena})


def _existe_usuario(nombre: str) -> bool:
    return any(u["usuario"] == nombre for u in _leer_usuarios())


def login() -> str | None:
    print("\n--- Iniciar Sesión ---")
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()

    for u in _leer_usuarios():
        if u["usuario"] == usuario and u["contrasena"] == contrasena:
            print(f"\n[✓] Bienvenido, {usuario}!")
            return usuario

    print("\n[!] Usuario o contraseña incorrectos.")
    return None


def registrar() -> str | None:
    print("\n--- Registro de Usuario ---")
    usuario = input("Elegí un nombre de usuario: ").strip()

    if not usuario:
        print("[!] El nombre de usuario no puede estar vacío.")
        return None

    if _existe_usuario(usuario):
        print("[!] Ese nombre de usuario ya está en uso.")
        return None

    contrasena = input("Elegí una contraseña: ").strip()

    if not validar_con_feedback(contrasena):
        return None

    _guardar_usuario(usuario, contrasena)
    print(f"\n[✓] Usuario '{usuario}' registrado exitosamente. Iniciando sesión...")
    return usuario
