# DevFilter IA — Proyecto integrador, fase 2

Implementación y comparación de los algoritmos de búsqueda BFS, DFS y A* para una simulación de preselección de talento tecnológico.

## Integrante
- Carlos David Pinilla.

Universidad Militar Nueva Granada  
Asignatura: Inteligencia Artificial

## 1. Descripción del proyecto

DevFilter IA es una propuesta de agente inteligente para apoyar la preselección de aspirantes a vacantes de desarrollo web junior.

En la fase 1 se definieron el problema, el modelo PEAS, las características del entorno y la arquitectura del agente.

En esta fase se implementa un subproblema de búsqueda: encontrar una lista de cuatro candidatos ficticios cuya puntuación técnica acumulada sea de al menos 36 puntos.

La finalidad es comparar el esfuerzo computacional de BFS, DFS y A* cuando resuelven el mismo problema.

El programa no analiza hojas de vida reales, no aprende las puntuaciones y no toma decisiones de contratación.

## 2. Objetivos

- Representar el problema mediante un espacio de estados determinista y discreto.
- Implementar BFS, DFS y A* en Python.
- Formular una heurística admisible y consistente para A*.
- Comparar nodos expandidos, tiempo de ejecución y costo de la solución.
- Analizar el comportamiento de los algoritmos y sus limitaciones.

## 3. Archivos del proyecto

| Archivo | Contenido |
|---|---|
| `devfilter.py` | Modelo del problema, algoritmos, heurística, pruebas y benchmark. |
| `benchmark.csv` | Resultados de la ejecución del benchmark. |
| `README.md` | Descripción del proyecto e instrucciones de ejecución. |

El informe académico se entrega como documento PDF y puede incluirse también en el repositorio.

## 4. Requisitos

- Python 3.8 o posterior.
- Una terminal para ejecutar el programa.

No se requieren librerías externas. El programa utiliza únicamente módulos de la biblioteca estándar de Python.

## 5. Ejecución

### Paso 1. Descargar el proyecto

En la página principal del repositorio, seleccionar:

Code → Download ZIP

Extraer el archivo descargado.

También es posible descargar directamente `devfilter.py`.

### Paso 2. Abrir una terminal

Ubicarse en la carpeta que contiene `devfilter.py`.

### Paso 3. Ejecutar el programa

Según la instalación de Python, utilizar uno de los siguientes comandos:

```bash
python devfilter.py
```

```bash
python3 devfilter.py
```

En Windows también puede utilizarse:

```powershell
py devfilter.py
```

### Paso 4. Consultar los resultados

El programa:

1. Ejecuta las pruebas de la heurística y de las soluciones.
2. Realiza una ejecución de calentamiento por algoritmo.
3. Ejecuta 101 repeticiones de BFS, DFS y A*.
4. Muestra los resultados en la terminal.
5. Escribe `benchmark.csv` en la carpeta de ejecución.

Si el archivo `benchmark.csv` ya existe en esa carpeta, se reemplaza con los nuevos resultados.

## 6. Datos de la simulación

Se utilizan 16 candidatos ficticios con puntuaciones enteras:

| Candidato | Puntuación |
|---|---:|
| C01 | 2 |
| C02 | 3 |
| C03 | 1 |
| C04 | 4 |
| C05 | 2 |
| C06 | 5 |
| C07 | 3 |
| C08 | 1 |
| C09 | 9 |
| C10 | 8 |
| C11 | 10 |
| C12 | 9 |
| C13 | 7 |
| C14 | 8 |
| C15 | 6 |
| C16 | 10 |

Parámetros:

- Número de candidatos: `n = 16`.
- Tamaño de la preselección: `k = 4`.
- Umbral de puntuación: `T = 36`.
- Puntuación individual máxima: `M = 10`.

Todos los candidatos se presuponen elegibles respecto de los requisitos obligatorios.

Las puntuaciones son sintéticas. No representan una medida del valor profesional de una persona.

Los datos se diseñaron colocando puntuaciones altas hacia el final del orden de exploración. No corresponden a una muestra aleatoria.

## 7. Formalización del problema

### Estado

