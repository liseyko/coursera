def minRefills(x,l):
    num_refills = 0
    cm = 0
    i = 0
    while i < len(x)-1:
        if cm + x[i+1] < l:
            cm += x[i+1]
            i +=1
        else:
            num_refills +=1
            cm = 0
            if cm + x[i+1] > l:
                return None
    return num_refills


if __name__ == '__main__':
    print(minRefills([0,10,30,40,20,10],50))