"""Sala Central: actividad clave «La Reconstrucción del Catálogo» (6 pasos visibles)."""
from arbol import ArbolBST, codigo_numerico, esta_ordenada
from catalogo import UBICACIONES
from entrada import leer_texto
from inventario import eliminar_duplicados, buscar_secuencial_con_conteo
from jugador import sumar_puntos, perder_vida
from persistencia import cargar_fragmentos
from preguntas import hacer_pregunta

CAMPOS = ("codigo", "titulo", "sala", "valor")
MAX_INTENTOS = 3
PUNTOS_POR_FRAGMENTO = 10
PENALIZACION_POR_INTENTO = 5


def fragmento_valido(fragmento):
    """Indica si un fragmento tiene todos sus campos y una ubicación conocida.

    Parámetros:
        fragmento (dict): fragmento a revisar.

    Retorna:
        bool: True si es válido.
    """
    return (isinstance(fragmento, dict)
            and all(c in fragmento for c in CAMPOS)
            and fragmento["codigo"] in UBICACIONES)


def paso_carga():
    """Paso 1: lee desde el archivo los fragmentos recolectados.

    Retorna:
        list[dict] | None: fragmentos leídos, o None si no se pudo leer el archivo.
    """
    print("\nPaso 1/6 - Carga: leyendo los fragmentos desde el archivo...")
    fragmentos = cargar_fragmentos()
    if fragmentos is not None:
        print(f"  Fragmentos leídos: {len(fragmentos)}")
    return fragmentos


def paso_depuracion(fragmentos):
    """Paso 2: elimina los fragmentos duplicados con un conjunto de códigos.

    Parámetros:
        fragmentos (list[dict]): lista a depurar (se modifica en el lugar).

    Retorna:
        int: cuántos fragmentos se descartaron.
    """
    print("\nPaso 2/6 - Depuración: eliminando duplicados con un conjunto de códigos...")
    descartados = eliminar_duplicados(fragmentos)
    print(f"  Fragmentos descartados: {descartados}")
    print(f"  Fragmentos únicos: {len(fragmentos)}")
    return descartados


def paso_ubicacion(fragmentos):
    """Paso 3: asocia a cada fragmento válido su tupla (estante, nivel).

    Parámetros:
        fragmentos (list[dict]): fragmentos ya depurados.

    Retorna:
        tuple[list[dict], dict]: (fragmentos válidos, {código: (estante, nivel)}).
    """
    print("\nPaso 3/6 - Ubicación: asignando (estante, nivel) a cada fragmento...")
    validos = [f for f in fragmentos if fragmento_valido(f)]
    ubicaciones = {f["codigo"]: UBICACIONES[f["codigo"]] for f in validos}
    for codigo, (estante, nivel) in sorted(ubicaciones.items()):
        print(f"  {codigo} -> estante {estante}, nivel {nivel}")
    invalidos = len(fragmentos) - len(validos)
    if invalidos:
        print(f"  Fragmentos inválidos ignorados: {invalidos}")
    return validos, ubicaciones


def paso_construccion(validos, ubicaciones):
    """Paso 4: inserta los fragmentos en el BST (clave = código numérico).

    Se insertan en el orden de las estanterías (estante, nivel).

    Parámetros:
        validos (list[dict]): fragmentos válidos.
        ubicaciones (dict): {código: (estante, nivel)}.

    Retorna:
        ArbolBST: el árbol construido.
    """
    print("\nPaso 4/6 - Construcción: insertando en el árbol binario de búsqueda...")
    orden = sorted(validos, key=lambda f: ubicaciones[f["codigo"]])
    print("  Orden de inserción:", [f["codigo"] for f in orden])
    arbol = ArbolBST()
    for fragmento in orden:
        arbol.insertar(fragmento)
    print(f"  Nodos: {arbol.tamano} | Altura del árbol: {arbol.altura()}")
    return arbol


