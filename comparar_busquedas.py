"""Compara búsqueda en el BST vs. búsqueda secuencial para el informe técnico.

Uso:  python comparar_busquedas.py
Genera la tabla en pantalla y la guarda en datos/resultados_comparacion.md
"""
import os
import random

from arbol import ArbolBST
from inventario import buscar_secuencial_con_conteo

TAMANOS = (10, 100, 1000)
SEMILLA = 2026
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "datos", "resultados_comparacion.md")


def crear_fragmentos(n):
    """Crea n fragmentos sintéticos con códigos F0001, F0002, ...

    Parámetros:
        n (int): tamaño del catálogo.

    Retorna:
        list[dict]: fragmentos en orden ascendente de código.
    """
    return [{"codigo": f"F{i:04d}", "titulo": f"Fragmento {i}", "sala": "-", "valor": 10}
            for i in range(1, n + 1)]


def medir(fragmentos):
    """Inserta los fragmentos (en el orden dado) y busca cada uno en ambas estructuras.

    Parámetros:
        fragmentos (list[dict]): orden de inserción; también es el orden de la lista.

    Retorna:
        dict: altura, promedio y peor caso de comparaciones del árbol y de la lista.
    """
    arbol = ArbolBST()
    for f in fragmentos:
        arbol.insertar(f)
    cuentas_arbol, cuentas_lista = [], []
    for f in fragmentos:
        cuentas_arbol.append(arbol.buscar_con_conteo(f["codigo"])[1])
        cuentas_lista.append(buscar_secuencial_con_conteo(fragmentos, f["codigo"])[1])
    n = len(fragmentos)
    return {"n": n, "altura": arbol.altura(),
            "prom_arbol": sum(cuentas_arbol) / n, "peor_arbol": max(cuentas_arbol),
            "prom_lista": sum(cuentas_lista) / n, "peor_lista": max(cuentas_lista)}


def tabla(titulo, filas):
    """Formatea los resultados como tabla Markdown.

    Parámetros:
        titulo (str): título de la tabla.
        filas (list[dict]): resultados de `medir`.

    Retorna:
        str: tabla en formato Markdown.
    """
    lineas = [f"### {titulo}", "",
              "| Tamaño del catálogo | Altura del árbol | Prom. árbol | Peor árbol "
              "| Prom. secuencial | Peor secuencial |",
              "|---:|---:|---:|---:|---:|---:|"]
    for r in filas:
        lineas.append(f"| {r['n']} | {r['altura']} | {r['prom_arbol']:.1f} | {r['peor_arbol']} "
                      f"| {r['prom_lista']:.1f} | {r['peor_lista']} |")
    return "\n".join(lineas)


def main():
    """Ejecuta la comparación para inserciones aleatorias y ordenadas.

    Retorna:
        None (imprime la tabla y la guarda en un archivo).
    """
    aleatorio, ordenado = [], []
    for n in TAMANOS:
        fragmentos = crear_fragmentos(n)
        mezclados = fragmentos[:]
        random.Random(SEMILLA).shuffle(mezclados)
        aleatorio.append(medir(mezclados))
        ordenado.append(medir(fragmentos))
    texto = ("# Comparación de comparaciones: árbol vs. búsqueda secuencial\n\n"
             "Se buscó cada código del catálogo una vez y se promedió el número de "
             "comparaciones (un nodo visitado o un elemento examinado = 1 comparación).\n\n"
             + tabla("Inserción en orden aleatorio", aleatorio) + "\n\n"
             + tabla("Inserción en orden ascendente (árbol degenerado)", ordenado) + "\n")
    print(texto)
    try:
        os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"Resultados guardados en {SALIDA}")
    except OSError as e:
        print(f"No se pudo guardar el archivo de resultados: {e}")


if __name__ == "__main__":
    main()
