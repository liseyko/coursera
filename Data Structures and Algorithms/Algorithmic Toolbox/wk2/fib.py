def get_fib(n):
    """naive method of getting n-th Fibonacci number"""
    i, j = 0, 1
    for _ in range(n):
        i, j = j, i + j
    return i

fibs = {0: 0, 1: 1}

def fib(n):
    """optimal method"""
    if n in fibs: return fibs[n]
    if n % 2 == 0:
        fibs[n] = ((2 * fib((n / 2) - 1)) + fib(n / 2)) * fib(n / 2)
        return fibs[n]
    else:
        fibs[n] = (fib((n - 1) / 2) ** 2) + (fib((n+1) / 2) ** 2)
        return fibs[n]



if __name__ == '__main__':
    n = int(input())
    print(fib(n))
    print(get_fib(n))
