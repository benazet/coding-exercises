# Good morning! Here's your coding interview problem for today.
# This problem was asked by Stripe.
# Given an array of integers, find the first missing positive integer in linear time and constant space.
# In other words, find the lowest positive integer that does not exist in the array.
# The array can contain duplicates and negative numbers as well.
# For example, the input [3, 4, -1, 1] should give 2. The input [1, 2, 0] should give 3.
# You can modify the input array in-place.

list = [3, 5, 2, -1, 1,6,5]

# didn't find this one in linear time, because i didn't understand that making a constant number of iteration on the whole 
# set is still linear time...


# Remove non-positive numbers
for i in range(len(list)-1,-1, -1):
    if list[i] <= 0 :
        list.pop(i)

# Setting negative values at index found
for v in list:
    if abs(v) <= len(list):
        list[abs(v)-1] = - list[abs(v)-1]

# Searching the first positive value
solution = len(list)+1
for i in range(0,len(list)-1):
    if list[i] > 0:
        solution = i + 1
        break

print (solution)