# Hecho: estacion(nombre, x, y)
ESTACIONES = {
    # Línea 1 - Roja (oriente-occidente)
    "Terminal Occidente": (0, 0),
    "Universidad": (2, 0),
    "Centro": (4, 0),
    "Parque": (6, 0),
    "Estadio": (8, 0),
    "Terminal Oriente": (10, 0),
    # Línea 2 - Azul (sur-norte), cruza la Línea 1 en "Centro"
    "Terminal Sur": (4, -6),
    "Hospital": (4, -4),
    "Mercado": (4, -2),
    "Biblioteca": (4, 2),
    "Estacion Norte": (4, 4),
    "Terminal Norte": (4, 6),
    # Línea 3 - Verde, cruza la Línea 1 en "Parque" y la Línea 2 en "Biblioteca"
    "Terminal Suroriente": (9, -5),
    "Zona Industrial": (8, -3),
    "Colegio": (5, 1),
    "Aeropuerto": (3, 5),
}

# Hecho: linea(nombre, [estaciones en orden], velocidad_promedio_kmh)
# El orden de la lista importa: define qué estaciones son adyacentes en esa línea.
LINEAS = {
    "Linea 1 - Roja": {
        "estaciones": [
            "Terminal Occidente",
            "Universidad",
            "Centro",
            "Parque",
            "Estadio",
            "Terminal Oriente",
        ],
        "velocidad_kmh": 25,
    },
    "Linea 2 - Azul": {
        "estaciones": [
            "Terminal Sur",
            "Hospital",
            "Mercado",
            "Centro",
            "Biblioteca",
            "Estacion Norte",
            "Terminal Norte",
        ],
        "velocidad_kmh": 35,
    },
    "Linea 3 - Verde": {
        "estaciones": [
            "Terminal Suroriente",
            "Zona Industrial",
            "Parque",
            "Colegio",
            "Biblioteca",
            "Aeropuerto",
        ],
        "velocidad_kmh": 20,
    },
}

# Hecho: tiempo fijo (en minutos) que penaliza hacer un transbordo entre líneas.
# Representa el tiempo de caminar entre andenes y esperar el siguiente vehículo.
PENALIZACION_TRANSBORDO_MIN = 5

# Se usa para construir una heurística admisible en la búsqueda A*:
# ninguna línea del sistema es más rápida que esta velocidad.
VELOCIDAD_MAXIMA_KMH = max(linea["velocidad_kmh"] for linea in LINEAS.values())
