fn_data = {0:0,1:1}

def get_fib(n):
    """get n-th Fibonacci number"""
    if n not in fn_data:
        fn_data[n] = get_fib(n-2) + get_fib(n-1)
    return fn_data[n]

if __name__ == '__main__':
    print(get_fib(int(input())))
