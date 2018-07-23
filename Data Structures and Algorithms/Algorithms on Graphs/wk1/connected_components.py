#Uses python3

import sys

def explore(v,adj,vis):
    vis[v] = True
    for w in adj[v]:
        if vis[w] == False:
            explore(w,adj,vis)
    return 0


def number_of_components(adj,vis):
    result = 0
    for v in range(len(adj)):
        if not vis[v]:
            explore(v,adj,vis)
            result+=1
    return result

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    vis = [False for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    #print(adj)
    print(number_of_components(adj,vis))
