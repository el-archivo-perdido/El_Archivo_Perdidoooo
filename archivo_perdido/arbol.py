"""Sala Central: árbol binario de búsqueda propio (sin librerías)."""


class Nodo:
    def __init__(self, fragmento):
        self.fragmento = fragmento
        self.izq = None
        self.der = None


class ArbolBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, fragmento):
        self.raiz = self._insertar(self.raiz, fragmento)

    def _insertar(self, nodo, fragmento):
        if nodo is None:
            return Nodo(fragmento)
        if fragmento["codigo"] < nodo.fragmento["codigo"]:
            nodo.izq = self._insertar(nodo.izq, fragmento)
        elif fragmento["codigo"] > nodo.fragmento["codigo"]:
            nodo.der = self._insertar(nodo.der, fragmento)
        return nodo

    def buscar(self, codigo):
        actual = self.raiz
        while actual is not None:
            if codigo == actual.fragmento["codigo"]:
                return actual.fragmento
            actual = actual.izq if codigo < actual.fragmento["codigo"] else actual.der
        return None

    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, resultado):
        if nodo is not None:
            self._inorden(nodo.izq, resultado)
            resultado.append(nodo.fragmento)
            self._inorden(nodo.der, resultado)
