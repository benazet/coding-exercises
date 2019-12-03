# Good morning! Here's your coding interview problem for today.
# This problem was recently asked by Google.
# Given a list of numbers and a number k, return whether any two numbers from the list add up to k.
# For example, given [10, 15, 3, 7] and k of 17, return true since 10 + 7 is 17.
# Bonus: Can you do this in one pass?

nums = (10, 15, 3, 7)
k = 17

def findPair(nums,goal):
    comp=list()
    for num in nums:
        if num in comp:
            print("%d+%d" % (num,goal-num))
            return True
        else:
            comp.append(goal-num)
    return False

print(findPair(nums,k))