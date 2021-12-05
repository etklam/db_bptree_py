

class Node(object):
    def __init__(self, parent= None, maxLength= 5):
        self.maxLength = maxLength
        self.parent:Node= parent
        self.childs = []
        self.keys = []

    # def searchNode(self, node, key):
    #     # loop through a node, and find the key should be inserted
    #     for i, element in enumerate(node.keys):
    #         print("compairing", key, element)
    #         if key < element:
    #             return node.childs[i], i

    #     return node.childs[i+1], i + 1

    def __getitem__(self, item):
        return self.childs[self.find(item)]

    def index(self, key):
        # return the index of a key in a index, if not find, return the length of the key array, which is the last +1 on an array
        for i, item in enumerate(self.keys):
            if key < item:
                return i

        return len(self.keys)

    def split(self):

        ## Split for 
        # newNode = self.Node(self.maxLength)

        mid = self.maxLength // 2
        right = self # name it, it is easier to read
        left = Node(self.maxLength)
        left.parent = self.parent

        left.keys = self.keys[:mid]
        left.childs = self.childs[:mid + 1]

        for child in left.childs:
            child.parent = left

        newKey = self.keys[mid]

        right.keys = self.keys[mid+1:]
        right.childs = self.childs[mid+1:]

        # self.childs = [leftNode, rightNode]
        # self.keys = [rightNode.keys[0]]

        # for child in leftNode.childs:
        #     child.parent = leftNode

        # for child in rightNode.childs:
        #     child.parent = rightNode

        return newKey, [left, right]

################################################################################################
    def isEmpty(self):
        if len(self.keys) == 0:
            return True
        return False

    def isRoot(self):
        return self.parent is None

    def isFull(self):
        return len(self.keys) == self.maxLength - 1


################################################################################################
class LeafNode(Node):
    def __init__(self, parent=None,prevNode=None,nextNode=None, maxLength=5):
        super().__init__(parent)
        # self.parent: Node = None
        # self.prev: LeafNode = None
        # self.next: LeafNode = None
        self.maxLength = 5
        self.next: LeafNode = next
        if prevNode is not None:
            prevNode.next = self
        self.prev: LeafNode = prevNode
        if nextNode is not None:
            nextNode.prev = self

    def __getitem__(self, item):
        # method is called a magic method
        # and this method returns the value corresponding to the given key
        return self.childs[self.keys.index(item)]

    def __setitem__(self, key, value):
        i = self.index(key)
        if key not in self.keys:
            self.keys[i:i] = [key]
            self.childs[i:i] = [value]
        else:
            self.childs[i-1] = value

    def insert(self, key, value):
        if self.keys == []:
            self.keys.append(key)
            self.childs.append([value])
            print("inserted:", key)
            return self

        for i, element in enumerate(self.keys):
            if key == element:
                # [:i] means array before i; [i:] means array after i
                # self.keys = self.keys[:i] + [key] + self.keys[i:] <- key not dup!
                self.childs = self.childs[:i] + [[child]] + self.childs[i:]
                print("==", self.keys)
                return
            elif key < element:
                # [:i] means array before i; [i:] means array after i
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.childs = self.childs[:i] + [[child]] + self.childs[i:]
                print("<", self.keys)
                return
            elif len(self.keys) - 1 == i:
                self.keys.append(key)
                self.childs.append([child])
                print("tail", self.keys)

    def split(self):

        # topNode = Node(self.maxLength)
        # leftNode = self
        # rightNode = LeafNode(self.maxLength)

        # mid = self.maxLength // 2

        # rightNode.parent = leftNode.parent = topNode

        # rightNode.keys = self.keys[mid:]
        # rightNode.childs = self.childs[mid:]
        # rightNode.prev = leftNode
        # if rightNode.next != None:
        #     rightNode.next = rightNode.next
        # topNode.keys = [rightNode.keys[0]]
        # topNode.childs = [leftNode, rightNode]

        # leftNode.keys = self.keys[:mid]
        # leftNode.childs = self.childs[:mid]
        # leftNode.next = rightNode

        left = LeafNode(self.parent, self.prev, self)
        right = self
        mid = len(self.keys) //2

        left.keys = self.keys[:mid]
        left.childs = self.childs[:mid]

        right.keys = self.keys[mid:]
        right.keys = self.childs[mid:]

        return right.keys[0], [left, right]

################################################################################################
class BTree(object):
    def __init__(self, maxLength=5):
        self.root = LeafNode(maxLength)

        self.max = self.maxLength = maxLength

    # def find(self, key):
    #     for i, item in enumerate(node.keys):
    #         if key < item:
    #             return self.childs[i], i
    #         elif i + 1 == len(self.keys):
    #             return self.childs[i+1], i + 1

    # def find(self, key):
    #     node = self.root
    #     for i, item in enumerate(node.keys):
    #         if key < item:
    #             return node.childs[i]
    #         elif i + 1 == len(node.keys):
    #             return node.childs[-1]          # return the right last node

    def __getitem__(self, item):
        return self.find(item)[item]

    def find(self, key):
        # find by using python __getitem__ method
        node = self.root
        while not isinstance(node, LeafNode):
            node = node[key]
        return node

    # def merge(self, parent, child, index):
    #     parent.childs.pop(index)
    #     pivot = child.keys[0]

    #     for c in child.childs:
    #         if isinstance(c, Node):
    #             c.parent = parent

    #     for i, item in enumerate(parent.keys):
    #         if pivot < item:
    #             parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
    #             parent.childs = parent.childs[:i] + child.childs + parent.childs[i:]
    #             break

    #         elif i + 1 == len(parent.keys):
    #             parent.keys += [pivot]
    #             parent.childs += child.childs
    #             break

    def insert(self, key, value):
        node = self.root
        # while not isinstance(node, LeafNode):  
        #     node, index = self.find(node, key)
        leaf = self.find(key)
        leaf[key] = value

        if len(leaf.keys) > self.maxLength:
            leaf.split()
        # node.insert(key, value)

        while len(node.keys) == node.maxLength:
            if not node.isRoot():
                parent = node.parent
                node = node.split()
                temp, index = self.find(parent, node.keys[0])
                self.merge(parent, node, index)
                node = parent
            else:
                node = node.split()
                self.root = node


    def printChilds(self):
        node = self.root
        layerCount = 1
        print("root:", node.keys)
        while not isinstance(node, LeafNode):
            nextLayer = node.childs
            node = node.childs[0]
            printer = str(layerCount) 
            printer += ":"
            for child in nextLayer:
                #print("Layer: ",layerCount, child.keys)
                printer += str(child.keys)
            print(printer)
            
        # current = Node
        # while current.childs != [] and hasattr(current, "childs"):
        #     print(current.keys)
        #     try:
        #         while current.next != None :
        #             if (current == current.next):
        #                 break
        #             else:
        #                 # current = current.next
        #                 print(current.keys)
        #     except:
        #         print(current.keys)
        #         current = current.childs[0]

class main():
    f = open("./test.txt", "r")
    tree = BTree(5)
    for x in f:
        tree.insert(int(x.rstrip()), 0)

    # tree.printChilds()
    # print(tree.root.childs[0].next.keys)
    # tree.printChilds()
    #tree.root.printAllChilds()
    # quit = False
    # while():
    #     ui = input("command>> ")
    #     if ui == "quit":
    #         print("Bye Bye")
    #         quit = True
    #     else:
    #         print("I don't know your command, please input again")

################################################################################################