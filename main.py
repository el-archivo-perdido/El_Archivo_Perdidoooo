"""Menú principal y flujo de la partida."""
from entrada import leer_opcion, leer_si_no
from jugador import mostrar_estado, subir_nivel
from persistencia import (guardar_partida, cargar_partida, guardar_fragmentos,
                          registrar_puntaje, mostrar_puntajes)
from salas import (sala_vestibulo, sala_estanterias, sala_mapas,
                   sala_fichas, sala_sellos, sala_central)

SALAS = [sala_vestibulo, sala_estanterias, sala_mapas,
         sala_fichas, sala_sellos, sala_central]

RETROALIMENTACION = [
    "Variables: int, float, str y bool con conversión validada.",
    "Listas: inserción, eliminación, búsqueda, orden y comprensiones.",
    "Tuplas: posiciones inmutables y desempaquetado.",
    "Diccionarios: acceso por clave y manejo de KeyError.",
    "Conjuntos: sin duplicados; unión, intersección y diferencia.",
    "Árbol BST: el recorrido inorden entrega los datos ordenados.",
]


def nuevo_estado():
    """Crea el estado inicial de una partida nueva.

    Retorna:
        dict: estado con jugador (None), inventario vacío y sala 0.
    """
    return {"jugador": None, "inventario": [], "sala": 0}


def cierre(estado):
    """Cierra la partida: muestra el estado, registra el puntaje y da la retroalimentación.

    Parámetros:
        estado (dict): estado de la partida terminada.

    Retorna:
        None.
    """
    j = estado["jugador"]
    print("\n=== ¡ARCHIVO RESTAURADO! ===")
    mostrar_estado(j)
    registrar_puntaje(j["nombre"], j["puntaje"])
    mostrar_puntajes()
    print("\nRetroalimentación conceptual:")
    for linea in RETROALIMENTACION:
        print(f"  - {linea}")


def jugar(estado):
    """Ejecuta las salas en orden desde la sala guardada en el estado.

    Si la partida ya estaba completada no se vuelve a registrar el puntaje.

    Parámetros:
        estado (dict): estado de la partida (se modifica).

    Retorna:
        None.
    """
    if estado["sala"] >= len(SALAS):
        print("\nEsta partida ya fue completada.")
        mostrar_estado(estado["jugador"])
        return
    while estado["sala"] < len(SALAS):
        if estado["sala"] > 0:
            mostrar_estado(estado["jugador"])
        if SALAS[estado["sala"]](estado):
            estado["sala"] += 1
            subir_nivel(estado["jugador"])
            guardar_partida(estado)
        elif not estado["jugador"]["activo"]:
            print("\nTe quedaste sin vida. Fin del juego.")
            registrar_puntaje(estado["jugador"]["nombre"], estado["jugador"]["puntaje"])
            return
        elif not leer_si_no("¿Reintentar la sala? (s/n): "):
            guardar_partida(estado)
            return
    cierre(estado)


def menu():
    """Muestra el menú principal y atiende las opciones hasta que el usuario sale.

    Retorna:
        None.
    """
    while True:
        print("\n=== EL ARCHIVO PERDIDO ===")
        print("1. Nueva partida\n2. Cargar partida\n3. Puntajes\n4. Salir")
        opcion = leer_opcion("Opción: ", {"1", "2", "3", "4"})
        if opcion == "1":
            jugar(nuevo_estado())
        elif opcion == "2":
            estado = cargar_partida()
            if estado:
                guardar_fragmentos(estado["inventario"])   # sincroniza el archivo de fragmentos
                jugar(estado)
        elif opcion == "3":
            mostrar_puntajes()
        else:
            print("¡Hasta pronto!")
            break


if __name__ == "__main__":
    menu()
