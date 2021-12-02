class Node (object):

    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.keys = []
        self.values = []
        self.leaf = True

class BTree (object):
    def __init__(self, maxLength = 5):
        self.root = Node(maxLength)

#    def insert(key, value):
#        # check is it a empty node
#        if not self.keys:
    def insert(self, key, value):
        # The very first insert
        if self.keys == []:
            self.keys.append(key)
            self.value.append([value])
            return

        for i, element in enumerate(self.keys):
            if key <= element:
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break
            
            else:
                self.keys.append(key)
                self.values.append([value])


