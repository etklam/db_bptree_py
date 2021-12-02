class Node (object):
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.keys = []
        self.values = []
        self.leaf = True

    def insert(self, key, value):
        if self.keys == []:
            self.keys.append(key)
            self.values.append([value])
            print("node")
            print(self.keys)
            return


    #    def insert(key, value):
    #        # check is it a empty node
    #        if not self.keys:
    # def insert(self, key, value):
    #     # The very first insert
    #     if self.keys == []:
    #         self.keys.append(key)
    #         self.value.append([value])
    #         return

    #     for i, element in enumerate(self.keys):
    #         if key <= element:
    #             self.keys = self.keys[:i] + [key] + self.keys[i:]
    #             self.values = self.values[:i] + [[value]] + self.values[i:]
    #             break
            
    #         else:
    #             self.keys.append(key)
    #             self.values.append([value])

class BTree (object):
    def __init__(self, maxLength ):
        self.root = Node(maxLength)

    def insert(self, node, key):
        root.insert(node, key, value)
    
    # def search(self, node, key):
    #     for i, element in enumerate(node.keys):
    #         if key < element:
    #             return node.values[i], i
    #     return node.values[i + 1], i + 1

    # def insert(self, key, value):
    #     # scanning from root
    #     parent = None
    #     child = self.root
class main():
    f = open("./file.txt", "r")
    tree = BTree(5)
    for x in f:
        tree.root.insert(x, 0)
