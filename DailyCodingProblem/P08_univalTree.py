# Good morning! Here's your coding interview problem for today.
# This problem was asked by Google.
# A unival tree (which stands for "universal value") is a tree where all nodes under it have the same value.
# Given the root to a binary tree, count the number of unival subtrees.
# For example, the following tree has 5 unival subtrees:
#    0
#   / \
#  1   0
#     / \
#    1   0
#   / \
#  1   1

class node:
    def __init__(self,value,left=None,right=None):
        self.value = value
        self.left = left
        self.right = right
    

    def print(self):
        print(self.left, '<--',self.value, '-->',self.right)



tree = node(False,node(True),node(False,node(True,node(True),node(True)),node(False)))

count = 0

def unival(tree):
    global count
    if tree == None:
        return True
    else :
        if unival(tree.left) == unival(tree.right):
            count +=1
        return tree.value

unival(tree)
print(count)