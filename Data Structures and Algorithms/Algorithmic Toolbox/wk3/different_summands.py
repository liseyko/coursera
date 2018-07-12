# Uses python3
import sys

def optimal_summands(n):
    
    if n < 3: 
        return [n]

    summands = []
    result = []

    r = 0
    for i in range(1,n):
        if n - r > 2*i:
            r += i
            result.append(i)
        else:
            result.append(n-r)
            return result

    return summands

if __name__ == '__main__':
    input = sys.stdin.read()
    n = int(input)
    summands = optimal_summands(n)
    print(len(summands))
    for x in summands:
        print(x, end=' ')
