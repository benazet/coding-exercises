#This problem was asked by Uber.

# Given an array of integers, return a new array such that each element at index i 
# of the new array is the product of all the numbers in the original array except the one at i.
# For example, if our input was [1, 2, 3, 4, 5], the expected output would be 
# [120, 60, 40, 30, 24]. If our input was [3, 2, 1], the expected output would be [2, 3, 6].

# Follow-up: what if you can't use division?

list = [1, 2, 3, 4, 5]

product =1
for i in list:
    product *= i

result = []
for i in list:
    result.append(product / i)

print(list)
print(result)


# Follow-up

result = []
for i in list:
    product = 1
    for j in list : 
        if j != i:
            product *= j
    result.append(product)

print(result)