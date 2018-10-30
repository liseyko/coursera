# Uses python3
def edit_distance(s, t):
    
    w, h = len(s)+1, len(t)+1
    D = [[0 for y in range(h)] for x in range(w)] 
    for i in range(w):
        D[i][0] = i
    for j in range(h):
        D[0][j] = j

    """for i in range(w-1):
        print(s[i], end=' ')
    print()"""
    for j in range(1,h):
        for i in range(1,w):
            options = [ D[i][j-1]+1, D[i-1][j]+1 ] 
            if s[i-1] == t[j-1]:
                options.append(D[i-1][j-1])
            else:
                options.append(D[i-1][j-1]+1)
            D[i][j] = min(options)
            """print(D[i][j], end=' ')
        print()"""
          
    return D[i][j]

if __name__ == "__main__":
    print(edit_distance(input(), input()))
