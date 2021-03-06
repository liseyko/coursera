#Uses python3
import sys
from collections import deque
from heapq import heappush, heappop

sys.setrecursionlimit(200000)

class Vertice():
    def __init__(self, id):
        self.id = id
        self.data = None
        self.pre = None
        self.post = None
        self.adj = []
        self.wgt = {}
        self.dist = None
        self.prev = None

    def __lt__(self, other):
        #return self.data < other.data
        return self.id < other.id

class Graph():
    def __init__(self, n_of_vertices = 0):
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

    def load(self, data, directed=True, weighted=False):
        self.directed = directed
        self.weighted = weighted
        if weighted:
            edges = list(zip(zip(data[0::3], data[1::3]), data[2::3]))
        else:
            edges = [(edge,None) for edge in zip(data[0::2], data[1::2])]
        for ((a, b), w) in edges:
            self.vertices[a-1].adj.append(b-1)
            if weighted:
                self.vertices[a-1].wgt[b-1] = w
            if not directed:
                self.vertices[b-1].adj.append(a-1)
                if weighted:
                    self.vertices[b-1].wgt[a-1] = w

    def _explore_init(self):
        self.explore_order = 0
        self.explored = set()

    def explore(self, v, update_order=False):
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
        if not self.weighted:
            dist = self.bfs(src)[0][dst]
            if dist:
                return dist
            else:
                return -1
        else:
            h = []
            dist = {v:float('inf') for v in self.vertices}
            self._explore_init()
            v = self.vertices[src]
            dist[v] = 0
            heappush(h, (dist[v], v))
            while len(h) > 0:
                (u_dist, u) = heappop(h)
                if u.id == dst:
                    return u_dist
                elif u.id in self.explored:
                    continue
                self.explored.add(u.id)
                for v_id in [v_id for v_id in u.adj if v_id not in self.explored]:
                    v = self.vertices[v_id]
                    #print(u.id, '-', v.id,':', dist[v], u_dist, '+', u.wgt[v_id])
                    if dist[v] > u_dist + u.wgt[v_id]:
                        dist[v] = u_dist + u.wgt[v_id]
                        heappush(h, (dist[v], v))
            return -1

    def shortest_distances(self, src):
        if self.weighted:
            dist = [float('inf') for _ in self.vertices]
            prev = [None for _ in self.vertices]
            dist[src] = 0

            for _ in range(len(self.vertices)):
                q = deque([src])
                reduced = False
                self._explore_init()
                while q:
                    u = self.vertices[q.popleft()]
                    self.explored.add(u.id)
                    for v_id in u.adj:
                        #print(f'{u.id} -> {v_id}, {u.wgt}, {dist}')
                        if dist[v_id] > dist[u.id] + u.wgt[v_id]:
                            dist[v_id] = dist[u.id] + u.wgt[v_id]
                            reduced = True
                            if v_id not in self.explored:
                                q.append(v_id)
                            prev[v_id] = u.id
                    if not reduced:
                        break
                if reduced:
                    loop_node = v_id
                    while True:
                        dist[loop_node] = float('-inf')
                        loop_node = prev[loop_node]
                        if loop_node == v_id:
                            break
            results = {float('inf'):'*',float('-inf'):'-'}
            return [results[x] if x in results else x for x in dist]




    def path(self, src, dst):
        prev = self.bfs(src)[1]
        print(prev)
        q = deque([dst])
        while dst != src:
            dst = prev[dst]
            q.appendleft(dst)
        return list(q)

    def negative_cycle(self):
        if not self.weighted or not self.vertices:
            return 0
        dist = [float('inf') for _ in range(len(self.vertices))]
        prev = [None for _ in range(len(self.vertices))]
        dist[self.toposorted_list()[0].id] = 0
        for _ in range(len(self.vertices)):
            reduced = False
            for u in self.vertices:
                for v_id in u.adj:
                    #print(f'{u.id}({dist[u.id]}) -> {v_id}({dist[v_id]}) [{u.wgt[v_id]}]')
                    if dist[v_id] > dist[u.id] + u.wgt[v_id]:
                        dist[v_id] = dist[u.id] + u.wgt[v_id]
                        reduced = True
            if not reduced:
                return 0
        return 1

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

        dist = [None for _ in range(len(self.vertices))]
        self.vertices[0].data = True
        for i in range(2):
            q = deque(self.vertices[i])
            while q:
                v = q.popleft()
                for w in self.vertices[v].adj:
                    w = self.vertices[w]
                    if w.data is None:
                        w.data = v.data != True
                        q.append(w)
                    elif w.data != (v.data != True):
                        return 0
        return -1


    def toposorted_list(self):
        if self.vertices and not self.vertices[0].post:
            self.dfs()
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
    n, data, src = data[0], data[2:-1], data[-1]-1
    #Graph with SRC and DST:
    #n, data, s, d = data[0], data[2:-2], data[-2]-1, data[-1]-1
    g = Graph(n)
    g.load(data,weighted=True)
    #for v in g.vertices:
    #    print(f'{v.id}: ({v.pre}/{v.post}), adj: {v.adj}')
    #print(g.distance(s,d))#,g.path(s,d))
    for x in g.shortest_distances(src):
        print(x)
