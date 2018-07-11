# python3

import sys

fibcache = {0: 0, 1: 1}
def fib(n):
    if n in fibcache: return fibcache[n]
    if n % 2 == 0:
        fibcache[n] = ((2 * fib((n / 2) - 1)) + fib(n / 2)) * fib(n / 2)
        return fibcache[n]
    else:
        fibcache[n] = (fib((n - 1) / 2) ** 2) + (fib((n+1) / 2) ** 2)
        return fibcache[n]

def fib(n,m):
    if n in fibcache: return fibcache[n]
    if n % 2 == 0:
        fibcache[n] = (2 * fib((n / 2) - 1,m))%m + ((fib(n / 2,m)) * fib(n / 2,m))%m
        return fibcache[n]
    else:
        fibcache[n] = (fib((n - 1) / 2,m) ** 2)%m + (fib((n+1) / 2,m) ** 2)%m
        return fibcache[n]


def pisano_period(n):
   s=[]
   k=0
   i=0
   while k<1 or s[:k] !=s[k:]:
       a = fib(i)
       s += [a%n]
       k = len(s)//2
       i += 1
   return k

def pp(m):
    for i in range(3,m*6+4):
        #print(fib(i)%m,end=',')
        if fib(i,m)%m == 0 and fib(i+1,m)%m == 1 and fib(i+2,m)%m == 1:
            print('pp:',i-1)
            return i


def fib_limited(n,m):
    #print(pp(m),'vs true:',pisano_period(m))
    #return fib( n % pisano_period(m) ) % m
    return fib( n % pp(m) ) % m

if __name__ == '__main__':
    input = sys.stdin.read();
    n, m = map(int, input.split())
    print(fib_limited(n, m))

