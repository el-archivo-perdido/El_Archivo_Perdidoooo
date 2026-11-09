<<<<<<< HEAD
"""Sala de Estanterías: operaciones de lista sobre el inventario."""
from arbol import codigo_numerico
=======
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097


def insertar(inventario, fragmento):
    """Inserta un fragmento al final del inventario.

    Parámetros:
        inventario (list[dict]): lista de fragmentos (se modifica).
        fragmento (dict): fragmento a agregar.

    Retorna:
        None.
    """
    inventario.append(fragmento)


def eliminar(inventario, codigo):
    """Elimina del inventario el primer fragmento con el código dado.

    Parámetros:
        inventario (list[dict]): lista de fragmentos (se modifica).
        codigo (str): código del fragmento a eliminar.

    Retorna:
        dict | None: el fragmento eliminado, o None si no estaba.
    """
    for i, f in enumerate(inventario):
        if f["codigo"] == codigo:
            return inventario.pop(i)
    return None


def buscar(inventario, codigo):
    """Busca un fragmento por código recorriendo la lista (búsqueda secuencial).

    Parámetros:
        inventario (list[dict]): lista de fragmentos.
        codigo (str): código a buscar.

    Retorna:
        dict | None: el fragmento encontrado, o None.
    """
    for f in inventario:
        if f["codigo"] == codigo:
            return f
    return None


def buscar_secuencial_con_conteo(fragmentos, codigo):
    """Búsqueda secuencial por clave numérica que cuenta las comparaciones.

    Se cuenta una comparación por cada elemento examinado, igual que el árbol
    cuenta una por cada nodo visitado, para que ambos valores sean comparables.

    Parámetros:
        fragmentos (list[dict]): lista de fragmentos.
        codigo (str | int): código a buscar ("F03", "3", 3...).

    Retorna:
        tuple[dict | None, int]: (fragmento o None, comparaciones realizadas).

    Lanza:
        ValueError: si el código no es numérico.
    """
    clave = codigo_numerico(codigo)
    comparaciones = 0
    for f in fragmentos:
        comparaciones += 1
        if codigo_numerico(f["codigo"]) == clave:
            return f, comparaciones
    return None, comparaciones


def ordenar(inventario):
    """Ordena el inventario por código (en el lugar).

    Parámetros:
        inventario (list[dict]): lista de fragmentos (se modifica).

    Retorna:
        None.
    """
    inventario.sort(key=lambda f: f["codigo"])


def eliminar_duplicados(inventario):
<<<<<<< HEAD
    """Quita fragmentos repetidos usando un conjunto de códigos ya vistos.

    Conserva la primera aparición de cada código y respeta el orden.

    Parámetros:
        inventario (list[dict]): lista de fragmentos (se modifica en el lugar).

    Retorna:
        int: cuántos fragmentos se descartaron.
    """
=======
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    vistos = set()
    unicos = []
    for f in inventario:
        if f["codigo"] not in vistos:
            vistos.add(f["codigo"])
            unicos.append(f)
    quitados = len(inventario) - len(unicos)
    inventario[:] = unicos
    return quitados


def titulos_valiosos(inventario, minimo=40):
<<<<<<< HEAD
    """Lista los títulos de los fragmentos de valor alto (comprensión de listas).

    Parámetros:
        inventario (list[dict]): lista de fragmentos.
        minimo (int): valor mínimo para considerarse valioso.

    Retorna:
        list[str]: títulos de los fragmentos con valor >= minimo.
    """
=======
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    return [f["titulo"] for f in inventario if f["valor"] >= minimo]
