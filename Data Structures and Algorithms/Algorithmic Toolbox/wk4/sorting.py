# Uses python3
import sys
import random

def partition3(a, l, r):
    x = a[l]
    j = l;
    dupes = 0
    for i in range(l + 1, r + 1):
        if a[i] <= x:
            j += 1
            a[i], a[j] = a[j], a[i]
        if a[i] == x:
            dupes += 1
            a[l+dupes], a[j] = a[j], a[l+dupes]
    for i in range(dupes+1):
        a[l+i], a[j-i] = a[j-i], a[l+i]
        
    return j-dupes,j
    

def partition2(a, l, r):
    x = a[l]
    j = l;
    for i in range(l + 1, r + 1):
        if a[i] <= x:
            j += 1
            a[i], a[j] = a[j], a[i]
    a[l], a[j] = a[j], a[l]
    return j


def randomized_quick_sort(a, l, r):
    if l >= r:
        return
    k = random.randint(l, r)
    a[l], a[k] = a[k], a[l]
    #use partition3
    #m = partition2(a, l, r)
    #randomized_quick_sort(a, l, m - 1);
    #randomized_quick_sort(a, m + 1, r);

    m1,m2 = partition3(a, l, r)
    randomized_quick_sort(a, l, m1 - 1);
    randomized_quick_sort(a, m2 + 1, r);


if __name__ == '__main__':
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    randomized_quick_sort(a, 0, n - 1)
    for x in a:
        print(x, end=' ')
