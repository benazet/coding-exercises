
# Good morning! Here's your coding interview problem for today.

# This problem was asked by Google.
# Implement integer exponentiation. That is, implement the pow(x, y) function, where x and y are integers and returns x ^ y.
# Do this faster than the naive method of repeated multiplication.
# For example, pow(2, 10) should return 1024.

import math
import timeit


def square_and_multiply(x, y):
    if y == 1:
        return x
    elif (y % 2) == 0:
        return square_and_multiply(x*x, y/2)
    else:
        return x * square_and_multiply(x*x, y//2)


def naive_repeated_multiplication(x, y):
    result = 1
    for _ in range(y):
        result *= x
    return result


def sm():
    return square_and_multiply(2, 257)


def naive():
    return naive_repeated_multiplication(2, 257)


print(timeit.timeit(sm))
print(timeit.timeit(naive))
