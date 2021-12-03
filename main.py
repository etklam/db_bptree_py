class Node (object):
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.keys = []
        self.values = []
        self.childs = []
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

                print("<=",self.keys)
                break
            elif len(self.keys)-1 == i:
                self.keys.append(key)
                self.values.append([value])
                print("tail",self.keys)
        
        if self.leafFull():
            self.split()
    
    def split(self):
        # if(self.leafFull):
            leftNode = Node(self.maxLength)
            rightNode = Node(self.maxLength)

            leftNode.keys = self.keys[:2]
            rightNode.keys = self.keys[2:]

            # un leaf the node
            self.leaf = False
            leftNode.values = self.values[:2]
            rightNode.values = self.values[2:]
            self.values = []

            #self.keys = self.keys[2] <-not work.
            emptylist = []
            emptylist.append(self.keys[2])
            self.keys = emptylist
            self.childs = [leftNode, rightNode]
            print("rootNode:", self.keys)
            print("leftNode:", leftNode.keys)
            print("rightNode:", rightNode.keys)

    def listAllkeys(self):
        print("::",self.keys)

    def leafFull(self):
        if len(self.keys) >= self.maxLength:
            return True
        return False

class BTree (object):
    def __init__(self, maxLength ):
        self.root = Node(maxLength)

    def insert(self, node, key):

        if self.root.leaf:
            self.root.insert(node, 0)
            return

        current = self.root

        parent = None
        if current.leaf == False:
            parent = current
            current, index = self.searchNode(current, key)

            # if not leaf, try search through keys

    def searchNode(self, node, key):
        # loop through a node, and find the key should be inserted
        for i, element in enumerate(node.keys):
            if key <= element:
                return node.childs[i], i

class main():
    #f = open("./debug.txt", "r")
    f = open("./file.txt", "r")
    tree = BTree(5)
    for x in f:
        tree.insert(int(x.rstrip()), 0)

