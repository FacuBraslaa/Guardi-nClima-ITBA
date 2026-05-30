import re


CRITERIOS = [
    ("longitud",    lambda p: len(p) >= 8,              "al menos 8 caracteres"),
    ("mayuscula",   lambda p: bool(re.search(r"[A-Z]", p)), "al menos una mayúscula"),
    ("minuscula",   lambda p: bool(re.search(r"[a-z]", p)), "al menos una minúscula"),
    ("numero",      lambda p: bool(re.search(r"\d", p)),    "al menos un número"),
    ("especial",    lambda p: bool(re.search(r"[!@#$%^&*(),.?\":{}|<>_\-]", p)), "al menos un carácter especial"),
]

MIN_CRITERIOS = 3


def evaluar(contrasena: str) -> dict:
    resultados = {}
    for nombre, fn, _ in CRITERIOS:
        resultados[nombre] = fn(contrasena)
    return resultados


def es_valida(contrasena: str) -> tuple[bool, list[str]]:
    resultados = evaluar(contrasena)
    fallidos = [desc for (nombre, _, desc), ok in zip(CRITERIOS, resultados.values()) if not ok]
    cumplidos = len(CRITERIOS) - len(fallidos)
    valida = cumplidos >= MIN_CRITERIOS
    return valida, fallidos


def sugerencias(fallidos: list[str]) -> str:
    if not fallidos:
        return ""
    lineas = ["Para fortalecer tu contraseña, agregá:"]
    for desc in fallidos:
        lineas.append(f"  • {desc}")
    return "\n".join(lineas)


def validar_con_feedback(contrasena: str) -> bool:
    valida, fallidos = es_valida(contrasena)
    if not valida:
        print("\n[!] Contraseña débil. No cumple el mínimo de 3 criterios de seguridad.")
        if fallidos:
            print(sugerencias(fallidos))
    return valida
