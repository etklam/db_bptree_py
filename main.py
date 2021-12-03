

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

    def printAllChilds(self):
        counter = 0
        print("Layer: ",counter, self.keys)
        while not isinstance(self, LeafNode):
            counter+=1
            childs = self.childs
            for c in childs:
                c.childsprintAllChilds(c)

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

    # def insert(self, key, value):
    #     print("inserting", key)
    #     # init
    #     current = self.root

    #     ### only LeafNode can insert, LeafNode and Node have diff split functions
    #     while not isinstance(current, LeafNode):
    #         current, i = self.searchNode(current, key)

    #     current.insert(key, value)

    #     ### check if full
    #     while current.isFull():
    #         if current.isRoot():
    #             top = current.split()
    #             current = top
    #         else:
    #             parent = current.parent
    #             current = current.split()
    #             temp, index = current.searchNode(parent, current.keys[0])
    #             self.merge(parent, current, index)
    #             current = parent
    def insert(self, key, value):
        node = self.root

        while not isinstance(node, LeafNode):  # While we are in internal nodes... search for leafs.
            node, index = self.find(node, key)

        # Node is now guaranteed a LeafNode!
        node.insert(key, value)

        while len(node.keys) == node.maxLength:  # 1 over full
            if not node.isRoot():
                parent = node.parent
                node = node.split()  # Split & Set node as the 'top' node.
                jnk, index = self.find(parent, node.keys[0])
                self.merge(parent, node, index)
                node = parent
            else:
                node = node.split()  # Split & Set node as the 'top' node.
                self.root = node  # Re-assign (first split must change the root!)

class main():
    f = open("./file.txt", "r")
    tree = BTree(5)
    for x in f:
        tree.insert(int(x.rstrip()), 0)

    print(tree.root.childs[0].next.keys)

    #tree.root.printAllChilds()


################################################################################################