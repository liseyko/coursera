import sys

class Vertice():
    def __init__(self,id):
        self.id = id
        self.pre = None
        self.post = None
        self.adj = []

class Graph():
    def __init__(self,n_of_vertices = 0):
        self.vertices = [Vertice(i) for i in range(n_of_vertices)]

    def load(self,data,directed = True):
        for v,w in zip(data[::2],data[1::2]):
            self.vertices[v-1].adj.append(w-1)
            if not directed:
                self.vertices[w-1].adj.append(v-1)

    def _explore_init(self):
        self.explore_order = 0
        self.explored = set()

    def explore(self,v):
        self.explore_order += 1
        v.pre = self.explore_order
        self.explored.add(v.id)
        for w in v.adj:
            if w not in self.explored:
                self.explore(self.vertices[w])
        self.explore_order += 1
        v.post = self.explore_order
        return 0

    def dfs(self):
        self.ccn = 0 #connected_components_number
        self._explore_init()
        for v in self.vertices:
            if v.id not in self.explored:
                self.ccn += 1
                self.explore(v)


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

    def toposort(self):
        return [v.id for v in sorted(self.vertices,key=lambda x: x.post,reverse=True)]


if __name__ == '__main__':
    data = list(map(int,sys.stdin.read().split()))
    n, data = data[0], data[2:]
    g = Graph(n)
    g.load(data)
    g.dfs()
    for v in g.vertices:
        print(f'{v.id}: ({v.pre}/{v.post}), adj: {v.adj}')
    print(' '.join(str(i+1) for i in g.toposort()))


    
