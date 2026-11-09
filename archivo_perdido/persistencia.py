"""Guardado/carga de partida y tabla de puntajes (JSON) con manejo de excepciones."""
import json
import os

RUTA_PARTIDA = "datos/partida.json"
RUTA_PUNTAJES = "datos/puntajes.json"


def guardar_partida(estado, ruta=RUTA_PARTIDA):
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(estado, f, ensure_ascii=False, indent=2)
        print("  (Partida guardada)")
    except OSError as e:
        print(f"  No se pudo guardar: {e}")


def cargar_partida(ruta=RUTA_PARTIDA):
    try:
        with open(ruta, encoding="utf-8") as f:
            estado = json.load(f)
        if not {"jugador", "inventario", "sala"} <= set(estado):
            raise ValueError("faltan claves")
        return estado
    except FileNotFoundError:
        print("No hay partida guardada.")
    except (json.JSONDecodeError, ValueError):
        print("El archivo de guardado está dañado.")
    except OSError as e:
        print(f"No se pudo leer el archivo: {e}")
    return None


def leer_puntajes(ruta=RUTA_PUNTAJES):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def registrar_puntaje(nombre, puntaje, ruta=RUTA_PUNTAJES):
    tabla = leer_puntajes(ruta)
    tabla.append({"nombre": nombre, "puntaje": round(puntaje, 1)})
    tabla.sort(key=lambda r: r["puntaje"], reverse=True)
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(tabla[:10], f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"No se pudo guardar el puntaje: {e}")


def mostrar_puntajes():
    tabla = leer_puntajes()
    print("\n=== TABLA DE PUNTAJES ===")
    if not tabla:
        print("Aún no hay puntajes.")
    for i, r in enumerate(tabla, start=1):
        print(f"{i}. {r['nombre']:<15} {r['puntaje']}")
