

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
    return [f["titulo"] for f in inventario if f["valor"] >= minimo]
