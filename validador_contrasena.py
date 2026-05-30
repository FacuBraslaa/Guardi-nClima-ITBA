import re

# Los criterios que tiene que cumplir la contraseña.
# Cada uno tiene un nombre interno, una función que lo evalúa, y el mensaje que le mostramos al usuario.
# Para que sea válida hay que cumplir al menos 3 de estos 5.
CRITERIOS = [
    ("longitud",    lambda p: len(p) >= 8,              "al menos 8 caracteres"),
    ("mayuscula",   lambda p: bool(re.search(r"[A-Z]", p)), "al menos una mayúscula"),
    ("minuscula",   lambda p: bool(re.search(r"[a-z]", p)), "al menos una minúscula"),
    ("numero",      lambda p: bool(re.search(r"\d", p)),    "al menos un número"),
    ("especial",    lambda p: bool(re.search(r"[!@#$%^&*(),.?\":{}|<>_\-]", p)), "al menos un carácter especial"),
]

# Mínimo de criterios que tiene que cumplir la contraseña para que la aceptemos
MIN_CRITERIOS = 3


def evaluar(contrasena: str) -> dict:
    # Corro cada criterio y guardo si pasó o no
    resultados = {}
    for nombre, fn, _ in CRITERIOS:
        resultados[nombre] = fn(contrasena)
    return resultados


def es_valida(contrasena: str) -> tuple[bool, list[str]]:
    resultados = evaluar(contrasena)
    # Me quedo con los criterios que NO se cumplieron para después mostrárselos al usuario
    fallidos = [desc for (nombre, _, desc), ok in zip(CRITERIOS, resultados.values()) if not ok]
    cumplidos = len(CRITERIOS) - len(fallidos)
    valida = cumplidos >= MIN_CRITERIOS
    return valida, fallidos


def sugerencias(fallidos: list[str]) -> str:
    # Si no faltó nada, no hay nada que sugerir
    if not fallidos:
        return ""
    lineas = ["Para fortalecer tu contraseña, agregá:"]
    for desc in fallidos:
        lineas.append(f"  • {desc}")
    return "\n".join(lineas)


def validar_con_feedback(contrasena: str) -> bool:
    # Esta es la función que usan los demás módulos.
    # Valida y si falla le dice al usuario exactamente qué le falta.
    valida, fallidos = es_valida(contrasena)
    if not valida:
        print("\n[!] Contraseña débil. No cumple el mínimo de 3 criterios de seguridad.")
        if fallidos:
            print(sugerencias(fallidos))
    return valida
