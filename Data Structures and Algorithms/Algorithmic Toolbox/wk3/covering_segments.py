# Uses python3
import sys
from collections import namedtuple

Segment = namedtuple('Segment', 'start end')

def optimal_points(segments):
    points = []

    segments.sort()

    s0 = list(segments[0])
    for s1 in segments[1:]:
        if s1[0] <= s0[1]:
            s0[1] = min(s0[1],s1[1])
        else:
            points.append(s0[1])
            s0 = list(s1)
    points.append(s0[1])
    return points

if __name__ == '__main__':
    input = sys.stdin.read()
    n, *data = map(int, input.split())
    segments = list(map(lambda x: Segment(x[0], x[1]), zip(data[::2], data[1::2])))
    points = optimal_points(segments)
    print(len(points))
    for p in points:
        print(p, end=' ')
