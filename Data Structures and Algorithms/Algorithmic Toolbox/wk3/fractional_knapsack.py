# python3

class Item():
    def __init__(self,vw):
        self.v, self.w = vw
        self.vpw = self.v / self.w

def get_optimal_value(capacity, items):
    value = 0.

    for i in items:
        slice = min(i.w,capacity)
        capacity -= slice
        value += i.vpw * slice
        if capacity == 0: 
            break

    return value


if __name__ == "__main__":

    n, capacity = map(int, input().strip().split())
    items = []
    for i in range(n):
        items.append(Item( map(int, input().strip().split())))

    items.sort(key=lambda x: x.vpw, reverse=True)

    opt_value = get_optimal_value(capacity, items)
    print("{:.5f}".format(opt_value))
