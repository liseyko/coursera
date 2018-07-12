from random import randint

def groupify(l,gr_range = 10):
    l.sort()
    results = [[]]
    cur_gr = l[0]

    for i in l:
        if i > cur_gr + gr_range:
            cur_gr = i
            results.append([i])
        else:
            results[-1].append(i)

    return results


if __name__ == '__main__':
    l = [randint(1,100) for _ in range(30)]
    print(l)
    print(groupify(l))