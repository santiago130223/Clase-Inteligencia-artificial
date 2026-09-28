
import heapq

from sistema_transporte.base_conocimiento import ESTACIONES, VELOCIDAD_MAXIMA_KMH
from sistema_transporte.motor_reglas import construir_grafo, distancia_km, lineas_de_estacion


def heuristica(estacion, destino):
    distancia = distancia_km(estacion, destino)
    horas = distancia / VELOCIDAD_MAXIMA_KMH
    return horas * 60


def buscar_mejor_ruta(origen, destino, trazar=False):
    """
    Ejecuta A* sobre el grafo derivado por las reglas y devuelve la mejor ruta.

    Devuelve un diccionario con:
        "pasos": lista de (estacion, linea, tipo_movimiento, costo_acumulado)
        "tiempo_total": tiempo total estimado en minutos
    o None si no existe una ruta entre origen y destino.
    """
    if origen not in ESTACIONES:
        raise ValueError(f"La estacion de origen '{origen}' no existe en el sistema.")
    if destino not in ESTACIONES:
        raise ValueError(f"La estacion de destino '{destino}' no existe en el sistema.")

    grafo, _ = construir_grafo(trazar=trazar)

    # El viajero puede "abordar" cualquier linea que pase por la estacion de origen.
    estados_iniciales = [(estacion_linea, 0.0) for estacion_linea in [(origen, linea) for linea in lineas_de_estacion(origen)]]

    costo_acumulado = {estado: 0.0 for estado, _ in estados_iniciales}
    padre = {estado: None for estado, _ in estados_iniciales}
    tipo_movimiento = {estado: "inicio" for estado, _ in estados_iniciales}

    cola = []
    for estado, _ in estados_iniciales:
        prioridad = heuristica(estado[0], destino)
        heapq.heappush(cola, (prioridad, estado))

    visitados = set()

    while cola:
        _, estado_actual = heapq.heappop(cola)
        if estado_actual in visitados:
            continue
        visitados.add(estado_actual)

        estacion_actual, _ = estado_actual
        if estacion_actual == destino:
            return _reconstruir_resultado(estado_actual, padre, tipo_movimiento, costo_acumulado)

        for estacion_dest, linea_dest, costo, tipo in grafo.get(estado_actual, []):
            estado_vecino = (estacion_dest, linea_dest)
            nuevo_costo = costo_acumulado[estado_actual] + costo
            if estado_vecino not in costo_acumulado or nuevo_costo < costo_acumulado[estado_vecino]:
                costo_acumulado[estado_vecino] = nuevo_costo
                padre[estado_vecino] = estado_actual
                tipo_movimiento[estado_vecino] = tipo
                prioridad = nuevo_costo + heuristica(estacion_dest, destino)
                heapq.heappush(cola, (prioridad, estado_vecino))

    return None  # No existe ruta posible.


def _reconstruir_resultado(estado_final, padre, tipo_movimiento, costo_acumulado):
    camino = []
    estado = estado_final
    while estado is not None:
        estacion, linea = estado
        camino.append((estacion, linea, tipo_movimiento[estado], costo_acumulado[estado]))
        estado = padre[estado]
    camino.reverse()
    return {
        "pasos": camino,
        "tiempo_total": costo_acumulado[estado_final],
    }
