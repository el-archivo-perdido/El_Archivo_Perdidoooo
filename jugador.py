"""Vestíbulo: atributos del jugador (int, float, str, bool)."""


def crear_jugador(nombre, dificultad):
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
    jugador["puntaje"] += float(puntos) * jugador["multiplicador"]


def perder_vida(jugador, dano):
    jugador["vida"] = max(0, jugador["vida"] - int(dano))
    if jugador["vida"] == 0:
        jugador["activo"] = False
    print(f"  -{dano} de vida. Vida actual: {jugador['vida']}")


def subir_nivel(jugador):
    jugador["nivel"] += 1


def mostrar_estado(jugador):
    print(f"\n[{jugador['nombre']}] Vida: {jugador['vida']} | "
          f"Puntaje: {jugador['puntaje']:.1f} | Nivel: {jugador['nivel']}")
