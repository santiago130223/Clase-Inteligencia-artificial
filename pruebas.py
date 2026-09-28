from main import ejecutar

CASOS_DE_PRUEBA = [
    ("Ruta directa, sin transbordos", "Terminal Occidente", "Terminal Oriente"),
    ("Ruta con un transbordo", "Universidad", "Biblioteca"),
    ("Ruta larga entre extremos opuestos del sistema", "Terminal Sur", "Aeropuerto"),
    ("Origen igual a destino", "Centro", "Centro"),
    ("Estacion que no existe (manejo de errores)", "Marte", "Centro"),
]


def main():
    for i, (descripcion, origen, destino) in enumerate(CASOS_DE_PRUEBA, start=1):
        print("=" * 70)
        print(f"CASO DE PRUEBA {i}: {descripcion}")
        print(f"Origen: {origen} | Destino: {destino}")
        print("=" * 70)
        ejecutar(origen, destino, trazar_reglas=(i == 1))
        print()


if __name__ == "__main__":
    main()
