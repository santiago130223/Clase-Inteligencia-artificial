# Sistema Inteligente de Rutas - Transporte Masivo (SITM ficticio)

Actividad 3 del curso de Inteligencia Artificial: sistema inteligente basado
en conocimiento que, a partir de una base de reglas lógicas, calcula la mejor
ruta entre dos estaciones de un sistema de transporte masivo.

## Cómo está resuelta la actividad

| Requisito de la actividad | Dónde está en el código |
|---|---|
| Representación del conocimiento (lógica, cap. 2) | `sistema_transporte/base_conocimiento.py`: hechos de estaciones, líneas y coordenadas. |
| Sistema basado en reglas (cap. 3) | `sistema_transporte/motor_reglas.py`: reglas SI-ENTONCES que derivan tramos transitables y estaciones de transbordo. |
| Búsqueda heurística (cap. 9) | `sistema_transporte/busqueda.py`: algoritmo **A\*** que usa la distancia en línea recta como heurística para encontrar la ruta de menor tiempo. |
| Programa ejecutable | `main.py` (modo interactivo o por línea de comandos). |
| Pruebas | `pruebas.py` (5 casos representativos, listos para documentar). |

## El sistema modelado

Es un sistema de transporte **ficticio** con 3 líneas y 3 estaciones de
transbordo, pensado para poder explicar el código y las reglas con claridad
en el video:

- **Línea 1 - Roja**: Terminal Occidente ↔ Terminal Oriente (6 estaciones).
- **Línea 2 - Azul**: Terminal Sur ↔ Terminal Norte (7 estaciones), cruza la
  Línea 1 en **Centro**.
- **Línea 3 - Verde**: Terminal Suroriente ↔ Aeropuerto (6 estaciones), cruza
  la Línea 1 en **Parque** y la Línea 2 en **Biblioteca**.

Cada estación tiene coordenadas (x, y) ficticias en kilómetros, usadas para
calcular tiempos de viaje y la heurística de A*. Cambiar de línea en una
estación de transbordo cuesta una penalización fija de 5 minutos.

Puedes ver la lista completa de estaciones con:

```bash
python main.py --estaciones
```

## Requisitos

- Python 3.9 o superior.
- No requiere ninguna librería externa (solo la librería estándar de Python).

## Cómo ejecutar

Modo interactivo (te pregunta origen y destino):

```bash
python main.py
```

Modo directo (sin preguntas), útil para el video:

```bash
python main.py "Terminal Occidente" "Aeropuerto"
```

Ejecutar los casos de prueba y generar el documento de evidencias:

```bash
python pruebas.py > pruebas_resultado.txt
```

El archivo `pruebas_resultado.txt` se puede abrir en cualquier editor e
"Imprimir como PDF" para producir el entregable **Documento PDF con las
pruebas realizadas**.

## Estructura del proyecto

```
Proyecto IA/
├── main.py                          # Punto de entrada (CLI)
├── pruebas.py                       # Casos de prueba automatizados
├── sistema_transporte/
│   ├── base_conocimiento.py         # Hechos: estaciones, líneas, coordenadas
│   ├── motor_reglas.py              # Reglas SI-ENTONCES (deriva el grafo de rutas)
│   └── busqueda.py                  # Búsqueda heurística A*
└── README.md
```

## Cómo adaptarlo a un sistema real (opcional)

Si el equipo prefiere usar datos reales de su ciudad, solo hay que editar
`sistema_transporte/base_conocimiento.py`:

1. Agregar las estaciones reales al diccionario `ESTACIONES` con
   coordenadas aproximadas (o reales, si se consiguen).
2. Agregar cada línea/ruta real a `LINEAS`, en el orden correcto de sus
   estaciones, con su velocidad promedio.

El motor de reglas y el algoritmo de búsqueda no necesitan ningún cambio.

## Nota para el trabajo en equipo

El log de git debe evidenciar el aporte de cada integrante. Cada miembro del
equipo debe hacer sus propios commits (con su nombre/usuario configurado en
git) desde su propia máquina, por ejemplo repartiendo así el trabajo:

- Integrante 1: `base_conocimiento.py` (modelar el sistema de transporte).
- Integrante 2: `motor_reglas.py` (reglas lógicas).
- Integrante 3: `busqueda.py` (algoritmo de búsqueda).
- Integrante 4: `main.py`, `pruebas.py` y documentación/video.

Recuerden agregar al tutor como colaborador del repositorio en GitHub/GitLab.