Una tupla de índices de candidatos seleccionados, ordenados de forma estrictamente creciente.

Ejemplo:

```python
(8, 9, 10)
```

Este estado representa a C09, C10 y C11, porque los índices del programa comienzan en cero.

### Estado inicial

```python
()
```

No se ha seleccionado ningún candidato.

### Acciones

Agregar un candidato cuyo índice sea mayor que el último seleccionado.

La acción se permite si:

- La lista tiene menos de cuatro integrantes.
- Quedan suficientes candidatos posteriores para completar la lista.

El orden creciente evita explorar diferentes permutaciones del mismo subconjunto.

### Modelo de transición

La transición concatena el índice del nuevo candidato con la tupla actual.

Ejemplo:

```text
Estado:       (8, 9)
Acción:       agregar 10
Nuevo estado: (8, 9, 10)
```

### Prueba de meta

Un estado es meta cuando:

```text
Cantidad de candidatos = 4
Puntuación acumulada >= 36
```

### Función de costo

Cada incorporación cuesta una unidad.

Por tanto:

```text
g(s) = cantidad de candidatos seleccionados
```

Todas las soluciones válidas tienen costo 4.

El programa encuentra una lista que cumple el umbral; no busca necesariamente la lista con mayor puntuación.

## 8. Algoritmos implementados

### BFS — Búsqueda en anchura

Utiliza una cola FIFO.

Explora los estados por niveles: primero las listas de un candidato, después las de dos y así sucesivamente.

### DFS — Búsqueda en profundidad

Utiliza una pila LIFO.

Explora una rama antes de continuar con otras alternativas.

Los sucesores se insertan en orden inverso para visitar primero los índices menores.

### A* — Búsqueda informada

Utiliza una cola de prioridad con:

```text
f(s) = g(s) + h(s)
```

Donde:

- `g(s)` es el costo acumulado.
- `h(s)` estima el costo restante.

En caso de empate, se prioriza el estado con mayor profundidad. Si el empate continúa, se utiliza el orden de inserción.

### Tratamiento de estados repetidos

No se utiliza un conjunto global de visitados.

En esta representación, cada subconjunto tiene un único padre: la misma tupla sin su último elemento. Por ello, no existen caminos duplicados hacia un mismo estado.

## 9. Heurística de A*

Se definen:

```text
r = k - cantidad de candidatos seleccionados
D = max(0, T - puntuación acumulada)
M = puntuación individual máxima
```

La heurística es:

```text
h(s) = max(r, techo(D / M))
```

La función `techo` redondea hacia arriba.

### Admisibilidad

Toda continuación exitosa necesita:

1. Incorporar los candidatos que faltan para completar los cuatro cupos.
2. Cubrir el déficit de puntuación.

Como un candidato aporta como máximo `M` puntos, cubrir el déficit requiere al menos `techo(D / M)` incorporaciones.

Ambas cantidades son cotas inferiores del costo restante. Su máximo también es una cota inferior.

Por tanto, la heurística no sobreestima el costo óptimo restante.

En estados sin solución, el costo restante se considera infinito.

### Consistencia

Cada incorporación:

- Reduce los cupos pendientes en uno.
- Reduce el déficit en una cantidad no mayor que `M`.

Por ello, la heurística puede disminuir como máximo una unidad por transición:

```text
h(s) <= 1 + h(siguiente)
```

En toda meta, `h(s) = 0`.

## 10. Pruebas de verificación

Antes del benchmark, el programa recorre exhaustivamente el árbol de la instancia y comprueba:

- Admisibilidad de la heurística frente al costo exacto restante.
- Consistencia en cada transición.
- Valor cero de la heurística en las metas.
- Existencia de una solución de costo 4.
- Cumplimiento de la meta por los tres algoritmos.

Si alguna comprobación falla, se produce un `AssertionError`.

## 11. Metodología del benchmark

Se utiliza `perf_counter_ns()` para medir la duración de cada búsqueda.

Procedimiento:

1. Una ejecución de calentamiento por algoritmo.
2. 101 repeticiones por algoritmo.
3. Conversión de nanosegundos a milisegundos.
4. Cálculo de la mediana.

