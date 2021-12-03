

class Node(object):
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.parent: Node = None
        self.childs = []
        self.keys = []

    def searchNode(self, node, key):
        # loop through a node, and find the key should be inserted
        for i, element in enumerate(node.keys):
            print("compairing", key, element)
            if key < element:
                return node.childs[i], i

        return node.childs[i + 1], i + 1

    def split(self):
        # newNode = self.Node(self.maxLength)

        mid = self.maxLength // 2

        leftNode = Node(self.maxLength)
        rightNode = Node(self.maxLength)

        leftNode.keys = self.keys[:mid]
        rightNode.keys = self.keys[mid + 1:]

        self.childs = [leftNode, rightNode]
        self.keys = [rightNode.keys[0]]

        for child in leftNode.childs:
            child.parent = leftNode

        for child in rightNode.childs:
            child.parent = rightNode

        return self

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
    def __init__(self, maxLength):
        super().__init__(maxLength)

        self.prev: LeafNode = None
        self.next: LeafNode = None

    def insert(self, key, child):
        if self.keys == []:
            self.keys.append(key)
            self.childs.append([child])
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

        ### use self as leftNode is more ez to handle
        topNode = Node(self.maxLength)
        leftNode = self
        rightNode = LeafNode(self.maxLength)

        mid = self.maxLength // 2

        rightNode.parent = leftNode.parent = topNode

        rightNode.keys = self.keys[mid:]
        rightNode.childs = self.childs[mid:]
        rightNode.prev = leftNode
        if rightNode.next != None:
            rightNode.next = rightNode.next
        topNode.keys = [rightNode.keys[0]]
        topNode.childs = [leftNode, rightNode]

        leftNode.keys = self.keys[:mid]
        leftNode.childs = self.childs[:mid]
        leftNode.next = rightNode

        return topNode

################################################################################################
class BTree(object):
    def __init__(self, maxLength):
        self.root = LeafNode(maxLength)

    @staticmethod
    def find(node: Node, key):
        for i, item in enumerate(node.keys):
            if key < item:
                return node.childs[i], i
            elif i + 1 == len(node.keys):
                return node.childs[i + 1], i + 1  # return right-most node/pointer.

    def merge(self, parent, child, index):
        parent.childs.pop(index)
        pivot = child.keys[0]

        for c in child.childs:
            if isinstance(c, Node):
                c.parent = parent

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.childs = parent.childs[:i] + child.childs + parent.childs[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.childs += child.childs
                break

    def insert(self, key, value):
        node = self.root

        while not isinstance(node, LeafNode):  
            node, index = self.find(node, key)


        node.insert(key, value)

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
    f = open("./file.txt", "r")
    tree = BTree(5)
    for x in f:
        tree.insert(int(x.rstrip()), 0)

    tree.printChilds()
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