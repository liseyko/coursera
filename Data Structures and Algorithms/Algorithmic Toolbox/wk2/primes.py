def gen_primelist(n):
    sieve = [0, 0] + [i for i in range(2,n+1,1)]
    print(sieve)
    for i in range(2,len(sieve)):
        if sieve[i] != 0:
            for j in range(sieve[i]*2,len(sieve),sieve[i]):
                sieve[j] = 0

    return [i for i in sieve if i > 0]

if __name__ == '__main__':
    #print(gen_primelist(100) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97])
    print(gen_primelist(int(input())))
