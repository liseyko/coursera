#!/usr/bin/python3
import sys
from copy import deepcopy
from heapq import heappush, heappop

class VerticeBase():
    def __init__(self, id):
        self.id = id
        self.adj = []

    def __lt__(self, other):
        return self.id < other.id

class Graph():
    def __init__(self, n_of_vertices=0, directed=True, weighted=True):
        self.inf = n*10**6
        self.vertices = [VerticeBase(i) for i in range(n_of_vertices)]
        self.verticesR = deepcopy(self.vertices)
        self.dist = [self.inf for _ in self.vertices]
        self.directed = directed
        self.weighted = weighted

    def append(self, u, v, w=1, offset=1):
        self.vertices[u - offset].adj.append([v - offset, w])
        self.verticesR[v - offset].adj.append([u - offset, w])
        #if not self.directed:
        #    self.vertices[v - offset].adj.append([u - offset, w])

    def biDirDij_distance(self, src, dst, offset=1):
        src, dst = src - offset, dst - offset
        vertices = [self.vertices, self.verticesR]
        distF = self.dist.copy()
        distR = self.dist.copy()
        dist = [distF, distR]
        distF[src], distR[dst] = 0, 0
        hf,hr = [], []
        h = [hf, hr]
        heappush(hf, (distF[src], self.vertices[src]))
        heappush(hr, (distR[dst], self.verticesR[dst]))
        #prevF = [None for _ in self.vertices]
        #prevR = prevF.copy()
        #prev = [prevF, prevR]
        processedF, processedR = set(), set()
        processed = [processedF, processedR]
        i = 0
        while True:
            if len(h[i]) > 0:
                (u_dist, u) = heappop(h[i])
                if u.id in processed[i]:
                    continue
                for v_id, v_wgt in u.adj: # def Process
                    if v_id not in processed[i] and dist[i][v_id] > u_dist + v_wgt: # def Relax()
                        dist[i][v_id] = u_dist + v_wgt
                        #prev[i][v_id] = u
                        heappush(h[i], (dist[i][v_id], vertices[i][v_id]))
                processed[i].add(u.id)
                if u.id in processed[1-i]:  #def shortestPath:
                    distance = self.inf
                    for v_id in processedF: #(processedF or processedR):
                        if distF[v_id]+distR[v_id] < distance:
                            distance = distF[v_id]+distR[v_id]
                    return distance
            if not hf and not hr:
                return -1
            i = 1 - i

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
        print(g.biDirDij_distance(s,d))