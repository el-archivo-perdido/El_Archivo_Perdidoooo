# Comparación de comparaciones: árbol vs. búsqueda secuencial

Se buscó cada código del catálogo una vez y se promedió el número de comparaciones (un nodo visitado o un elemento examinado = 1 comparación).

### Inserción en orden aleatorio

| Tamaño del catálogo | Altura del árbol | Prom. árbol | Peor árbol | Prom. secuencial | Peor secuencial |
|---:|---:|---:|---:|---:|---:|
| 10 | 6 | 3.6 | 6 | 5.5 | 10 |
| 100 | 12 | 7.2 | 12 | 50.5 | 100 |
| 1000 | 22 | 11.8 | 22 | 500.5 | 1000 |

### Inserción en orden ascendente (árbol degenerado)

| Tamaño del catálogo | Altura del árbol | Prom. árbol | Peor árbol | Prom. secuencial | Peor secuencial |
|---:|---:|---:|---:|---:|---:|
| 10 | 10 | 5.5 | 10 | 5.5 | 10 |
| 100 | 100 | 50.5 | 100 | 50.5 | 100 |
| 1000 | 1000 | 500.5 | 1000 | 500.5 | 1000 |
