#Uses python3

import sys

def explore(v,adj,vis,order,x):
    vis[v] = True
    for w in adj[v]:
        if vis[w] == False:
            explore(w,adj,vis,order,x)
            order.append(w)
            x+=1
    return 0


def dfs(adj, vis, order, x):
    #write your code here
    for v in range(len(adj)):
        if not vis[v]:
            explore(v,adj,vis,order,x)
            order.append(v)
            x +=1
    
def toposort(adj):
    vis = [False for _ in range(len(adj))]
    #used = [0] * len(adj)
    order = []
    x = 0
    #write your code here
    dfs(adj,vis,order,x)
    #print(adj)
    #print(order)
    return reversed(order)

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    order = toposort(adj)
    for x in order:
        print(x + 1, end=' ')
