class Node (object):

    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.keys = []
        self.values = []
        self.leaf = True

class BTree (object):
    def __init__(self, maxLength):
        maxLength = 5
        self.root = Node(maxLength)

#    def insert(key, value):
#        # check is it a empty node
#        if not self.keys:
