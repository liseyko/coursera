#!/usr/bin/python3
import sys
import math
from collections import deque
from heapq import heappush, heappop

sys.setrecursionlimit(200000)

class VerticeBase():
    def __init__(self, id):
        self.id = id
        self.adj = [] #[[v1,w1],[v2,w2]...]
        #self.wgt = {}

    def __lt__(self, other):
        return self.id < other.id

class VerticeD(VerticeBase):
    def __init__(self, id):
        super().__init__(id)
        self.rev = []

class Vertice(VerticeD):
    def __init__(self, id):
        super().__init__(id)
        self.data = None
        self.pre = None
        self.post = None
        self.dist = None
        self.prev = None
    """
    def __lt__(self, other):
        return self.data < other.data
    """

class Graph():
    def __init__(self, n_of_vertices=0, directed=True, weighted=True):
        self.vertices = [Vertice(i) for i in range(n_of_vertices)]
        self.verticesR = None
        self.vertices_RevAdj = None
        self.directed = directed
        self.weighted = weighted

    def _init_reverse_copy(self, full_copy=False):
            #if isinstance(self.vertices[0],VerticeD):
            if full_copy:
                self.verticesR = [Vertice(i) for i in range(len(self.vertices))]
                for u in self.vertices:
                    for v_id, v_wgt in u.adj:
                        self.verticesR[v_id].adj.append([u.id,v_wgt])
            else:
                self.vertices_RevAdj = [[] for _ in range(len(self.vertices))]
                for u in self.vertices:
                    for v_id, v_wgt in u.adj:
                        self.vertices_RevAdj[v_id].append([u.id,v_wgt])

    def reverse(self):
        if not self.vertices_RevAdj:
            self._init_reverse_copy()
        for i in range(len(self.vertices)):
            self.vertices[i].adj, self.vertices_RevAdj[i] = self.vertices_RevAdj[i], self.vertices[i].adj

    def append(self, u, v, w=1, offset=1):
        self.vertices[u - offset].adj.append([v - offset, w])
        if not self.directed:
            self.vertices[v - offset].adj.append(u - offset, w)

    def load(self, data, directed=True, weighted=False, from_coordinates=False, offset=1):
        del self.vertices[:]
        self.vertices_RevAdj = None
        if from_coordinates:
            directed = False
            weighted = True
            offset = 0
            data = self._create_dense_graph(data)
        self.directed = directed
        self.weighted = weighted
        if weighted:
            edges = list(zip(zip(data[0::3], data[1::3]), data[2::3]))
        else:
            edges = [(edge, 1) for edge in zip(data[0::2], data[1::2])]
        for ((a, b), w) in edges:
            self.append(a, b, w, offset)

    def _create_dense_graph(self, coord_lst):
        g = []
        cll = len(coord_lst)
        for i in range(0,cll-1):
            for j in range(i+1,cll):
                (x1, y1), (x2, y2) = coord_lst[i], coord_lst[j]
                w = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                g += [i, j, w]
        return g

    def _explore_init(self):
        self.explore_order = 0
        self.explored = set()

    def explore(self, u, update_order=False):
        if update_order:
            self.explore_order += 1
            u.pre = self.explore_order
        self.explored.add(u.id)
        for v, _ in u.adj:
            if v not in self.explored:
                self.explore(self.vertices[v],update_order)
        if update_order:
            self.explore_order += 1
            u.post = self.explore_order
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
            for w, _ in v.adj:
                if not dist[w]:
                    q.append(w)
                    dist[w] = dist[v.id] + 1
                    prev[w] = v.id
        return dist, prev


    def _biDirDij_distance(self, src, dst, offset=1):
        self._init_reverse_copy(full_copy = True)
        vertices = [self.vertices, self.verticesR]
        distF = [float('inf') for _ in self.vertices]
        distR = distF.copy()
        dist = [distF, distR]
        distF[src], distR[dst] = 0, 0
        hf,hr = [], []
        h = [hf, hr]
        heappush(hf, (distF[src], self.vertices[src]))
        heappush(hr, (distR[dst], self.verticesR[dst]))
        prevF = [None for _ in self.vertices]
        prevR = prevF.copy()
        prev = [prevF, prevR]
        processedF, processedR = set(), set()
        processed = [processedF, processedR]
        i = 0
        while True:
            if len(h[i]) > 0:
                (u_dist, u) = heappop(h[i])
                if u.id in processed[i]:
                    continue
                for v_id, v_wgt in [(v_id, v_wgt) for (v_id, v_wgt) in u.adj if v_id not in processed[i]]: # def Process
                    if dist[i][v_id] > u_dist + v_wgt: # def Relax()
                        dist[i][v_id] = u_dist + v_wgt
                        prev[i][v_id] = u
                        heappush(h[i], (dist[i][v_id], vertices[i][v_id]))
                if u.id in processed[1-i]:  #def shortestPath:
                    distance = float('inf') 
                    for v_id in (processedF or processedR):
                        if distF[v_id]+distR[v_id] < distance:
                            distance = distF[v_id]+distR[v_id]
                    #print(distF,'\n',distR,'\n',processedF,'<->',processedR,',', src,'->',dst,' : ',u_dist,'+', dist[1-i][u.id])
                    #return u_dist + dist[1-i][u.id] #should return path + distance instead
                    return distance
                processed[i].add(u.id)
            if len(hf) + len(hr) == 0:
                return -1
            i = 1 - i

    def _dij_distance(self, src, dst, offset=1):
        h = []
        dist = [float('inf') for _ in self.vertices]
        explored = set()
        dist[src] = 0
        heappush(h, (dist[src], self.vertices[src]))
        while len(h) > 0:
            (u_dist, u) = heappop(h)
            if u.id == dst:
                return u_dist
            if u.id in explored:
                continue
            for v_id, v_wgt in [(v_id, v_wgt) for (v_id, v_wgt) in u.adj if v_id not in explored]:
                #print(u.id, '-', v.id,':', dist[v], u_dist, '+', u.wgt[v_id])
                if dist[v_id] > u_dist + v_wgt:
                    dist[v_id] = u_dist + v_wgt
                    heappush(h, (dist[v_id], self.vertices[v_id]))
            explored.add(u.id)
        return -1

    def distance(self, src, dst, offset=1):
        src, dst = src - offset, dst - offset
        if not self.weighted:
            dist = self.bfs(src)[0][dst]
            if dist:
                return dist
            else:
                return -1
        else: 
            #return self._dij_distance(src,dst,offset)
            return self._biDirDij_distance(src,dst,offset)

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
                    for v_id, v_wgt in u.adj:
                        #print(f'{u.id} -> {v_id}, {u.wgt}, {dist}')
                        if dist[v_id] > dist[u.id] + v_wgt:
                            dist[v_id] = dist[u.id] + v_wgt
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
        #print(prev)
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
                for v_id, v_wgt in u.adj:
                    #print(f'{u.id}({dist[u.id]}) -> {v_id}({dist[v_id]}) [{u.wgt[v_id]}]')
                    if dist[v_id] > dist[u.id] + v_wgt:
                        dist[v_id] = dist[u.id] + v_wgt
                        reduced = True
            if not reduced:
                return 0
        return 1

    def _acyclic_explore(self,v):
        self.explored.add(v.id)
        self.cycle.add(v.id)
        for w, _ in v.adj:
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
                for w, _ in self.vertices[v].adj:
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

    def mst_kruskal(self):
        v_grp = {}
        edges = set()
        for u in self.vertices:
            v_grp[u.id] = set([u.id])
            for v_id, v_wgt in u.adj:
                #print('wgt:', u.wgt[v_id],'edge:', sorted((v_id, u.id)))
                edges.add((v_wgt, tuple(sorted((v_id, u.id)))))
        edges = sorted(edges)
        result = []
        for (w,(u_id,v_id)) in edges:
            #print(f'{u_id}-{v_id} : {u_id} not in {v_grp[v_id]} and {v_id} not in {v_grp[u_id]}')
            if u_id not in v_grp[v_id] and v_id not in v_grp[u_id]:
                result += [u_id, v_id, w]
                v_grp[u_id].update(v_grp[v_id])
                for vgi in v_grp[u_id]:
                    v_grp[vgi] = v_grp[u_id]
                #print(v_grp)
        return result

    def mst_prim(self):
        cost = [float('inf') for _ in self.vertices]
        parent = [None for _ in self.vertices]
        cost[0] = 0
        h = []
        self._explore_init()
        heappush(h, (0,self.vertices[0]))
        while len(h) > 0 and len(self.explored) < len(self.vertices):
            _, u = heappop(h)
            #print('exploring:', u.id)
            self.explored.add(u.id)
            for v_id, v_wgt in u.adj:
                v = self.vertices[v_id]
                #print(f'{v_id} not explored: {v_id not in self.explored} and {cost[v_id]} > {u.wgt[v_id]}')
                if v_id not in self.explored and cost[v_id] > v_wgt:
                    #print('sub_exploring:', v_id)
                    cost[v_id] = v_wgt
                    parent[v_id] = u.id
                    heappush(h, (cost[v_id], v))
                    #print('pushed',v_id,':',u.id,'-',v_id, '|', cost[v_id])
        result = list(sum([[parent[i],i,cost[i]] for i in range(1,len(parent))], []))
        return result

    def minimum_distance(self):
        #print(self.mst_kruskal())
        #print(self.mst_prim())
        #print(format(sum(self.mst_kruskal()[2::3]), '.9f') == format(sum(self.mst_prim()[2::3]), '.9f'))
        return format(sum(self.mst_kruskal()[2::3]), '.9f')

    def clustering(self, k):
        return format(self.mst_kruskal()[2::3][-k+1],'.12f')



def readline():
    return map(int, sys.stdin.readline().split())

if __name__ == '__main__':
    n, m = readline()
    g = Graph(n)
    for _ in range(m):
        u, v, w = readline()
        g.append(u, v, w)

    q, = readline()
    for _ in range(q):
        s, d = readline()
        print(g.distance(s,d))