#Uses python3

import sys

def acyclic_explore(v,adj,vis,recstack):
    vis[v] = True
    recstack.add(v)
    for w in adj[v]:
        if w in recstack:
            return 1
        if vis[w] == False:
            if acyclic_explore(w,adj,vis,recstack) == 1:
                return 1
    recstack.discard(v)
    return 0


def acyclic(adj,vis):
    result = 0
    for v in range(len(adj)):
        if not vis[v]:
            recstack = set()
            if acyclic_explore(v,adj,vis,recstack) == 1:
                result = 1
                break
    return result



if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    vis = [False for _ in range(n)]
    recstack = [False for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(acyclic(adj,vis))
