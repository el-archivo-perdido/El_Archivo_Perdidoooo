<<<<<<< HEAD
"""Una función por sala. Cada una recibe `estado` y devuelve True si se superó."""
from catalogo import CATALOGO
from entrada import leer_texto, leer_entero, leer_opcion
from inventario import insertar, eliminar, buscar, ordenar, titulos_valiosos
from jugador import crear_jugador, sumar_puntos, perder_vida, mostrar_estado
from persistencia import guardar_fragmentos
from preguntas import hacer_pregunta
from reconstruccion import reconstruir_catalogo

ORIGEN = (41, 27)
FRAGMENTO_POS = (43, 29)
LIMITES = (38, 44, 24, 30)          # fila_min, fila_max, col_min, col_max
=======

from arbol import ArbolBST
from catalogo import CATALOGO
from entrada import leer_texto, leer_entero, leer_opcion
from inventario import (insertar, eliminar, buscar, ordenar,
                        eliminar_duplicados, titulos_valiosos)
from jugador import crear_jugador, sumar_puntos, perder_vida, mostrar_estado
from preguntas import hacer_pregunta

ORIGEN = (41, 27)
FRAGMENTO_POS = (43, 29)
LIMITES = (38, 44, 24, 30)     
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
MOVIMIENTOS = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
PISTAS_CORRECTAS = {"azul", "roble", "norte"}


<<<<<<< HEAD
def otorgar_fragmento(estado, codigo, valioso=True):
    """Agrega un fragmento del catálogo al inventario y lo guarda en el archivo.

    Parámetros:
        estado (dict): estado de la partida.
        codigo (str): código del fragmento en CATALOGO (por ejemplo "F02").
        valioso (bool): si es True suma su valor al puntaje; si es False (copia
            repetida) solo se agrega al inventario.

    Retorna:
        None.
    """
    fragmento = dict(CATALOGO[codigo])
    insertar(estado["inventario"], fragmento)
    if valioso:
        sumar_puntos(estado["jugador"], fragmento["valor"])
        print(f"  Fragmento obtenido: {fragmento['titulo']} (valor {fragmento['valor']})")
    else:
        print(f"  Encuentras una copia de «{fragmento['titulo']}».")
    guardar_fragmentos(estado["inventario"])


# ---------------------------------------------------------------- Vestíbulo
def sala_vestibulo(estado):
    """Vestíbulo: registra al jugador (int, float, str, bool) y entrega el fragmento F01.

    Parámetros:
        estado (dict): estado de la partida (se crea el jugador).

    Retorna:
        bool: True siempre (la sala no se puede perder).
    """
=======
def otorgar_fragmento(estado, codigo):
    fragmento = dict(CATALOGO[codigo])
    insertar(estado["inventario"], fragmento)
    sumar_puntos(estado["jugador"], fragmento["valor"])
    print(f"  Fragmento obtenido: {fragmento['titulo']} (valor {fragmento['valor']})")


def sala_vestibulo(estado):
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    print("\n=== VESTÍBULO ===")
    print("El Guardián del Silo Azul te recibe con una linterna: "
          "«El catálogo fue destruido. Solo tú puedes reconstruirlo».")
    nombre = leer_texto("¿Cómo te llamas, explorador? ")
    dificultad = leer_entero("Dificultad (1=fácil, 2=media, 3=difícil): ", 1, 3)
    estado["jugador"] = crear_jugador(nombre, dificultad)
    mostrar_estado(estado["jugador"])
    otorgar_fragmento(estado, "F01")
    hacer_pregunta(estado["jugador"], "vestibulo")
    return True


<<<<<<< HEAD
# ------------------------------------------------------------- Estanterías
def sala_estanterias(estado):
    """Sala de Estanterías: encontrar el libro intruso (operaciones de lista).

    Parámetros:
        estado (dict): estado de la partida.

    Retorna:
        bool: True si el jugador identifica el intruso; False si falla 3 veces o muere.
    """
