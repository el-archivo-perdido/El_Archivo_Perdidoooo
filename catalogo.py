"""Catálogo de fragmentos: cada fragmento es un diccionario."""

CATALOGO = {
    "F01": {"codigo": "F01", "titulo": "Códice de Variables",   "sala": "Vestíbulo",   "valor": 20},
    "F02": {"codigo": "F02", "titulo": "Tratado de Listas",     "sala": "Estanterías", "valor": 30},
    "F03": {"codigo": "F03", "titulo": "Atlas de Tuplas",       "sala": "Mapas",       "valor": 40},
    "F04": {"codigo": "F04", "titulo": "Diccionario de Claves", "sala": "Fichas",      "valor": 50},
    "F05": {"codigo": "F05", "titulo": "Libro de Conjuntos",    "sala": "Sellos",      "valor": 60},
}

UBICACIONES = {
    "F03": (1, 1),
    "F01": (1, 2),
    "F05": (1, 3),
    "F02": (2, 1),
    "F04": (2, 2),
}
