# Good morning! Here's your coding interview problem for today.
# This problem was asked by Google.
# Given the root to a binary tree, implement serialize(root), which serializes the tree into a string, 
# and deserialize(s), which deserializes the string back into the tree.

# For example, given the following Node class
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

import json

class NodeEncoder(json.JSONEncoder):
    def default(self,o):
        return {'__{}__'.format(o.__class__.__name__): o.__dict__}

def NodeDecoder(o):
    if '__Node__' in o:
        n=Node(None)
        n.__dict__.update(o['__Node__'])
        return n
    return o

def serialize(node):
    return json.dumps(node,cls=NodeEncoder)

def deserialize(text):
    return json.loads(text,object_hook=NodeDecoder)


# The following test should pass:
node = Node('root', Node('left', Node('left.left')), Node('right'))
print(serialize(node))
assert deserialize(serialize(node)).left.left.val == 'left.left'
print (deserialize(serialize(node)).left.left.val )