=======
def sala_estanterias(estado):
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    j = estado["jugador"]
    print("\n=== SALA DE ESTANTERÍAS ===")
    print("Hay un libro intruso entre los fragmentos del estante.")
    estante = [dict(CATALOGO["F05"]),
               {"codigo": "X99", "titulo": "Libro intruso", "sala": "?", "valor": 0},
               dict(CATALOGO["F02"]), dict(CATALOGO["F03"])]
    for f in estante:
        print(f"  {f['codigo']} - {f['titulo']}")

    for intentos in range(3, 0, -1):
        codigo = leer_texto(f"Código del intruso ({intentos} intentos): ").upper()
        if buscar(estante, codigo) is None:
            print("  Ese código no está en el estante.")
            perder_vida(j, 5)
        elif codigo != "X99":
            print("  Ese libro es legítimo.")
            perder_vida(j, 10)
        else:
            eliminar(estante, codigo)
            ordenar(estante)
            print("  Intruso eliminado. Estante ordenado:", [f["codigo"] for f in estante])
            print("  Libros valiosos:", titulos_valiosos(estante))
            otorgar_fragmento(estado, "F02")
            hacer_pregunta(j, "estanterias")
            return True
        if not j["activo"]:
            break
    return False


<<<<<<< HEAD
# -------------------------------------------------------------------- Mapas
def mover(pos, direccion):
    """Calcula la nueva posición tras un movimiento, respetando los muros.

    Parámetros:
        pos (tuple[int, int]): posición actual (fila, columna).
        direccion (str): "w", "a", "s" o "d".

    Retorna:
        tuple[int, int]: la nueva posición, o la misma si hay un muro.
    """
    fila, col = pos                           # desempaquetado
    df, dc = MOVIMIENTOS[direccion]           # desempaquetado
    nueva = (fila + df, col + dc)             # tupla nueva (inmutable)
=======

def mover(pos, direccion):
    fila, col = pos                       
    df, dc = MOVIMIENTOS[direccion]       
    nueva = (fila + df, col + dc)            
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    fmin, fmax, cmin, cmax = LIMITES
    if fmin <= nueva[0] <= fmax and cmin <= nueva[1] <= cmax:
        return nueva
    print("  Un muro bloquea el paso.")
    return pos


def recorrer(ruta):
<<<<<<< HEAD
    """Imprime las posiciones de una ruta, desempaquetando cada tupla.

    Parámetros:
        ruta (list[tuple[int, int]]): posiciones (fila, columna) visitadas.

    Retorna:
        None.
    """
    for fila, col in ruta:                    # desempaquetado en el recorrido
=======
    for fila, col in ruta:                   
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
        print(f"  Pasaste por ({fila}, {col})")


def sala_mapas(estado):
<<<<<<< HEAD
    """Sala de Mapas: llegar a la posición del fragmento con a lo sumo 12 movimientos.

    Parámetros:
        estado (dict): estado de la partida.

    Retorna:
        bool: True si llega al fragmento; False si se queda sin movimientos.
    """
=======
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    j = estado["jugador"]
    print("\n=== SALA DE MAPAS ===")
    print("Un fragmento está 2 filas abajo y 2 columnas a la derecha. Usa w/a/s/d.")
    pos = ORIGEN
    ruta = [pos]
    movimientos = 0
    while movimientos < 12 and pos != FRAGMENTO_POS:
        print(f"Estás en {pos}.")
        pos = mover(pos, leer_opcion("Mover (w/a/s/d): ", set(MOVIMIENTOS)))
        ruta.append(pos)
        movimientos += 1
    recorrer(ruta)
    if pos == FRAGMENTO_POS:
        otorgar_fragmento(estado, "F03")
        hacer_pregunta(j, "mapas")
        return True
    print("  Te quedaste sin movimientos.")
    perder_vida(j, 20)
    return False


<<<<<<< HEAD
# ------------------------------------------------------------------- Fichas
def consultar(catalogo, codigo):
    """Consulta una ficha por clave, manejando claves inexistentes.

    Parámetros:
        catalogo (dict): diccionario {código: fragmento}.
        codigo (str): código a consultar.

    Retorna:
        dict | None: la ficha, o None (con aviso) si la clave no existe.
    """
=======
def consultar(catalogo, codigo):
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    try:
        return catalogo[codigo]
    except KeyError:
        print(f"  La ficha {codigo} no existe en el catálogo.")
        return None


def sala_fichas(estado):
<<<<<<< HEAD
    """Sala de Fichas: hallar la ficha de «Diccionario de Claves» con 4 consultas.

    Parámetros:
        estado (dict): estado de la partida.

    Retorna:
        bool: True si la encuentra; False si agota las consultas o muere.
    """
