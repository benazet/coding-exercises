# Good morning! Here's your coding interview problem for today.
# This problem was asked by Apple.
# Implement a job scheduler which takes in a function f and an integer n, and calls f after n milliseconds.


import time

def f():
    print("Function f called")


def schedule(f,n):
    t = time.time()
    while time.time() - t < n:
        #waiting
        a=1
    f()

schedule(f,1)