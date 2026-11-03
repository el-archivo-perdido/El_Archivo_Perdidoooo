"""Sala de Estanterías: operaciones de lista sobre el inventario."""


def insertar(inventario, fragmento):
    inventario.append(fragmento)


def eliminar(inventario, codigo):
    for i, f in enumerate(inventario):
        if f["codigo"] == codigo:
            return inventario.pop(i)
    return None


def buscar(inventario, codigo):
    for f in inventario:
        if f["codigo"] == codigo:
            return f
    return None


def ordenar(inventario):
    inventario.sort(key=lambda f: f["codigo"])


def eliminar_duplicados(inventario):
    """Quita fragmentos repetidos usando un conjunto. Devuelve cuántos quitó."""
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
    """Comprensión de listas."""
    return [f["titulo"] for f in inventario if f["valor"] >= minimo]