La medición incluye únicamente la llamada a la función de búsqueda.

Excluye:

- Importaciones.
- Pruebas previas.
- Escritura del CSV.
- Impresión de resultados.

Los tres algoritmos utilizan el mismo estado inicial, acciones, transición, meta y costos.

## 12. Métricas registradas

| Campo del CSV | Significado |
|---|---|
| `algorithm` | Algoritmo utilizado. |
| `expanded` | Nodos expandidos. |
| `cost` | Costo de la solución. |
| `utility` | Puntuación acumulada de la lista encontrada. |
| `selected` | Índices de los candidatos seleccionados. |
| `frontier_peak` | Máximo número de entradas pendientes en la frontera. |
| `median_ms` | Mediana del tiempo de búsqueda en milisegundos. |
| `repetitions` | Número de repeticiones del benchmark. |

Un nodo expandido es un nodo no meta para el que se solicita generar sucesores, incluidas las hojas sin sucesores.

La meta se comprueba al extraer un nodo de la frontera. El nodo meta no se contabiliza como expandido.

La frontera máxima mide entradas pendientes, no bytes de memoria total.

## 13. Resultado de referencia

Con los datos y el orden de exploración suministrados:

| Algoritmo | Nodos expandidos | Costo | Puntuación | Frontera máxima |
|---|---:|---:|---:|---:|
| BFS | 2310 | 4 | 36 | 1820 |
| DFS | 2258 | 4 | 36 | 49 |
| A* | 4 | 4 | 36 | 25 |

Los tres algoritmos encuentran:

```text
C09, C10, C11 y C12
```

Puntuación:

```text
9 + 8 + 10 + 9 = 36
```

Representación interna:

```python
(8, 9, 10, 11)
```

Los tiempos medidos se consultan en `benchmark.csv`. Pueden cambiar según el equipo y las condiciones de ejecución.

Si se modifican los datos, el orden de sucesores o las reglas de desempate, también pueden cambiar los demás resultados.

## 14. Complejidad computacional

Se utilizan las siguientes variables:

- `b`: ramificación máxima.
- `d`: profundidad de la primera meta.
- `m`: profundidad máxima.
- `N`: número total de estados generados.
- `k`: tamaño máximo de una tupla.
- `n`: número de candidatos.

En esta instancia:

```text
b <= 16
d = m = k = 4
```

Bajo el supuesto de operaciones de nodo de costo constante:

| Algoritmo | Tiempo | Espacio |
|---|---|---|
| BFS | O(b^d), en este árbol limitado a profundidad d | O(b^d) |
| DFS | O(b^m) | O(bm), sin visitados globales |
| A* | Puede requerir exploración exponencial; el heap agrega un costo O(log N) por operación | O(N) entradas en el peor caso |

En el código, sumar puntuaciones y copiar tuplas introduce costos adicionales.

Las cotas conservadoras para la implementación son:

```text
BFS y DFS: O(Nk)
A*: O(N(k + n + log N))
```

El término `n` aparece porque `max(SCORES)` recorre las puntuaciones al evaluar la heurística.

La memoria ocupada por los índices de las tuplas pendientes es `O(kF)`, donde `F` es la frontera máxima.

## 15. Limitaciones

- Se evalúa una sola instancia sintética.
- Los candidatos de mayor puntuación aparecen tarde en el orden fijado.
- Todas las metas tienen profundidad cuatro.
- El experimento compara esfuerzo de búsqueda, no calidad profesional.
- DFS no garantiza soluciones de costo mínimo en problemas generales.
- La ventaja observada de A* depende de los datos, la heurística y el desempate.
- Encontrar una lista factible no demuestra equidad.
- El sistema no predice desempeño laboral ni reemplaza la revisión humana.

## 16. Referencias
Russell, S., & Norvig, P. (2020).
Artificial intelligence: A modern approach (4.ª ed.). Pearson.

Repositorio de referencia AIMA-Python:
https://github.com/aimacode/aima-python

La implementación de este proyecto es código propio. El repositorio AIMA se
incluye como referencia, no como repositorio de entrega.