=======
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    j = estado["jugador"]
    print("\n=== SALA DE FICHAS ===")
    print("Busca la ficha del libro «Diccionario de Claves» (códigos F01 a F05).")
    for _ in range(4):
        codigo = leer_texto("Código de ficha: ").upper()
        ficha = consultar(CATALOGO, codigo)
        if ficha is None:
            perder_vida(j, 5)
        else:
            print(f"  {ficha['codigo']}: {ficha['titulo']} | sala {ficha['sala']} | valor {ficha['valor']}")
            if ficha["titulo"] == "Diccionario de Claves":
                otorgar_fragmento(estado, "F04")
                hacer_pregunta(j, "fichas")
                return True
        if not j["activo"]:
            break
    return False


<<<<<<< HEAD
# ------------------------------------------------------------------- Sellos
def sala_sellos(estado):
    """Sala de Sellos: validar pistas con operaciones de conjuntos.

    Entre los sellos aparece además una copia repetida del fragmento F02, que se
    depurará en la Sala Central (Paso 2 de la actividad clave).

    Parámetros:
        estado (dict): estado de la partida.

    Retorna:
        bool: True si hay al menos 2 pistas correctas; False en caso contrario.
    """
=======
def sala_sellos(estado):
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    j = estado["jugador"]
    print("\n=== SALA DE SELLOS ===")
    print("El Guardián del Silo Azul susurra: «Pista: el silo es de color azul».")
    print("Escribe tus pistas separadas por comas (se requieren al menos 2 correctas).")
    entradas = [p.strip().lower() for p in leer_texto("Pistas: ").split(",") if p.strip()]
<<<<<<< HEAD
    pistas = set(entradas)                           # elimina duplicados
    print(f"  Duplicados descartados: {len(entradas) - len(pistas)}")
    validas = pistas & PISTAS_CORRECTAS              # intersección
    faltantes = PISTAS_CORRECTAS - pistas            # diferencia
    todas = pistas | PISTAS_CORRECTAS                # unión
=======
    pistas = set(entradas)                          
    print(f"  Duplicados descartados: {len(entradas) - len(pistas)}")
    validas = pistas & PISTAS_CORRECTAS           
    faltantes = PISTAS_CORRECTAS - pistas        
    todas = pistas | PISTAS_CORRECTAS              
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    print(f"  Válidas: {sorted(validas)} | Faltantes: {len(faltantes)} | Total conocido: {len(todas)}")
    if len(validas) < 2:
        perder_vida(j, 15)
        return False
    otorgar_fragmento(estado, "F05")
<<<<<<< HEAD
    otorgar_fragmento(estado, "F02", valioso=False)   # copia repetida
=======
    print(f"  Fragmentos repetidos eliminados: {eliminar_duplicados(estado['inventario'])}")
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    hacer_pregunta(j, "sellos")
    return True


<<<<<<< HEAD
# ------------------------------------------------------------------ Central
def sala_central(estado):
    """Sala Central: reconstruye el catálogo (actividad clave de 6 pasos).

    Parámetros:
        estado (dict): estado de la partida.

    Retorna:
        bool: True si se reconstruyó el catálogo; False si faltan fragmentos o falla algún paso.
    """
=======
def sala_central(estado):
    j = estado["jugador"]
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    print("\n=== SALA CENTRAL ===")
    codigos = {f["codigo"] for f in estado["inventario"]}
    if codigos != set(CATALOGO):
        print("El Guardián del Silo Azul niega con la cabeza: aún faltan fragmentos.")
        return False
<<<<<<< HEAD
    print("El Guardián del Silo Azul extiende los fragmentos sobre la mesa central.")
    if not reconstruir_catalogo(estado):
        return False
    print("El Guardián del Silo Azul asiente: «Mereces restaurar el archivo».")
=======
    arbol = ArbolBST()
    for fragmento in estado["inventario"]:
        arbol.insertar(fragmento)
    print("Catálogo reconstruido (recorrido inorden):")
    for f in arbol.inorden():
        print(f"  {f['codigo']} - {f['titulo']}")
    codigo = leer_texto("Busca un código en el árbol: ").upper()
    encontrado = arbol.buscar(codigo)
    print(f"  Resultado: {encontrado['titulo']}" if encontrado else "  No está en el árbol.")
    sumar_puntos(j, 50)
    print("El Guardián del Silo Azul asiente: «Mereces restaurar el archivo».")
    hacer_pregunta(j, "central")
>>>>>>> fd438b1ddaf45f035dc5cff6c664c70967472097
    return True
