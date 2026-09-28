

import math

from sistema_transporte.base_conocimiento import (
    ESTACIONES,
    LINEAS,
    PENALIZACION_TRANSBORDO_MIN,
)


def distancia_km(estacion_a, estacion_b):
    """Distancia en línea recta entre dos estaciones, según sus coordenadas."""
    xa, ya = ESTACIONES[estacion_a]
    xb, yb = ESTACIONES[estacion_b]
    return math.dist((xa, ya), (xb, yb))


def tiempo_tramo_min(estacion_a, estacion_b, velocidad_kmh):
    """Tiempo de viaje (minutos) entre dos estaciones consecutivas de una línea."""
    distancia = distancia_km(estacion_a, estacion_b)
    horas = distancia / velocidad_kmh
    return round(horas * 60, 1)


def generar_hechos_tramos(trazar=False):
    """
    Regla 1: deriva los tramos (conexiones directas) entre estaciones
    consecutivas de cada línea, junto con su tiempo de viaje.

    Devuelve una lista de hechos derivados:
        ("tramo", estacion_a, estacion_b, nombre_linea, tiempo_min)
    """
    tramos = []
    for nombre_linea, datos in LINEAS.items():
        estaciones = datos["estaciones"]
        velocidad = datos["velocidad_kmh"]
        for i in range(len(estaciones) - 1):
            a, b = estaciones[i], estaciones[i + 1]
            tiempo = tiempo_tramo_min(a, b, velocidad)
            tramos.append(("tramo", a, b, nombre_linea, tiempo))
            if trazar:
                print(
                    f"  Regla 1 -> SI '{a}' y '{b}' son consecutivas en "
                    f"{nombre_linea} ENTONCES tramo transitable en {tiempo} min"
                )
    return tramos


def calcular_estaciones_transferencia(trazar=False):
    """
    Regla 2: deriva qué estaciones son de transbordo, es decir, en cuáles
    líneas coincide una misma estación.

    Devuelve un diccionario: {nombre_estacion: {linea_1, linea_2, ...}}
    Solo se incluyen estaciones que pertenecen a 2 o más líneas.
    """
    lineas_por_estacion = {}
    for nombre_linea, datos in LINEAS.items():
        for estacion in datos["estaciones"]:
            lineas_por_estacion.setdefault(estacion, set()).add(nombre_linea)

    transferencias = {
        estacion: lineas
        for estacion, lineas in lineas_por_estacion.items()
        if len(lineas) > 1
    }

    if trazar:
        for estacion, lineas in transferencias.items():
            lineas_txt = ", ".join(sorted(lineas))
            print(
                f"  Regla 2 -> SI '{estacion}' pertenece a [{lineas_txt}] "
                f"ENTONCES '{estacion}' es estacion de transbordo"
            )
    return transferencias


def construir_grafo(trazar=False):
    """
    Construye el grafo de estados sobre el que se hace la búsqueda.

    Cada nodo del grafo es una tupla (estacion, linea): "estar parado en
    esa estación, habiendo llegado por esa línea". Las aristas son de dos
    tipos:

    - "avanzar": moverse a la estación siguiente/anterior de la misma línea
                (Regla 1).
    - "transbordo": cambiar de línea sin moverse de estación (Regla 3),
                solo permitido si la estación es de transferencia entre
                ambas líneas (Regla 2).

    Devuelve: (grafo, transferencias)
        grafo: {(estacion, linea): [(estacion_destino, linea_destino, costo, tipo)]}
        transferencias: resultado de calcular_estaciones_transferencia()
    """
    if trazar:
        print("Aplicando Regla 1 (tramos entre estaciones consecutivas):")
    tramos = generar_hechos_tramos(trazar=trazar)

    if trazar:
        print("\nAplicando Regla 2 (deteccion de estaciones de transbordo):")
    transferencias = calcular_estaciones_transferencia(trazar=trazar)

    grafo = {}

    def agregar_arista(origen, destino, costo, tipo):
        grafo.setdefault(origen, []).append((destino[0], destino[1], costo, tipo))

    # Regla 1 aplicada al grafo: cada tramo genera una arista en ambos sentidos.
    for _, a, b, linea, tiempo in tramos:
        agregar_arista((a, linea), (b, linea), tiempo, "avanzar")
        agregar_arista((b, linea), (a, linea), tiempo, "avanzar")

    # Regla 3 aplicada al grafo: en cada estación de transbordo se puede
    # cambiar entre cualquier par de líneas que pasen por ella.
    if trazar:
        print("\nAplicando Regla 3 (conexiones de transbordo entre lineas):")
    for estacion, lineas in transferencias.items():
        lineas = sorted(lineas)
        for i, linea_origen in enumerate(lineas):
            for linea_destino in lineas:
                if linea_origen == linea_destino:
                    continue
                agregar_arista(
                    (estacion, linea_origen),
                    (estacion, linea_destino),
                    PENALIZACION_TRANSBORDO_MIN,
                    "transbordo",
                )
                if trazar:
                    print(
                        f"  Regla 3 -> SI '{estacion}' es transbordo entre "
                        f"{linea_origen} y {linea_destino} ENTONCES se puede "
                        f"cambiar de linea pagando {PENALIZACION_TRANSBORDO_MIN} min"
                    )

    return grafo, transferencias


def lineas_de_estacion(nombre_estacion):
    """Devuelve la lista de líneas que pasan por una estación dada."""
    return [
        nombre_linea
        for nombre_linea, datos in LINEAS.items()
        if nombre_estacion in datos["estaciones"]
    ]
