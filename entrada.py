"""Validación de entradas del usuario (reutilizable en todo el juego)."""


def leer_entero(mensaje, minimo, maximo):
    """Pide un entero en [minimo, maximo]; repite hasta que sea válido."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"  Ingresa un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  Entrada inválida: escribe un número entero.")


def leer_texto(mensaje):
    """Pide un texto no vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("  El texto no puede estar vacío.")


def leer_opcion(mensaje, validas):
    """Pide una opción que esté dentro de `validas` (conjunto de str)."""
    while True:
        opcion = input(mensaje).strip().lower()
        if opcion in validas:
            return opcion
        print(f"  Opción inválida. Elige una de: {', '.join(sorted(validas))}")


def leer_si_no(mensaje):
    """Devuelve True para 's' y False para 'n'."""
    return leer_opcion(mensaje, {"s", "n"}) == "s"
