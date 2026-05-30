import csv
import os
from datetime import datetime

_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_HISTORIAL = os.path.join(_DIR, "historial_global.csv")

# Todas las columnas que guardamos por cada consulta
CAMPOS = ["fecha", "hora", "usuario", "ciudad", "pais", "temperatura", "sensacion", "humedad", "viento", "descripcion"]


def _inicializar_csv():
    # Si es la primera vez que se corre la app, creamos el archivo con los encabezados
    if not os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=CAMPOS).writeheader()


def guardar_consulta(usuario: str, datos_clima: dict):
    _inicializar_csv()
    ahora = datetime.now()
    # Armamos la fila con todos los datos del clima más el usuario y la fecha/hora actual
    fila = {
        "fecha": ahora.strftime("%Y-%m-%d"),
        "hora": ahora.strftime("%H:%M:%S"),
        "usuario": usuario,
        "ciudad": datos_clima["ciudad"],
        "pais": datos_clima["pais"],
        "temperatura": datos_clima["temperatura"],
        "sensacion": datos_clima["sensacion"],
        "humedad": datos_clima["humedad"],
        "viento": datos_clima["viento"],
        "descripcion": datos_clima["descripcion"],
    }
    with open(ARCHIVO_HISTORIAL, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=CAMPOS).writerow(fila)


def leer_historial() -> list[dict]:
    # Devuelve todas las consultas de todos los usuarios (el historial global)
    _inicializar_csv()
    with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def historial_usuario(usuario: str) -> list[dict]:
    # Filtramos el historial global para quedarnos solo con las consultas de este usuario
    return [r for r in leer_historial() if r["usuario"] == usuario]


def mostrar_historial(registros: list[dict]):
    if not registros:
        print("\n[i] No hay consultas registradas.")
        return

    print(f"\n{'='*60}")
    print(f"  {'FECHA':<12} {'HORA':<10} {'CIUDAD':<20} {'TEMP':>6}")
    print(f"{'='*60}")
    for r in registros:
        # Si el nombre de la ciudad es muy largo, lo cortamos para que no rompa la tabla
        ciudad = r['ciudad'][:18] + ".." if len(r['ciudad']) > 20 else r['ciudad']
        temp = f"{round(float(r['temperatura']))}°"
        print(f"  {r['fecha']:<12} {r['hora']:<10} {ciudad:<20} {temp:>5}")
    print(f"{'='*60}")
