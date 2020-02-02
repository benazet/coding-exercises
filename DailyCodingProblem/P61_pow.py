
# Good morning! Here's your coding interview problem for today.

# This problem was asked by Google.
# Implement integer exponentiation. That is, implement the pow(x, y) function, where x and y are integers and returns x ^ y.
# Do this faster than the naive method of repeated multiplication.
# For example, pow(2, 10) should return 1024.

import math
import timeit


def power(x, y):
    if y == 1:
        return x
    elif (y % 2) == 0:
        return power(x*x, y/2)
    else:
        return x*power(x*x, y//2)
