"""Pruebas: estructuras, persistencia y una partida completa con entradas simuladas.

Los archivos se redirigen a una carpeta temporal para no pisar los guardados reales.
"""
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import persistencia
import main
from arbol import ArbolBST, codigo_numerico, esta_ordenada
from catalogo import CATALOGO, UBICACIONES
from inventario import eliminar_duplicados, buscar_secuencial_con_conteo
from reconstruccion import calcular_puntaje


def frag(n):
    """Crea un fragmento mínimo con código F + n de 4 dígitos."""
    return {"codigo": f"F{n:04d}", "titulo": f"T{n}", "sala": "-", "valor": 1}


class BaseTemporal(unittest.TestCase):
    """Redirige las rutas de persistencia a una carpeta temporal."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = self.tmp.name
        self.patcher = patch.multiple(
            persistencia,
            RUTA_PARTIDA=os.path.join(d, "partida.json"),
            RUTA_PUNTAJES=os.path.join(d, "puntajes.json"),
            RUTA_FRAGMENTOS=os.path.join(d, "fragmentos.json"))
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.tmp.cleanup()


class TestArbol(unittest.TestCase):
    def test_codigo_numerico(self):
        self.assertEqual(codigo_numerico("F03"), 3)
        self.assertEqual(codigo_numerico("f3"), 3)
        self.assertEqual(codigo_numerico(7), 7)
        with self.assertRaises(ValueError):
            codigo_numerico("abc")

    def test_bst_inorden_ordenado(self):
        a = ArbolBST()
        for c in ["F03", "F01", "F05", "F02"]:
            a.insertar({"codigo": c})
        self.assertEqual([f["codigo"] for f in a.inorden()], ["F01", "F02", "F03", "F05"])
        self.assertTrue(esta_ordenada(a.inorden()))

    def test_clave_numerica_no_alfabetica(self):
        a = ArbolBST()
        for n in (10, 9, 100, 2):
            a.insertar(frag(n))
        self.assertEqual([codigo_numerico(f["codigo"]) for f in a.inorden()], [2, 9, 10, 100])

    def test_duplicado_ignorado(self):
        a = ArbolBST()
        self.assertTrue(a.insertar(frag(1)))
        self.assertFalse(a.insertar(frag(1)))
        self.assertEqual(a.tamano, 1)

    def test_busqueda_con_conteo(self):
        a = ArbolBST()
        for n in (4, 2, 6, 1, 3):
            a.insertar(frag(n))
        f, comps = a.buscar_con_conteo("F0003")
        self.assertEqual((f["codigo"], comps), ("F0003", 3))
        self.assertEqual(a.buscar_con_conteo("F0099")[0], None)

    def test_arbol_degenerado(self):
        a = ArbolBST()
        lista = [frag(n) for n in range(1, 301)]
        for f in lista:
            a.insertar(f)
        self.assertEqual(a.altura(), 300)
        self.assertEqual(a.buscar_con_conteo("F0300")[1], 300)
        self.assertEqual(buscar_secuencial_con_conteo(lista, "F0300")[1], 300)

    def test_ubicaciones_dan_arbol_balanceado(self):
        orden = sorted(CATALOGO.values(), key=lambda f: UBICACIONES[f["codigo"]])
        a = ArbolBST()
        for f in orden:
            a.insertar(f)
        self.assertEqual(a.altura(), 3)
        self.assertTrue(esta_ordenada(a.inorden()))


class TestListasYPuntaje(unittest.TestCase):
    def test_eliminar_duplicados(self):
        inv = [dict(CATALOGO["F01"]), dict(CATALOGO["F02"]), dict(CATALOGO["F01"])]
        self.assertEqual(eliminar_duplicados(inv), 1)
        self.assertEqual([f["codigo"] for f in inv], ["F01", "F02"])

    def test_calcular_puntaje(self):
        self.assertEqual(calcular_puntaje(5, 1), 50.0)
        self.assertEqual(calcular_puntaje(5, 3), 40.0)
        self.assertEqual(calcular_puntaje(0, 3), 0.0)


class TestPersistencia(BaseTemporal):
    def test_cargar_partida_inexistente(self):
        self.assertIsNone(persistencia.cargar_partida())

    def test_cargar_partida_json_no_diccionario(self):
        for contenido in ("[1, 2]", "5", "{roto"):
            with open(persistencia.RUTA_PARTIDA, "w", encoding="utf-8") as f:
                f.write(contenido)
            self.assertIsNone(persistencia.cargar_partida())

    def test_guardar_y_cargar_partida(self):
        estado = main.nuevo_estado()
        estado["jugador"] = {"nombre": "Ana", "vida": 100, "puntaje": 0.0,
                             "nivel": 1, "multiplicador": 1.0, "activo": True}
        persistencia.guardar_partida(estado)
        self.assertEqual(persistencia.cargar_partida(), estado)

    def test_fragmentos_ida_y_vuelta(self):
        fr = [dict(CATALOGO["F01"])]
        self.assertTrue(persistencia.guardar_fragmentos(fr))
        self.assertEqual(persistencia.cargar_fragmentos(), fr)

    def test_cargar_fragmentos_danado(self):
        self.assertIsNone(persistencia.cargar_fragmentos())
        with open(persistencia.RUTA_FRAGMENTOS, "w", encoding="utf-8") as f:
            json.dump([{"codigo": "F01"}], f)
        self.assertIsNone(persistencia.cargar_fragmentos())


class TestPartida(BaseTemporal):
    ENTRADAS = ["abc", "Ana", "x", "1", "2",
                "x99", "1",
                "s", "s", "d", "d", "2",
                "F09", "F04", "1",
                "azul, roble, roble", "3",
                "xyz", "F99", "F03", "1"]

    def test_partida_completa(self):
        entradas = iter(self.ENTRADAS)
        with patch("builtins.input", lambda _="": next(entradas)):
            estado = main.nuevo_estado()
            main.jugar(estado)
        self.assertEqual(estado["sala"], 6)
        self.assertEqual(len(estado["inventario"]), 5)
        self.assertEqual(len(persistencia.leer_puntajes()), 1)

    def test_partida_terminada_no_duplica_puntaje(self):
        entradas = iter(self.ENTRADAS)
        with patch("builtins.input", lambda _="": next(entradas)):
            estado = main.nuevo_estado()
            main.jugar(estado)
        main.jugar(estado)
        self.assertEqual(len(persistencia.leer_puntajes()), 1)


if __name__ == "__main__":
    unittest.main()
