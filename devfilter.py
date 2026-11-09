
from collections import deque
from heapq import heappush, heappop
from itertools import count
from math import ceil
from time import perf_counter_ns
from statistics import median
import csv

SCORES = (2, 3, 1, 4, 2, 5, 3, 1, 9, 8, 10, 9, 7, 8, 6, 10)
K, TARGET = 4, 36

def utility(state):
    return sum(SCORES[i] for i in state)

def goal(state):
    return len(state) == K and utility(state) >= TARGET

def successors(state):
    """Índices crecientes: cada subconjunto tiene exactamente un camino."""
    if len(state) >= K:
        return
    start = state[-1] + 1 if state else 0
    for i in range(start, len(SCORES)):
        if len(SCORES) - i - 1 >= K - len(state) - 1:
            yield state + (i,)

def heuristic(state):
    """Cota inferior: cupos faltantes y déficit dividido por máximo global."""
    return max(K - len(state), ceil(max(0, TARGET - utility(state))/max(SCORES)))

def search(kind):
    """Cuenta expansión solo cuando se generan sucesores; excluye la meta.
    DFS visita primero los índices menores. A* desempata por mayor g,
    después por orden de inserción. No almacena caminos duplicados.
    """
    expanded, peak = 0, 1
    serial = count()
    if kind == 'A*':
        frontier = [(heuristic(()), 0, next(serial), ())]
    else:
        frontier = deque([()])
    while frontier:
        if kind == 'A*':
            _, _, _, state = heappop(frontier)
        elif kind == 'BFS':
            state = frontier.popleft()
        elif kind == 'DFS':
            state = frontier.pop()
        else:
            raise ValueError(kind)
        if goal(state):
            return dict(algorithm=kind, expanded=expanded, cost=len(state),
                        utility=utility(state), selected=state, frontier_peak=peak)
        expanded += 1
        children = list(successors(state))
        if kind == 'A*':
            for child in children:
                g = len(child)
                heappush(frontier, (g + heuristic(child), -g, next(serial), child))
        else:
            frontier.extend(reversed(children) if kind == 'DFS' else children)
        peak = max(peak, len(frontier))
    return dict(algorithm=kind, expanded=expanded, cost=None,
                utility=None, selected=(), frontier_peak=peak)

def benchmark(repeats=101):
    rows = []
    for kind in ('BFS', 'DFS', 'A*'):
        search(kind)
        times = []
        for _ in range(repeats):
            start = perf_counter_ns()
            result = search(kind)
            times.append((perf_counter_ns() - start)/1e6)
        result['median_ms'] = median(times)
        result['repetitions'] = repeats
        rows.append(result)
    return rows

def tests():
    """Verifica h frente al costo exacto a meta para TODOS los estados."""
    def visit(state):
        children = list(successors(state))
        distances = [visit(child) for child in children]
        exact = 0 if goal(state) else min((1+d for d in distances), default=float('inf'))
        assert heuristic(state) <= exact
        for child in children:
            assert heuristic(state) <= 1 + heuristic(child)
        if goal(state):
            assert heuristic(state) == 0
        return exact
    assert visit(()) == K
    rows = [search(kind) for kind in ('BFS', 'DFS', 'A*')]
    assert all(row['cost'] == K and row['utility'] >= TARGET for row in rows)
    return True

if __name__ == '__main__':
    tests()
    rows = benchmark()
    with open('benchmark.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(row)
