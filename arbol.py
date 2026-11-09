"""Sala Central: árbol binario de búsqueda (BST) propio, sin librerías externas.

La clave de cada nodo es el código numérico del fragmento (por ejemplo, "F03" -> 3).
Las operaciones son iterativas para que un árbol degenerado (por inserciones
ordenadas) con cientos de nodos no agote el límite de recursión de Python.
"""


def codigo_numerico(codigo):
    """Convierte un código de fragmento a su clave numérica.

    Propósito: obtener la clave entera con que se ordena y se busca en el árbol.

    Parámetros:
        codigo (str | int): código como "F03", "f3" o "3".

    Retorna:
        int: la clave numérica (por ejemplo, 3).

    Lanza:
        ValueError: si el código no contiene un número entero.
    """
    texto = str(codigo).strip().upper()
    if texto.startswith("F"):
        texto = texto[1:]
    return int(texto)


def esta_ordenada(fragmentos):
    """Comprueba que una lista de fragmentos esté en orden estrictamente ascendente.

    Parámetros:
        fragmentos (list[dict]): fragmentos con la clave "codigo".

    Retorna:
        bool: True si las claves numéricas van de menor a mayor sin repetirse.
    """
    claves = [codigo_numerico(f["codigo"]) for f in fragmentos]
    return all(a < b for a, b in zip(claves, claves[1:]))


class Nodo:
    """Nodo del BST: guarda un fragmento, su clave numérica y los dos hijos."""

    def __init__(self, fragmento):
        """Crea un nodo hoja a partir de un fragmento.

        Parámetros:
            fragmento (dict): diccionario con al menos la clave "codigo".

        Retorna:
            None (inicializa los atributos clave, fragmento, izq y der).
        """
        self.clave = codigo_numerico(fragmento["codigo"])
        self.fragmento = fragmento
        self.izq = None
        self.der = None


class ArbolBST:
    """Árbol binario de búsqueda de fragmentos, ordenado por código numérico."""

    def __init__(self):
        """Crea un árbol vacío.

        Retorna:
            None (inicializa raiz = None y tamano = 0).
        """
        self.raiz = None
        self.tamano = 0

    def insertar(self, fragmento):
        """Inserta un fragmento respetando la propiedad del BST.

        Menores a la izquierda, mayores a la derecha; las claves repetidas se ignoran.

        Parámetros:
            fragmento (dict): fragmento con la clave "codigo".

        Retorna:
            bool: True si se insertó, False si la clave ya existía.
        """
        nuevo = Nodo(fragmento)
        if self.raiz is None:
            self.raiz = nuevo
            self.tamano = 1
            return True
        actual = self.raiz
        while True:
            if nuevo.clave < actual.clave:
                if actual.izq is None:
                    actual.izq = nuevo
                    break
                actual = actual.izq
            elif nuevo.clave > actual.clave:
                if actual.der is None:
                    actual.der = nuevo
                    break
                actual = actual.der
            else:
                return False
        self.tamano += 1
        return True

    def buscar_con_conteo(self, codigo):
        """Busca un fragmento por código y cuenta las comparaciones realizadas.

        Se cuenta una comparación por cada nodo visitado (en cada nodo se compara
        la clave buscada con la del nodo para decidir si es igual o hacia dónde ir).

        Parámetros:
            codigo (str | int): código a buscar ("F03", "3", 3...).

        Retorna:
            tuple[dict | None, int]: (fragmento o None si no existe, comparaciones).

        Lanza:
            ValueError: si el código no es numérico.
        """
        clave = codigo_numerico(codigo)
        actual = self.raiz
        comparaciones = 0
        while actual is not None:
            comparaciones += 1
            if clave == actual.clave:
                return actual.fragmento, comparaciones
            actual = actual.izq if clave < actual.clave else actual.der
        return None, comparaciones

    def buscar(self, codigo):
        """Busca un fragmento por código.

        Parámetros:
            codigo (str | int): código a buscar.

        Retorna:
            dict | None: el fragmento, o None si no está en el árbol.
        """
        return self.buscar_con_conteo(codigo)[0]

    def inorden(self):
        """Recorre el árbol en inorden (izquierda, nodo, derecha).

        En un BST este recorrido entrega los fragmentos ordenados por clave.

        Retorna:
            list[dict]: los fragmentos en el orden visitado.
        """
        resultado = []
        pila = []
        actual = self.raiz
        while pila or actual is not None:
            while actual is not None:        # bajar todo lo posible por la izquierda
                pila.append(actual)
                actual = actual.izq
            actual = pila.pop()
            resultado.append(actual.fragmento)
            actual = actual.der              # luego visitar el subárbol derecho
        return resultado

    def altura(self):
        """Calcula la altura del árbol (número de niveles).

        Un árbol vacío tiene altura 0; un árbol degenerado de n nodos, altura n.

        Retorna:
            int: cantidad de niveles del árbol.
        """
        if self.raiz is None:
            return 0
        maxima = 0
        pila = [(self.raiz, 1)]
        while pila:
            nodo, nivel = pila.pop()
            maxima = max(maxima, nivel)
            if nodo.izq is not None:
                pila.append((nodo.izq, nivel + 1))
            if nodo.der is not None:
                pila.append((nodo.der, nivel + 1))
        return maxima
