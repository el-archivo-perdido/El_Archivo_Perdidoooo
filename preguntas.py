<<<<<<< HEAD
"""Preguntas conceptuales: (pregunta, opciones, índice correcto 1-based, explicación)."""
=======

>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
from entrada import leer_entero
from jugador import sumar_puntos

PREGUNTAS = {
    "vestibulo": ("¿Qué ocurre al ejecutar int('abc')?",
                  ["Devuelve 0", "Lanza ValueError", "Devuelve None"], 2,
                  "int() no puede convertir texto no numérico y lanza ValueError; por eso se usa try/except."),
    "estanterias": ("¿Qué hace lista.append(x)?",
                    ["Agrega x al final", "Agrega x al inicio", "Reemplaza la lista"], 1,
                    "append agrega al final; insert(0, x) agregaría al inicio y es más costoso."),
    "mapas": ("¿Por qué una posición (fila, col) es mejor como tupla?",
              ["Se imprime más rápido", "Es inmutable: no se altera por error", "Admite duplicados"], 2,
              "Las tuplas son inmutables, así una coordenada no cambia accidentalmente."),
    "fichas": ("¿Qué ventaja tiene buscar por clave en un diccionario?",
               ["Acceso directo sin recorrer todo", "Mantiene orden alfabético", "Permite claves repetidas"], 1,
               "El diccionario usa hash: el acceso por clave es O(1) en promedio."),
    "sellos": ("¿Qué ocurre al agregar un elemento repetido a un conjunto?",
               ["Se duplica", "Lanza error", "Se ignora"], 3,
               "Un conjunto solo guarda elementos únicos; el repetido se ignora."),
    "central": ("¿Qué devuelve el recorrido inorden de un BST?",
                ["Los elementos en orden ascendente", "Solo la raíz", "El orden de inserción"], 1,
                "Visita izquierda, nodo, derecha: en un BST eso produce los datos ordenados."),
}


def hacer_pregunta(jugador, clave):
<<<<<<< HEAD
    """Hace la pregunta conceptual de una sala y otorga 10 puntos si se acierta.

    Parámetros:
        jugador (dict): jugador (puede recibir puntos).
        clave (str): clave de la pregunta en PREGUNTAS (por ejemplo "mapas").

    Retorna:
        None (imprime el resultado y la explicación).
    """
=======
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    pregunta, opciones, correcta, explicacion = PREGUNTAS[clave]
    print(f"\n--- Pregunta conceptual ---\n{pregunta}")
    for i, op in enumerate(opciones, start=1):
        print(f"  {i}. {op}")
    if leer_entero("Tu respuesta: ", 1, len(opciones)) == correcta:
        print("¡Correcto! +10 puntos.")
        sumar_puntos(jugador, 10)
    else:
        print("Incorrecto.")
    print(f"Explicación: {explicacion}")
