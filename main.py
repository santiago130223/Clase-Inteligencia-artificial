"""
Sistema inteligente basado en conocimiento para calcular la mejor ruta entre
dos estaciones del Sistema Integrado de Transporte Masivo (SITM).

Actividad 3 - Sistemas inteligentes basados en conocimiento.

Uso:
    python main.py                     -> modo interactivo
    python main.py "Origen" "Destino"  -> modo directo (sin preguntas)
    python main.py --estaciones        -> lista todas las estaciones disponibles
"""

import sys

from sistema_transporte.base_conocimiento import ESTACIONES, LINEAS
from sistema_transporte.busqueda import buscar_mejor_ruta


def listar_estaciones():
    print("Estaciones disponibles en el sistema:\n")
    for nombre_linea, datos in LINEAS.items():
        print(f"{nombre_linea}:")
        for estacion in datos["estaciones"]:
            print(f"  - {estacion}")
        print()


def imprimir_ruta(resultado, origen, destino):
    print(f"\nMejor ruta encontrada: {origen} -> {destino}")
    print("-" * 60)

    pasos = resultado["pasos"]
    _, linea_actual, _, _ = pasos[0]
    print(f"1. Abordar {linea_actual} en '{pasos[0][0]}'")

    numero = 2
    for i in range(1, len(pasos)):
        estacion, linea, tipo, costo_acumulado = pasos[i]
        estacion_anterior, linea_anterior, _, costo_anterior = pasos[i - 1]
        duracion = round(costo_acumulado - costo_anterior, 1)

        if tipo == "transbordo":
            print(
                f"{numero}. Transbordo en '{estacion}': "
                f"{linea_anterior} -> {linea} ({duracion} min)"
            )
        else:
            print(f"{numero}. Viajar a '{estacion}' por {linea} ({duracion} min)")
        numero += 1

    print("-" * 60)
    print(f"Tiempo total estimado: {round(resultado['tiempo_total'], 1)} minutos")


def ejecutar(origen, destino, trazar_reglas=True):
    if trazar_reglas:
        print("Motor de reglas: derivando conocimiento a partir de los hechos...\n")

    try:
        resultado = buscar_mejor_ruta(origen, destino, trazar=trazar_reglas)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print()
    if resultado is None:
        print(f"No se encontro una ruta entre '{origen}' y '{destino}'.")
        return

    imprimir_ruta(resultado, origen, destino)


def modo_interactivo():
    print("=== Planificador de rutas - SITM ===\n")
    listar_estaciones()
    origen = input("Estacion de origen: ").strip()
    destino = input("Estacion de destino: ").strip()
    ejecutar(origen, destino)


def main():
    argumentos = sys.argv[1:]

    if argumentos and argumentos[0] == "--estaciones":
        listar_estaciones()
        return

    if len(argumentos) >= 2:
        origen, destino = argumentos[0], argumentos[1]
        ejecutar(origen, destino)
        return

    modo_interactivo()


if __name__ == "__main__":
    main()
