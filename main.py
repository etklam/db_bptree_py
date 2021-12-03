class Node (object):
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.keys = []
        self.values = []
        self.childs = []
        self.leaf = True
        self.parentPointer = None
        self.rightPointer = None
        self.leftPointer = None

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

    def printNodeKeys(self):
        return self.keys
        # if self.leafFull:
        #     self.split()

    # def migrateToLeft(self):

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

            # adding pointers to each node
            self.childs = [leftNode, rightNode]
            rightNode.parentPointer = self
            rightNode.leftPointer = leftNode
            leftNode.parentPointer = self
            leftNode.rightPointer = rightNode

            # print("rootNode:", self.keys)
            # print("leftNode:", leftNode.keys)
            # print("rightNode:", rightNode.keys)

    def printAllChildsKey(self):
        arr = []
        arr.append(self.keys)
        for child in self.childs:
            arr.append(child.keys)

        # print(str(arr))

    def leafFull(self):
        if len(self.keys) >= self.maxLength:
            return True
        return False

class BTree (object):
    def __init__(self, maxLength ):
        self.root = Node(maxLength)

    def insert(self, key, value):
        print("inserting", key)
        current = self.root
        if current.leaf == True:
            current.insert(key, value)
            if current.leafFull():
                print('current is full')
            #if "self.leftPointer.leafFull()" or "self.leftpointer == None":
                current.split()
            return

        while current.leaf == False:
            # return the next current node
            current, i = self.searchNode(current, key)    
        current.insert(key, value)

        if current.leafFull():
            print('current is full')
            #if "self.leftPointer.leafFull()" or "self.leftpointer == None":
            current.split()
        # self.printTree()

        

    def searchNode(self, node, key):
        # loop through a node, and find the key should be inserted
        for i, element in enumerate(node.keys):
            print("compairing", key, element)
            if key < element:
                return node.childs[i], i

        return node.childs[i + 1], i + 1

    def printTree(self):
        current = self.root
        counter = 0
        print("root:",current.keys)
        counter+=1
        while not current.leaf:
            current = current.childs[0]
            arr = []
            arr.append(current.keys)
            while current.rightPointer != None:
                current = current.rightPointer
                arr.append(current.keys)
            print("Layer: ", counter,"have:", arr)
class main():
    f = open("./file.txt", "r")
    tree = BTree(5)
    for x in f:
        tree.insert(int(x.rstrip()), 0)

    tree.printTree()
