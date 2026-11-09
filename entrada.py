
def leer_entero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"  Ingresa un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  Entrada inválida: escribe un número entero.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("  El texto no puede estar vacío.")


def leer_opcion(mensaje, validas):
    while True:
        opcion = input(mensaje).strip().lower()
        if opcion in validas:
            return opcion
        print(f"  Opción inválida. Elige una de: {', '.join(sorted(validas))}")


def leer_si_no(mensaje):
    return leer_opcion(mensaje, {"s", "n"}) == "s"
