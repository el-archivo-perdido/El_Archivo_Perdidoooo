"""Validación de entradas del usuario (reutilizable en todo el juego)."""


def leer_entero(mensaje, minimo, maximo):
    """Pide un entero en [minimo, maximo]; repite hasta que sea válido.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.
        minimo (int): valor mínimo aceptado.
        maximo (int): valor máximo aceptado.

    Retorna:
        int: el número ingresado, dentro del rango.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"  Ingresa un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  Entrada inválida: escribe un número entero.")


def leer_texto(mensaje):
    """Pide un texto no vacío; repite hasta que lo sea.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.

    Retorna:
        str: el texto ingresado, sin espacios en los extremos.
    """
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("  El texto no puede estar vacío.")


def leer_opcion(mensaje, validas):
    """Pide una opción que esté dentro de `validas`; repite hasta que lo sea.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.
        validas (set[str]): opciones permitidas (en minúsculas).

    Retorna:
        str: la opción elegida, en minúsculas.
    """
    while True:
        opcion = input(mensaje).strip().lower()
        if opcion in validas:
            return opcion
        print(f"  Opción inválida. Elige una de: {', '.join(sorted(validas))}")


def leer_si_no(mensaje):
    """Pide una respuesta sí/no ('s' o 'n').

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.

    Retorna:
        bool: True para 's', False para 'n'.
    """
    return leer_opcion(mensaje, {"s", "n"}) == "s"
