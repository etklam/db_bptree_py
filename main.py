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
            return self

        for i, element in enumerate(self.keys):
            if key <= element:
                #[:i] means array before i; [i:] means array after i
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                # print("<=",self.keys)
                break
            elif len(self.keys)-1 == i:
                self.keys.append(key)
                self.values.append([value])
                # print("tail",self.keys)
                break
        return self
    
    def listAllkeys(self):
        print(self.keys)

    def leafFull():
        if len(keys) >= maxLength:
            return True
        return False

class BTree (object):
    def __init__(self, maxLength ):
        self.root = Node(maxLength)

    def insert(self, node, key):
        self.root.insert(node, key, value)
        self.root.listAllkeys()
    
    def search(self, node, key):
        for i, element in enumerate(node.keys):
            if key < element:
                return i
        return i + 1

    # def insert(self, key, value):
    #     # scanning from root
    #     parent = None
    #     child = self.root
class main():
    #f = open("./debug.txt", "r")
    f = open("./file.txt", "r")
    tree = BTree(5)
    for x in f:
        tree.root.insert(int(x.rstrip()), 0)
