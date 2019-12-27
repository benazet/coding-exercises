# Good morning! Here's your coding interview problem for today.
# This problem was asked by Airbnb.
# Given a list of integers, write a function that returns the largest sum of non-adjacent numbers. 
# Numbers can be 0 or negative.
# For example, [2, 4, 6, 2, 5] should return 13, since we pick 2, 6, and 5. [5, 1, 1, 5] should return 10, 
# since we pick 5 and 5.

# Follow-up: Can you do this in O(N) time and constant space?


# recurse

def largestSum(list):
    l = len(list)
    if l == 0 :
        return 0
    elif l == 1 :
        return list[0]
    else :
        first = list[0] + largestSum(list[2:])
        second = list[1] + largestSum(list[3:])
        return max( first , second)


print(largestSum([2, 9, 6, 2, 5, 15, 25]))
print(largestSum([5, 1, 1, 5]))


# O(n)

# the idea is to store as you go two alternating series

def largestSum2(list):
    l = len(list)
    if l > 2:
        list[2] += list[0]
    for i in range(3,l):
        list[i] += max(list[i-2],list[i-3])
    return max(list[-1],list[-2])


print(largestSum2([2, 9, 6, 2, 5, 15, 25]))
print(largestSum2([5, 1, 1, 5]))
