# python3
import sys, threading
sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

class TreeHeight:
        def __init__(self):
            self.max_Height = 0
            self.height_cache = []

        def read(self):
            self.n = int(sys.stdin.readline())
            self.height_cache = [0] * self.n
            self.parent = list(map(int, sys.stdin.readline().split()))

        def compute_height(self):
            for node in range(self.n):
                self.compute_height_fast(node)
            return self.max_Height;


        def compute_height_fast(self, node):
            if node == -1:
                return 0
            elif self.height_cache[node] != 0:
                return self.height_cache[node]
            else:
                self.height_cache[node] = 1 + self.compute_height_fast(self.parent[node])
                self.max_Height = max(self.max_Height, self.height_cache[node]);
                return self.height_cache[node]
                


def main():
  tree = TreeHeight()
  tree.read()
  print(tree.compute_height())

if __name__ == "__main__":
    threading.Thread(target=main).start()
