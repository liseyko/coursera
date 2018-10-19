# Uses python3
import sys
import random


def fast_count_segments(starts, ends, points):
    cnt = [0] * len(points)
    starts = [(starts[i],1) for i in range(len(starts))]
    ends = [(ends[i]+1,-1) for i in range(len(ends))]
    segments = sorted(starts+ends)
    points = sorted([(points[i],i) for i in range(len(points))])

    i, j, q = 0, 0, 1
    while points[i][0] < segments[0][0]: i += 1
    while i < len(points) and j < len(segments)-1:
        if points[i][0] < segments[j+1][0]:
            cnt[points[i][1]] = q
            i += 1
        else:
            j += 1
            q += segments[j][1]
    return cnt

def naive_count_segments(starts, ends, points):
    cnt = [0] * len(points)
    for i in range(len(points)):
        for j in range(len(starts)):
            if starts[j] <= points[i] <= ends[j]:
                cnt[i] += 1
    return cnt

def selftest():
  for t in range(101):
    starts, ends, points = [], [], []
    n,m = random.randint(10,100), random.randint(10,100)
    for i in range(n):
        starts.append(random.randint(0,40) - 20)
        ends.append(starts[-1] + random.randint(1,20))
    for i in range(m):
        points.append(random.randint(0,40) - 20)
    r1 = naive_count_segments(starts, ends, points)
    r2 = fast_count_segments(starts, ends, points)
    if r1 == r2:
        print("%i: Success"%(t))
    else:
        print("%i: Fail:"%(t))
        print("+:",r1)
        print("-:",r2)
        print("s:",starts)
        print("e:",ends)
        print("p:",points)

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    m = data[1]
    starts = data[2:2 * n + 2:2]
    ends   = data[3:2 * n + 2:2]
    points = data[2 * n + 2:]
    #use fast_count_segments
    #cnt = naive_count_segments(starts, ends, points)
    cnt = fast_count_segments(starts, ends, points)
    for x in cnt:
        print(x, end=' ')    

    #selftest()
