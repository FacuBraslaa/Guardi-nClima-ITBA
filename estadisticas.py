from collections import Counter
from historial import leer_historial


def calcular_estadisticas() -> dict | None:
    registros = leer_historial()

    if not registros:
        return None

    # Counter cuenta cuántas veces aparece cada ciudad, most_common(1) da la más frecuente
    ciudades = [r["ciudad"] for r in registros]
    ciudad_mas_consultada, cantidad = Counter(ciudades).most_common(1)[0]

    temperaturas = []
    for r in registros:
        try:
            temperaturas.append(float(r["temperatura"]))
        except ValueError:
            pass  # por si hay alguna fila rara en el CSV

    promedio_temp = round(sum(temperaturas) / len(temperaturas), 1) if temperaturas else 0.0
    usuarios_unicos = len(set(r["usuario"] for r in registros))

    return {
        "total_consultas": len(registros),
        "ciudad_mas_consultada": ciudad_mas_consultada,
        "veces_consultada": cantidad,
        "promedio_temperatura": promedio_temp,
        "usuarios_unicos": usuarios_unicos,
    }


def mostrar_estadisticas():
    stats = calcular_estadisticas()

    if not stats:
        print("\n[i] No hay datos suficientes para mostrar estadísticas.")
        return

    print(f"\n{'='*45}")
    print("       ESTADÍSTICAS GLOBALES")
    print(f"{'='*45}")
    print(f"  Total de consultas       : {stats['total_consultas']}")
    print(f"  Usuarios únicos          : {stats['usuarios_unicos']}")
    print(f"  Ciudad más consultada    : {stats['ciudad_mas_consultada']} ({stats['veces_consultada']} veces)")
    print(f"  Temperatura promedio     : {round(stats['promedio_temperatura'])}°")
    print(f"{'='*45}")