def paso_verificacion(arbol):
    """Paso 5: recorre el árbol en inorden y verifica que el resultado esté ordenado.

    Parámetros:
        arbol (ArbolBST): árbol construido.

    Retorna:
        bool: True si el inorden está ordenado y completo; False (con aviso) si no.
    """
    print("\nPaso 5/6 - Verificación: recorrido inorden...")
    lista = arbol.inorden()
    print("  Inorden:", [f["codigo"] for f in lista])
    if esta_ordenada(lista) and len(lista) == arbol.tamano:
        print("  Verificación correcta: la lista está ordenada.")
        return True
    print("  ERROR: el recorrido inorden NO está ordenado; el árbol es incorrecto.")
    return False


def leer_codigo_busqueda():
    """Pide un código de fragmento y lo convierte a número, repitiendo si es inválido.

    Retorna:
        int: la clave numérica ingresada (acepta "F03", "f3" o "3").
    """
    while True:
        texto = leer_texto("Código del fragmento a consultar (ej. F03): ")
        try:
            return codigo_numerico(texto)
        except ValueError:
            print("  Código inválido: escribe una F seguida de un número (ej. F03).")


def paso_consulta(arbol, fragmentos):
    """Paso 6: busca fragmentos por código y compara árbol vs. búsqueda secuencial.

    Parámetros:
        arbol (ArbolBST): árbol construido.
        fragmentos (list[dict]): lista depurada, usada para la búsqueda secuencial.

    Retorna:
        tuple[bool, int]: (si encontró un fragmento, intentos usados).
    """
    print("\nPaso 6/6 - Consulta: árbol vs. búsqueda secuencial")
    intentos = 0
    while intentos < MAX_INTENTOS:
        clave = leer_codigo_busqueda()
        intentos += 1
        fragmento, comp_arbol = arbol.buscar_con_conteo(clave)
        _, comp_lista = buscar_secuencial_con_conteo(fragmentos, clave)
        print(f"  Comparaciones en el árbol: {comp_arbol} | "
              f"en la lista (secuencial): {comp_lista}")
        if fragmento is not None:
            print(f"  Encontrado: {fragmento['codigo']} - {fragmento['titulo']} "
                  f"(sala {fragmento['sala']}, valor {fragmento['valor']})")
            return True, intentos
        print(f"  El código no está en el catálogo. Intentos: {intentos}/{MAX_INTENTOS}")
    return False, intentos


def calcular_puntaje(num_validos, intentos):
    """Calcula el puntaje de la reconstrucción.

    Suma 10 puntos por fragmento válido y resta 5 por cada intento de consulta
    adicional al primero. Nunca es negativo.

    Parámetros:
        num_validos (int): fragmentos válidos recuperados.
        intentos (int): intentos usados en la consulta.

    Retorna:
        float: puntaje base (antes del multiplicador de dificultad).
    """
    puntos = (PUNTOS_POR_FRAGMENTO * num_validos
              - PENALIZACION_POR_INTENTO * max(0, intentos - 1))
    return float(max(0, puntos))


def reconstruir_catalogo(estado):
    """Ejecuta los 6 pasos de la reconstrucción del catálogo.

    Parámetros:
        estado (dict): estado de la partida (jugador e inventario).

    Retorna:
        bool: True si la reconstrucción se completó; False si debe reintentarse.
    """
    j = estado["jugador"]
    fragmentos = paso_carga()
    if fragmentos is None:
        print("El Guardián del Silo Azul no encuentra los fragmentos guardados.")
        return False
    paso_depuracion(fragmentos)
    estado["inventario"][:] = fragmentos
    validos, ubicaciones = paso_ubicacion(fragmentos)
    if not validos:
        print("  No hay fragmentos válidos para reconstruir el catálogo.")
        return False
    arbol = paso_construccion(validos, ubicaciones)
    if not paso_verificacion(arbol):
        perder_vida(j, 10)
        return False
    encontrado, intentos = paso_consulta(arbol, fragmentos)
    if not encontrado:
        perder_vida(j, 10)
        return False
    puntos = calcular_puntaje(len(validos), intentos)
    sumar_puntos(j, puntos)
    print(f"\nFragmentos válidos: {len(validos)} | Intentos: {intentos} "
          f"| Puntos base: {puntos:.0f}")
    hacer_pregunta(j, "central")
    return True
