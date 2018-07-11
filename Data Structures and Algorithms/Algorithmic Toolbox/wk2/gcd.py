def gcd(a, b):
    if b > a:
        a, b = b, a
    if b == 0:
        return 0
    a = a % b
    if a == 0:
        return b
    elif a == 1:
        return 1
    else:
        return gcd(b, a)

if __name__ == '__main__':
    a,b = map(int,input("enter 2 numbers: ").split())
    print(gcd(a, b))