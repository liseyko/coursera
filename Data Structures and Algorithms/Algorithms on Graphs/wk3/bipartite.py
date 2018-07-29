import sys
from collections import deque

sys.setrecursionlimit(200000)

class Vertice():
    def __init__(self,id):
        self.id = id
        self.data = None
        self.pre = None
        self.post = None
        self.adj = []
        self.dist = None
        self.prev = None

class Graph():
    def __init__(self,n_of_vertices = 0):
        self.vertices = [Vertice(i) for i in range(n_of_vertices)]
        self.vertices_RevAdj = None
        self.directed = True

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
        self.directed = directed
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
                    prev[w] = v.id
        return dist,prev

    def distance(self, src, dst):
        dist = self.bfs(src)[0][dst]
        if dist:
            return dist
        else:
            return -1

    def path(self, src, dst):
        prev = self.bfs(src)[1]
        print(prev)
        q = deque([dst])
        while dst != src:
            dst = prev[dst]
            q.appendleft(dst)
        return list(q)
        

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

    def is_bipartite(self):
        if self.directed:
            return False
        if len(self.vertices) < 2:
            return 0
        self.vertices[0].data = True
        for i in range(2):
            q = deque([self.vertices[i]])
            while q:
                v = q.popleft()
                for w in v.adj:
                    w = self.vertices[w]
                    if w.data is None:
                        w.data = v.data != True
                        q.append(w)
                    elif w.data != (v.data != True):
                        return 0
        return 1


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
    n, data = data[0], data[2:]
    g = Graph(n)
    #g.load(data)
    g.load(data,directed = False)
    print(g.is_bipartite())
    #for v in g.vertices:
    #    print(f'{v.id}: ({v.data})')

