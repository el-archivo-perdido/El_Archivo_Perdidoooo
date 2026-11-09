"""Persistencia: partida, fragmentos recolectados y tabla de puntajes (JSON).

Todas las lecturas y escrituras manejan excepciones para que el juego no se caiga
ante archivos inexistentes, dañados o sin permisos.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PARTIDA = os.path.join(BASE_DIR, "datos", "partida.json")
RUTA_PUNTAJES = os.path.join(BASE_DIR, "datos", "puntajes.json")
RUTA_FRAGMENTOS = os.path.join(BASE_DIR, "datos", "fragmentos.json")

CLAVES_JUGADOR = {"nombre", "vida", "puntaje", "nivel", "multiplicador", "activo"}
CLAVES_FRAGMENTO = {"codigo", "titulo", "sala", "valor"}


def _escribir_json(datos, ruta):
    """Escribe datos en un archivo JSON, creando la carpeta si no existe.

    Parámetros:
        datos: objeto serializable a JSON.
        ruta (str): ruta del archivo destino.

    Retorna:
        None.

    Lanza:
        OSError: si no se puede crear la carpeta o escribir el archivo.
    """
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def _estado_valido(estado):
    """Verifica que un estado cargado tenga la estructura esperada.

    Parámetros:
        estado: objeto leído desde el archivo de guardado.

    Retorna:
        bool: True si es un diccionario con jugador, inventario y sala coherentes.
    """
    return (isinstance(estado, dict)
            and {"jugador", "inventario", "sala"} <= set(estado)
            and isinstance(estado["jugador"], dict)
            and CLAVES_JUGADOR <= set(estado["jugador"])
            and isinstance(estado["inventario"], list)
            and all(isinstance(f, dict) for f in estado["inventario"])
            and isinstance(estado["sala"], int)
            and estado["sala"] >= 0)


def guardar_partida(estado, ruta=None):
    """Guarda el estado de la partida en un archivo JSON.

    Parámetros:
        estado (dict): estado con jugador, inventario y sala.
        ruta (str | None): archivo destino; por defecto RUTA_PARTIDA.

    Retorna:
        bool: True si se guardó, False si hubo un error de escritura.
    """
    ruta = ruta or RUTA_PARTIDA
    try:
        _escribir_json(estado, ruta)
        print("  (Partida guardada)")
        return True
    except (OSError, TypeError) as e:
        print(f"  No se pudo guardar: {e}")
        return False


def cargar_partida(ruta=None):
    """Carga una partida guardada, validando su estructura.

    Parámetros:
        ruta (str | None): archivo de origen; por defecto RUTA_PARTIDA.

    Retorna:
        dict | None: el estado de la partida, o None si no existe o está dañado.
    """
    ruta = ruta or RUTA_PARTIDA
    try:
        with open(ruta, encoding="utf-8") as f:
            estado = json.load(f)
        if not _estado_valido(estado):
            raise ValueError("estructura inválida")
        return estado
    except FileNotFoundError:
        print("No hay partida guardada.")
    except ValueError:      # incluye JSONDecodeError y UnicodeDecodeError
        print("El archivo de guardado está dañado.")
    except OSError as e:
        print(f"No se pudo leer el archivo: {e}")
    return None


def guardar_fragmentos(fragmentos, ruta=None):
    """Guarda en un archivo los fragmentos recolectados (lista de diccionarios).

    Parámetros:
        fragmentos (list[dict]): fragmentos del inventario.
        ruta (str | None): archivo destino; por defecto RUTA_FRAGMENTOS.

    Retorna:
        bool: True si se guardó, False si hubo un error de escritura.
    """
    ruta = ruta or RUTA_FRAGMENTOS
    try:
        _escribir_json(fragmentos, ruta)
        return True
    except (OSError, TypeError) as e:
        print(f"  No se pudo guardar los fragmentos: {e}")
        return False


def cargar_fragmentos(ruta=None):
    """Lee desde un archivo los fragmentos recolectados (Paso 1 de la actividad clave).

    Parámetros:
        ruta (str | None): archivo de origen; por defecto RUTA_FRAGMENTOS.

    Retorna:
        list[dict] | None: la lista de fragmentos, o None si falta o está dañado.
    """
    ruta = ruta or RUTA_FRAGMENTOS
    try:
        with open(ruta, encoding="utf-8") as f:
            fragmentos = json.load(f)
        if (not isinstance(fragmentos, list)
                or not all(isinstance(x, dict) and CLAVES_FRAGMENTO <= set(x)
                           for x in fragmentos)):
            raise ValueError("estructura inválida")
        return fragmentos
    except FileNotFoundError:
        print("  No existe el archivo de fragmentos.")
    except ValueError:
        print("  El archivo de fragmentos está dañado.")
    except OSError as e:
        print(f"  No se pudo leer el archivo de fragmentos: {e}")
    return None


def leer_puntajes(ruta=None):
    """Lee la tabla de puntajes.

    Parámetros:
        ruta (str | None): archivo de origen; por defecto RUTA_PUNTAJES.

    Retorna:
        list[dict]: registros {"nombre", "puntaje"}; lista vacía si no hay datos válidos.
    """
    ruta = ruta or RUTA_PUNTAJES
    try:
        with open(ruta, encoding="utf-8") as f:
            tabla = json.load(f)
    except (OSError, ValueError):
        return []
    if not isinstance(tabla, list):
        return []
    return [r for r in tabla
            if isinstance(r, dict) and "nombre" in r
            and isinstance(r.get("puntaje"), (int, float))]


def registrar_puntaje(nombre, puntaje, ruta=None):
    """Agrega un puntaje a la tabla y conserva solo los 10 mejores.

    Parámetros:
        nombre (str): nombre del jugador.
        puntaje (float): puntaje obtenido.
        ruta (str | None): archivo de la tabla; por defecto RUTA_PUNTAJES.

    Retorna:
        None.
    """
    ruta = ruta or RUTA_PUNTAJES
    tabla = leer_puntajes(ruta)
    tabla.append({"nombre": nombre, "puntaje": round(puntaje, 1)})
    tabla.sort(key=lambda r: r["puntaje"], reverse=True)
    try:
        _escribir_json(tabla[:10], ruta)
    except OSError as e:
        print(f"No se pudo guardar el puntaje: {e}")


def mostrar_puntajes():
    """Imprime la tabla de puntajes.

    Retorna:
        None.
    """
    tabla = leer_puntajes()
    print("\n=== TABLA DE PUNTAJES ===")
    if not tabla:
        print("Aún no hay puntajes.")
    for i, r in enumerate(tabla, start=1):
        print(f"{i}. {r['nombre']:<15} {r['puntaje']}")
