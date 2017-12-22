from Queue import Queue
import numpy as np
import sys

def preFlows(C, F, heights, eflows, s):
    # vertices[s,0] = len(vertices)
    heights[s] = len(heights)
    # Height of the source vertex is equal to the total # of vertices

    # edges[s,:,1] = edges[s,:,0]
    F[s,:] = C[s,:]
    # Flow of edges from source is equal to their respective capacities


    for v in xrange(len(C)):
        # For every vertex v that has an incoming edge from s
        if C[s,v] > 0: 
            eflows[v] += C[s,v]
            # Initialize excess flow for v
            C[v,s] = 0
            F[v,s] = -C[s,v]
            # Set capacity of edge from v to s in residual graph to 0

# Returns the first vertex that is not the source and not the sink and 
# has a nonzero excess flow
# If non exists return None
def overFlowVertex(vertices, s, t):
    for v in xrange(len(vertices)):
        if v != s and v != t and vertices[v,1] > 0 :
            return v
    return None

# For a vertex v adjacent to u, we can push if:
#   (1) the flow of the edge u -> v is less than its capacity
#   (2) height of u > height of v
# Flow is the minimum of the remaining possible flow on this edge 
# and the excess flow of u
def push(edges, vertices, u):  
    for v in xrange(len(edges[u])):
        if edges[u,v,1] != edges[u,v,0]:
            if vertices[u,0] > vertices[v,0]:
                flow = min(edges[u,v,0] - edges[u,v,1], vertices[u,1])
                # print "pushing flow", flow, "from", u, "to", v
                vertices[u,1] -= flow  
                vertices[v,1] += flow 
                edges[u,v,1]  += flow  
                edges[v,u,1]  -= flow

                return True

    return False

# For a vertex v adjacent to u, we can relabel if
#   (1) the flow of the edge u -> v is less than its capacity
#   (2) the height of v is less than the minimum height
def relabel(edges, vertices, u):
    mh = float("inf") # Minimum height
    for v in xrange(len(edges[u])):
        if edges[u,v,1] != edges[u,v,0] and vertices[v,0] < mh:
            mh = vertices[v,0]
    vertices[u,0] = mh + 1
    # print "relabeling", u, "with mh", mh + 1

def dfs(rGraph, V, s, visited):

    stack = [s]
    while stack:
        v = stack.pop()
        if not visited[v]:
            visited[v] = True
            stack.extend([u for u in xrange(V) if rGraph[v][u] > 0])



def pushRelabel(C, s, t):
    print "Running push relabel algorithm"
    def preFlows():
        heights[s] = V
        F[s,:] = C[s,:]
        for v in xrange(V):
            if C[s,v] > 0: 
                excess[v] = C[s,v]
                excess[s] -= C[s,v]
                # C[v,s] = 0
                F[v,s] = -C[s,v]
    def overFlowVertex():
        for v in xrange(V):
            if v != s and v != t and excess[v] > 0:
                return v
        return None
    def push(u):
        # assert(excess[u] > 0)
        for v in xrange(V):
            if C[u,v] > F[u,v] and heights[u] == heights[v] + 1:
                flow = min(C[u,v] - F[u,v], excess[u])
                if C[u,v] > 0:
                    F[u,v] += flow
                else:
                    F[v,u] -= flow
                excess[u] -= flow 
                excess[v] += flow 
                # F[u,v] += flow  
                # F[v,u] -= flow
                return True
        return False
    def relabel(u):
        # assert(excess[u] > 0)
        # print heights, u
        # assert([heights[u] <= heights[v] for v in xrange(V) if C[u,v] > F[u,v]])
        heights[u] = min([heights[v] for v in xrange(V) if C[u,v] > F[u,v]]) + 1



    V = len(C)
    F = np.zeros((V, V))
    heights = np.zeros(V)
    excess = np.zeros(V)


    preFlows()

    while True:
        u = overFlowVertex()
        # print "overflowing vertex is", u
        if u == None: break
        if not push(u):
            relabel(u)
    # Max flow is equal to the excess flow of the sink
    #return vertices[t,1]
    print "Max flow", excess[t]
    # print C
    # print F
    # print C-F
    # print heights
    # print excess



    visited = np.zeros(V, dtype=bool)
    dfs(C - F, V, s, visited)

    cuts = []


    for u in xrange(V):
        for v in xrange(V):
            if visited[u] and not visited[v] and C[u,v]:
                cuts.append((u, v))
    return cuts

if __name__ == "__main__":

    # graph = [[0, 16, 13, 0, 0, 0],
    #          [0, 0, 10, 12, 0, 0],
    #          [0, 4, 0, 0, 14, 0],
    #          [0, 0, 9, 0, 0, 20],
    #          [0, 0, 0, 7, 0, 4],
    #          [0, 0, 0, 0, 0, 0]]

    graph = [[0, 4, 0, 5, 1, 0, 0],
             [4, 0, 4, 0, 10, 0, 0],
             [0, 4, 0, 0, 0, 10, 6],
             [5, 0, 0, 0, 5, 0, 0],
             [1, 0, 0, 5, 0, 5, 0],
             [0, 0, 10, 0, 5, 0, 4],
             [0, 0, 6, 0, 0, 4, 0]]

    print pushRelabel(np.asarray(graph), 0, 6)
