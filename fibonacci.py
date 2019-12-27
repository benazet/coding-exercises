# Illustration of DYNAMIC PROGRAMING
#  Calculate the fibonacci sequence
#  Hyp : n > 2 (don't handle  fib(0))

import time

def fib_recursion(n):
    if n == 1 or n == 2 :
        return 1
    else:
        return fib_recursion(n-1) + fib_recursion(n-2)

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:            
            memo[x] = f(x)
        return memo[x]
    return helper


@memoize
def fib_recursion_memo(n):
    if n == 1 or n == 2 :
        return 1
    else:
        return fib_recursion(n-1) + fib_recursion(n-2)

memo = {}
def fib_memo(n):
    global memo
    if n in memo:
        return memo[n]
    if n == 1 or n == 2 :
        result = 1
    else:
        result = fib_memo(n-1) + fib_memo(n-2)
    memo[n] = result
    return result

def fib_bup(n):
    f2 = 1
    f1 = 1
    for _ in range(2,n):
        result = f2 + f1
        f2 = f1
        f1 = result
    return result

N=10
print("Calculating the %dth value of the Fibonacci sequence" % N)
t = time.time()*10e6
print("{:<15}{:<8}{:>12}{:>12} µs".format("Recursion","O(2^n)",fib_recursion(N),time.time()*10e6-t))
t = time.time()*10e6
print("{:<15}{:<8}{:>12}{:>12} µs".format("Recursion memo","O(2^n)",fib_recursion_memo(N),time.time()*10e6-t))
t = time.time()*10e6
print("{:<15}{:<8}{:>12}{:>12} µs".format("Memoization","O(2n)",fib_memo(N),time.time()*10e6-t))
t = time.time()*10e6
print("{:<15}{:<8}{:>12}{:>12} µs".format("Bottom-up","O(n)",fib_bup(N),time.time()*10e6-t))

N=1000
print("\n%dth value of the Fibonacci sequence :" % N)
t = time.time()*10e6
print(fib_bup(N))
print("{}µs".format(time.time()*10e6-t))
