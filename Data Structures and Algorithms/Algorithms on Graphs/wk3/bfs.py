import sys
from collections import deque

sys.setrecursionlimit(200000)

class Vertice():
    def __init__(self,id):
        self.id = id
        self.pre = None
        self.post = None
        self.adj = []
        self.dist = None
        self.prev = None

class Graph():
    def __init__(self,n_of_vertices = 0):
        self.vertices = [Vertice(i) for i in range(n_of_vertices)]
        self.vertices_RevAdj = None

    def _init_reverse_copy(self):
            self.vertices_RevAdj = [[] for _ in range(len(self.vertices))]
            for v in self.vertices:
                for w in v.adj:
                    self.vertices_RevAdj[w].append(v.id)

    def reverse(self):
        if not self.vertices_RevAdj:
            self._init_reverse_copy()
        for i in range(len(self.vertices)):
            self.vertices[i].adj, self.vertices_RevAdj[i] = self.vertices_RevAdj[i], self.vertices[i].adj

    def load(self,data,directed = True):
        for v,w in zip(data[::2],data[1::2]):
            self.vertices[v-1].adj.append(w-1)
            if not directed:
                self.vertices[w-1].adj.append(v-1)

    def _explore_init(self):
        self.explore_order = 0
        self.explored = set()

    def explore(self,v,update_order=False):
        if update_order:
            self.explore_order += 1
            v.pre = self.explore_order
        self.explored.add(v.id)
        for w in v.adj:
            if w not in self.explored:
                self.explore(self.vertices[w],update_order)
        if update_order:
            self.explore_order += 1
            v.post = self.explore_order
        return 0

    def dfs(self):
        self.n_of_cc = 0 #number_of_connected_components
        self._explore_init()
        for v in self.vertices:
            if v.id not in self.explored:
                self.n_of_cc += 1
                self.explore(v,update_order=True)

    def bfs(self, src):
        dist = [None for _ in range(len(self.vertices))]
        prev = dist[:] 
        dist[src] = 0
        q = deque([src])
        while q:
            v = self.vertices[q.popleft()]
            for w in v.adj:
                if not dist[w]:
                    q.append(w)
                    dist[w] = dist[v.id] + 1
                    prev[w] = v
        return dist

    def distance(self, src, dst):
        dist = self.bfs(src)[dst]
        if dist:
            return dist
        else:
            return -1


    def _acyclic_explore(self,v):
        self.explored.add(v.id)
        self.cycle.add(v.id)
        for w in v.adj:
            if w in self.cycle:
                return False
            if w not in self.explored:
                if not self._acyclic_explore(self.vertices[w]):
                    return False
        self.cycle.discard(v.id)
        return True

    def is_acyclic(self):
        self._explore_init()
        self.cycle = set()
        for v in self.vertices:
            if v.id not in self.explored:
                if not self._acyclic_explore(v):
                    return False
        return True

    def toposorted_list(self):
        return [v for v in sorted(self.vertices,key=lambda x: x.post,reverse=True)]

    def n_of_scc(self): #number_of_strongly_connected_components
        self.reverse()
        self.dfs()
        self.reverse()
        self._explore_init()
        scc_number = 0
        for v in self.toposorted_list():
            if v.id not in self.explored:
                self.explore(v)
                scc_number += 1
        return scc_number


if __name__ == '__main__':
    data = list(map(int,sys.stdin.read().split()))
    #n, data = data[0], data[2:]
    n, data, s, d = data[0], data[2:-2], data[-2]-1, data[-1]-1
    g = Graph(n)
    #g.load(data)
    g.load(data,directed = False)
    #for v in g.vertices:
    #    print(f'{v.id}: ({v.pre}/{v.post}), adj: {v.adj}')
    print(g.distance(s,d))

    


    
