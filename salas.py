
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
MOVIMIENTOS = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
PISTAS_CORRECTAS = {"azul", "roble", "norte"}


def otorgar_fragmento(estado, codigo):
    fragmento = dict(CATALOGO[codigo])
    insertar(estado["inventario"], fragmento)
    sumar_puntos(estado["jugador"], fragmento["valor"])
    print(f"  Fragmento obtenido: {fragmento['titulo']} (valor {fragmento['valor']})")


def sala_vestibulo(estado):
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


def sala_estanterias(estado):
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



def mover(pos, direccion):
    fila, col = pos                       
    df, dc = MOVIMIENTOS[direccion]       
    nueva = (fila + df, col + dc)            
    fmin, fmax, cmin, cmax = LIMITES
    if fmin <= nueva[0] <= fmax and cmin <= nueva[1] <= cmax:
        return nueva
    print("  Un muro bloquea el paso.")
    return pos


def recorrer(ruta):
    for fila, col in ruta:                   
        print(f"  Pasaste por ({fila}, {col})")


def sala_mapas(estado):
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


def consultar(catalogo, codigo):
    try:
        return catalogo[codigo]
    except KeyError:
        print(f"  La ficha {codigo} no existe en el catálogo.")
        return None


def sala_fichas(estado):
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


def sala_sellos(estado):
    j = estado["jugador"]
    print("\n=== SALA DE SELLOS ===")
    print("El Guardián del Silo Azul susurra: «Pista: el silo es de color azul».")
    print("Escribe tus pistas separadas por comas (se requieren al menos 2 correctas).")
    entradas = [p.strip().lower() for p in leer_texto("Pistas: ").split(",") if p.strip()]
    pistas = set(entradas)                          
    print(f"  Duplicados descartados: {len(entradas) - len(pistas)}")
    validas = pistas & PISTAS_CORRECTAS           
    faltantes = PISTAS_CORRECTAS - pistas        
    todas = pistas | PISTAS_CORRECTAS              
    print(f"  Válidas: {sorted(validas)} | Faltantes: {len(faltantes)} | Total conocido: {len(todas)}")
    if len(validas) < 2:
        perder_vida(j, 15)
        return False
    otorgar_fragmento(estado, "F05")
    print(f"  Fragmentos repetidos eliminados: {eliminar_duplicados(estado['inventario'])}")
    hacer_pregunta(j, "sellos")
    return True


def sala_central(estado):
    j = estado["jugador"]
    print("\n=== SALA CENTRAL ===")
    codigos = {f["codigo"] for f in estado["inventario"]}
    if codigos != set(CATALOGO):
        print("El Guardián del Silo Azul niega con la cabeza: aún faltan fragmentos.")
        return False
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
    return True
