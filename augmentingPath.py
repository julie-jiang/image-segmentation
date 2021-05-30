from queue import Queue
import numpy as np

def bfs(rGraph, V, s, t, parent):
    q = Queue()
    visited = np.zeros(V, dtype=bool)
    q.put(s)
    visited[s] = True
    parent[s]  = -1

    while not q.empty():
        u = q.get()
        for v in range(V):
            if (not visited[v]) and rGraph[u][v] > 0:
                q.put(v)
                parent[v] = u
                visited[v] = True
    return visited[v]

def dfs(rGraph, V, s, visited):
    stack = [s]
    while stack:
        v = stack.pop()
        if not visited[v]:
            visited[v] = True
            stack.extend([u for u in range(V) if rGraph[v][u]])



def augmentingPath(graph, s, t):
    print("Running augmenting path algorithm")
    rGraph = graph.copy()
    V = len(graph)
    parent = np.zeros(V, dtype='int32')

    while bfs(rGraph, V, s, t, parent):
        pathFlow = float("inf")
        v = t
        while v != s:
            u = parent[v]
            pathFlow = min(pathFlow, rGraph[u][v])
            v = parent[v]

        v = t
        while v != s:
            u = parent[v]
            rGraph[u][v] -= pathFlow
            rGraph[v][u] += pathFlow
            v = parent[v]

    visited = np.zeros(V, dtype=bool)
    dfs(rGraph, V, s, visited)

    cuts = []

    for i in range(V):
        for j in range(V):
            if visited[i] and not visited[j] and graph[i][j]:
                cuts.append((i, j))
    return cuts
