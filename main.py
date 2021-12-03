class Node (object):
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.parent: Node = None
        self.childs = []
        self.keys = []
        self.values = []
        self.leaf = True
        # self.parentPointer = None
        # self.rightPointer = None
        # self.leftPointer = None

    def insert(self, key, value):
        if self.keys == []:
            self.keys.append(key)
            self.values.append([value])
            return self

        for i, element in enumerate(self.keys):
            if key == element:
                #[:i] means array before i; [i:] means array after i
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                print("==",self.keys)
                break
            elif key < element:
                #[:i] means array before i; [i:] means array after i
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                print("<",self.keys)
                break
            elif len(self.keys)-1 == i:
                self.keys.append(key)
                self.values.append([value])
                print("tail",self.keys)

    def addKey(self, key):
        ## insert function without value
        if self.keys == []:
            self.keys.append(key)
            return self

        for i, element in enumerate(self.keys):
            if key == element:
                #[:i] means array before i; [i:] means array after i
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                print("==",self.keys)
                break
            elif key < element:
                #[:i] means array before i; [i:] means array after i
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                print("<",self.keys)
                break
            elif len(self.keys)-1 == i:
                self.keys.append(key)
                print("tail",self.keys)
    
    def split(self):
        # newNode = self.Node(self.maxLength)

        mid = self.maxLength//2

        # newNode.values = self.values[mid + 1:]
        # self.values = self.values[:mid + 1]
        # newNode.keys = self.keys[mid+1:]
        # self.keys = self.keys[:mid]

        # if len(newNode.values) > 0:
        #     newNode.leaf = False
        leftNode = Node(self.maxLength)
        rightNode = Node(self.maxLength)

        leftNode.keys = self.keys[:mid]
        rightNode.keys = self.keys[mid+1:]

        self.childs = [leftNode, rightNode]
        self.keys = [rightNode.keys[0]]

        for child in leftNode.childs:
            child.parent = leftNode
        
        for child in rightNode.childs:
            child.parent = rightNode

        return self
 

    def isEmpty(self):
        if len(self.keys) == 0:
            return True
        return False

    def getNodeKeys(self):
        return self.keys
        # if self.leafFull:
        #     self.split()
    def isFull(self):
        return (self.keys) >= self.maxLength -1

    def isRoot(self):
        return self.parent is None

    # def migrateToLeft(self):

    # def split(self):
    #     # if(self.leafFull):
    #         try:
    #             # no parentNode means it is a root node
    #             parentNode = self.parentPointer
    #         except:
    #             leftNode = Node(self.maxLength)
    #             rightNode = Node(self.maxLength)

    #             leftNode.keys = self.keys[:2]
    #             rightNode.keys = self.keys[2:]

    #             # un leaf the node
    #             self.leaf = False
    #             leftNode.values = self.values[:2]
    #             rightNode.values = self.values[2:]
    #             self.values = []

    #             #self.keys = self.keys[2] <-not work.
    #             emptylist = []
    #             emptylist.append(self.keys[2])
    #             self.keys = emptylist

    #             # adding pointers to each node
    #             self.childs = [leftNode, rightNode]
    #             rightNode.parentPointer = self
    #             rightNode.leftPointer = leftNode
    #             leftNode.parentPointer = self
    #             leftNode.rightPointer = rightNode
    def split(self):


        leftNode = Node(self.maxLength)
        rightNode = Node(self.maxLength)
        
        leftNode.keys = self.keys[:2]
        rightNode.keys = self.keys[3:]
        
        leftNode.values = self.values[:2]
        rightNode.values = self.values[3:]

        return self.keys[2], leftNode, rightNode

            # print("rootNode:", self.keys)
            # print("leftNode:", leftNode.keys)
            # print("rightNode:", rightNode.keys)

    def moveToLeft(self):
        # move the smallest value from right node to left node
        # update the keys in parent Node
        parent = self.parentPointer
        leftNode = self.leftPointer
        keyToMove = self.keys.pop(0)
        valueToMove = self.values.pop(0)

        # add to left tail
        leftNode.keys.append(keyToMove)
        leftNode.values.append(valueToMove)

        # update key on parent
        for key in parent.keys:
            if key == keyToMove:
                key = self.keys[0]

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

class LeafNode(Node):
    def __init__(self, maxLength):
        super().__init__(maxLength)

        self.prev: LeafNode = None
        self.next: LeafNode = None



class BTree (object):
    def __init__(self, maxLength ):
        self.root = Node(maxLength)

    def insert(self, key, value):
        print("inserting", key)
        # init
        current = self.root
        if current.leaf == True:
            current.insert(key, value)
            if current.leafFull():
                print('current is full')
            #if "self.leftPointer.leafFull()" or "self.leftpointer == None":
                pivot, leftNode, rightNode = current.split()
                current = Node(current.maxLength)
                current.leaf = False
                current.addKey(pivot)
                current.childs[leftNode,rightNode]
            return
        # end init
        while current.leaf == False:
            # return the next current node
            current, i = self.searchNode(current, key)

        current.insert(key, value)
        # current.insert(key, value)

        if current.leafFull():
            print('current is full')
            try:
                isEmpty = current.leftPointer.isEmpty()
                leftFull = current.leftPointer.leafFull()
            except:
                print("current is root")
                current.split()
                return

            if(leftFull):
                current.split()
            else:
                current.moveToLeft()


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
