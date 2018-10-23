# Uses python3
import sys
from collections import Counter


def get_majority_element(a, left, right):
    if len(a)<3:
        return -1
    if right - left == 0:
        return -1
    elif right - left == 1:
        return a[left]
    #elif right - left == 2:
    #    return [k for k,v in Counter(a[left:right]).items() if v>1][0]
    #elif right - left == 3:
    #    return [k for k,v in Counter(a[left:right]).items() if v>1][0]
    else:
        m = left + (right - left + 1) // 2
        al = get_majority_element(a, left, m-1)
        ar = get_majority_element(a, m, right)
        if al == ar: # and m - left != 1 and right - m != 1:
            if Counter(a[left:right+1])[al] > (right-left+1) // 2:
                return al
            else: 
                return -1
        else:
            if ar == -1 or al != -1:
                #for i in range(m,right+1):
                #    if al == a[i]:
                #print(Counter(a[left:right+1]))
                if Counter(a[left:right+1])[al] > (right-left+1) // 2:
                    return al
            if al == -1 or ar != -1:
                #for i in range(left,m):
                    #if ar == a[i]:
                #print(Counter(a[left:right+1]))
                if Counter(a[left:right+1])[ar] > (right-left+1) // 2:
                    return ar
            return -1
        

if __name__ == '__main__':
    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    if get_majority_element(a, 0, len(a)-1) != -1:
        print(1)
    else:
        print(0)
