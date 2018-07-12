from gcd import gcd

def lcm(a, b):
    """retur Least Common Multiple of a and b"""
    return a * b // gcd(a, b)

if __name__ == '__main__':
    a, b = map(int, input().split())
    print(lcm(a, b))
