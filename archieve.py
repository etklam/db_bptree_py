class main():
    f = open("./file.txt", "r")
    tree = BTree(5)
    for x in f:
        tree.insert(int(x.rstrip()), 0)

    tree.root.show()


################################################################################################

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
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.childs = self.childs[:i] + [[child]] + self.childs[i:]
                print("==", self.keys)
                break
            elif key <= element:
                # [:i] means array before i; [i:] means array after i
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.childs = self.childs[:i] + [[child]] + self.childs[i:]
                print("<", self.keys)
                break
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

        leftNode.keys = self.keys[:mid]
        leftNode.childs = self.childs[:mid]
        leftNode.next = rightNode

        topNode.keys = [rightNode.keys[0]]
        topNode.childs = [leftNode, rightNode]

        return topNode


################################################################################################
class BTree(object):
    def __init__(self, maxLength):
        self.root = LeafNode(maxLength)

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
        print("inserting", key)
        # init
        current = self.root

        ### only LeafNode can insert, LeafNode and Node have diff split functions
        while not isinstance(current, LeafNode):
            current, i = self.searchNode(current, key)

        current.insert(key, value)

        ### check if full
        while current.isFull():
            if current.isRoot():
                top = current.split()
                current = top
            else:
                parent = current.parent
                current = current.split()
                temp, index = current.searchNode(parent, current.keys[0])
                self.merge(parent, current, index)
                current = parent

