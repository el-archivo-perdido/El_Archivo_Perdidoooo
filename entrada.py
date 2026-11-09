
def leer_entero(mensaje, minimo, maximo):
<<<<<<< HEAD
    """Pide un entero en [minimo, maximo]; repite hasta que sea válido.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.
        minimo (int): valor mínimo aceptado.
        maximo (int): valor máximo aceptado.

    Retorna:
        int: el número ingresado, dentro del rango.
    """
=======
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"  Ingresa un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  Entrada inválida: escribe un número entero.")


def leer_texto(mensaje):
<<<<<<< HEAD
    """Pide un texto no vacío; repite hasta que lo sea.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.

    Retorna:
        str: el texto ingresado, sin espacios en los extremos.
    """
=======
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("  El texto no puede estar vacío.")


def leer_opcion(mensaje, validas):
<<<<<<< HEAD
    """Pide una opción que esté dentro de `validas`; repite hasta que lo sea.

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.
        validas (set[str]): opciones permitidas (en minúsculas).

    Retorna:
        str: la opción elegida, en minúsculas.
    """
=======
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    while True:
        opcion = input(mensaje).strip().lower()
        if opcion in validas:
            return opcion
        print(f"  Opción inválida. Elige una de: {', '.join(sorted(validas))}")


def leer_si_no(mensaje):
<<<<<<< HEAD
    """Pide una respuesta sí/no ('s' o 'n').

    Parámetros:
        mensaje (str): texto que se muestra al pedir el dato.

    Retorna:
        bool: True para 's', False para 'n'.
    """
=======
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    return leer_opcion(mensaje, {"s", "n"}) == "s"
