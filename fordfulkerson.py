from Queue import Queue
import numpy as np

def bfs(rGraph, V, s, t, parent):
    q = Queue()
    visited = np.zeros(V, dtype=bool)
    q.put(s)
    visited[s] = True
    parent[s]  = -1

    while not q.empty():
        u = q.get()
        for v in xrange(V):
            if (not visited[v]) and rGraph[u][v] > 0:
                q.put(v)
                parent[v] = u
                visited[v] = True
    return visited[v]

def dfs(rGraph, V, s, visited):
    # visited[s] = True
    # for i in xrange(V):
    #     if rGraph[s][i] and not visited[i]:
    #         dfs(rGraph, V, i, visited)

    stack = [s]
    while stack:
        v = stack.pop()
        if not visited[v]:
            visited[v] = True
            stack.extend([u for u in xrange(V) if rGraph[v][u]])



def fordFulkerson(graph, s, t):
    print "running ford fulkerson"
    rGraph = graph.copy()
    V = len(graph)
    parent = np.zeros(V, dtype='int32')
    print "kickstarting while loop"

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

    cut = []

    for i in xrange(V):
        for j in xrange(V):
            if visited[i] and not visited[j] and graph[i][j]:
                cut.append((i, j))
    return cut
