#Uses python3

import sys

class vertice():
    def __init__(self,id):
        self.id = id
        self.visited = False
        self.edges = []
    def __repr__(self):
        return str(self.id)

def reach(v,dst,V):
    V[v].visited = True
    if v == dst:
        return 1
    for w in V[v].edges:
        if V[w].visited == False:
            if reach(w,dst,V) == 1:
                return 1
    return 0


if __name__ == '__main__':
    n, m = map(int, sys.stdin.readline().split())
    V = {}
    for i in range(m):
        v, w =  map(int, sys.stdin.readline().split())
        if v not in V.keys(): V[v] = vertice(v)
        if w not in V.keys(): V[w] = vertice(w)
        V[v].edges.append(w)
        V[w].edges.append(v)
    x, y = map(int, sys.stdin.readline().split())
    #print(V)
    #for v in V.values():
    #    print(v.id,v.edges)
    #print(x,y)

    print(reach(x, y, V))
