
def crear_jugador(nombre, dificultad):
    """Crea el diccionario del jugador con tipos explícitos.

    Parámetros:
        nombre (str): nombre del jugador.
        dificultad (int): 1 (fácil), 2 (media) o 3 (difícil).

    Retorna:
        dict: jugador con nombre (str), vida (int), puntaje (float), nivel (int),
        multiplicador (float) y activo (bool).
    """
    multiplicador = {1: 1.0, 2: 1.5, 3: 2.0}[dificultad]   # float
    return {
        "nombre": str(nombre).strip(),   # str
        "vida": 100,                     # int
        "puntaje": 0.0,                  # float
        "nivel": 1,                      # int
        "multiplicador": multiplicador,  # float
        "activo": True,                  # bool
    }


def sumar_puntos(jugador, puntos):
    """Suma puntos al jugador aplicando su multiplicador de dificultad.

    Parámetros:
        jugador (dict): jugador (se modifica).
        puntos (int | float): puntos base a sumar.

    Retorna:
        None.
    """
    jugador["puntaje"] += float(puntos) * jugador["multiplicador"]


def perder_vida(jugador, dano):
    """Resta vida al jugador (mínimo 0) y lo desactiva si llega a 0.

    Parámetros:
        jugador (dict): jugador (se modifica).
        dano (int): vida a restar.

    Retorna:
        None.
    """
    jugador["vida"] = max(0, jugador["vida"] - int(dano))
    if jugador["vida"] == 0:
        jugador["activo"] = False
    print(f"  -{dano} de vida. Vida actual: {jugador['vida']}")


def subir_nivel(jugador):
    """Sube un nivel al jugador.

    Parámetros:
        jugador (dict): jugador (se modifica).

    Retorna:
        None.
    """
    jugador["nivel"] += 1


def mostrar_estado(jugador):
    """Imprime nombre, vida, puntaje y nivel del jugador.

    Parámetros:
        jugador (dict): jugador a mostrar.

    Retorna:
        None.
    """
    print(f"\n[{jugador['nombre']}] Vida: {jugador['vida']} | "
          f"Puntaje: {jugador['puntaje']:.1f} | Nivel: {jugador['nivel']}")
