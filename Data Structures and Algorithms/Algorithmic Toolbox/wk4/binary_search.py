# Uses python3
import sys

def binary_search(a, x):
    l, r = 0, len(a)-1
    # write your code here
    while l <= r:
        m = l + (r - l) // 2
        if x == a[m]:
            return m
        elif x > a[m]:
            l = m + 1
        else:
            r = m - 1
    return -1

def linear_search(a, x):
    for i in range(len(a)):
        if a[i] == x:
            return i
    return -1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    m = data[n + 1]
    a = data[1 : n + 1]
    for x in data[n + 2:]:
        # replace with the call to binary_search when implemented
        #print(linear_search(a, x), end = ' ')
        print(binary_search(a, x), end = ' ')
