from typing import ValuesView

###############################
###
###
###
###
###
###
###############################


class Node:
    def __init__(self, maxLength=5):
        self.maxLength = maxLength

        self.values = []
        self.keys = []
        self.next: Node = None
        self.parent: Node = None
        self.isLeaf = False

    
    # Insert at the leaf
    def insert(self, leaf, value, key):
        print("insert:", key)
        
        if (self.values):
            temp = self.values
            for i in range(len(temp)):
                if (value == temp[i]):
                    self.keys[i].append(key)
                    print("after insert:", self.keys)
                    break
                elif (value < temp[i]):
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    print("after insert:", self.keys)
                    break
                elif (i + 1 == len(temp)):
                    self.values.append(value)
                    self.keys.append([key])
                    print("after insert:", self.keys)
                    break
        else:
            self.values = [value]
            self.keys = [[key]]

    def split(self):
        node = self
        mid = node.maxLength // 2
        left = node
        right = Node()
        right.isLeaf = True
        right.parent = node.parent
        right.values = node.values[mid:]
        right.keys = node.keys[mid:]
        right.next = node.next
        left.values = node.values[:mid]
        left.keys = node.keys[:mid]
        left.next = right
        print("left:", left.keys)
        print("right:", right.keys)
        print("key", right.values[0])
        return left,right.keys[0], right
    
    def printALayer(self):
        current = self
        token = ":::"
        token += str(current.values)
        while current.next!=None:
            current = current.next
            token += str(current.values)
        token += ":::"
        print(token)

class BPTree:
    def __init__(self, maxLength=5):
        self.root = Node(maxLength)
        self.root.isLeaf = True
        
    def insert(self, key, value = 0):
        node = self.search(key)
        node.insert(node, value, key)

        ## if > maxOrder:
        if (len(node.values) == node.maxLength):
            left, key, right = node.split()
            self.updateParent(left, key, right)
            # self.split(left, keys, right)

    def updateParent(self, left, key, right):
        if(self.root == left):
            #this is a init split
            newRoot = Node()
            newRoot.values = key
            newRoot.keys = [left, right]
            self.root = newRoot
            left.parent = newRoot
            right.parent = newRoot
            return
        else:
            upNode = left.parent
            pointers = upNode.keys
            for i in range(len(pointers)):
                if (pointers[i] == left):
                    # find the left(original pointer on upNode), then assign to the next slot
                    upNode.values = upNode.values[:i]+key+upNode.values[i:]
                    upNode.keys = upNode.keys[:i+1]+[right]+upNode.keys[i+1:]  # the new pointer(right pointer) should be one behind the original(pointer)

        # Not root:
        # parent = left.parent
        # temp = parent.keys
        # for i in range(len(temp)):
        #     if(temp[i] == left.keys):
        #         parent.values = parent.values[:i] + [key] + parent.values[i:]
        #         parent.keys = parent.keys[:i+1]+[key] + parent.values[i+1:]



        # print("splited parent", parent.keys)

    def search(self, value):
        current = self.root
        while not current.isLeaf:
            temp = current.values
            for i in range(len(temp)):
                # print("temp[i]:", value, str(temp[i]))
                if (value == temp[i]):
                    current = current.keys[i + 1]
                    break
                elif (value < temp[i]):
                    current = current.keys[i]
                    break
                elif (i + 1 == len(current.values)):
                    current = current.keys[i + 1]
                    break
        return current

    def printTree(self):
        current = self.root
        # print("root:", self.root.values)
        layer = self.countLayer()
        print(layer)
        current.printALayer()
        for i in range(layer):
            current = current.keys[0]
            current.printALayer()

    def countLayer(self):
        current = self.root
        counter = 0
        while not current.isLeaf:
            current = current.keys[0]
            counter += 1
        return counter
    
    # def allLeftNode(self):
    #     current = self.root
    #     counter = 0
    #     while not current.isLeaf:
    #         current = current.keys[0]
    #         counter +=1

    #     return counter


            

class main():
    f = open("./test.txt", "r")
    tree = BPTree(5)
    for x in f:
        tree.insert(int(x.rstrip()), int(x.rstrip()))

    current = tree.root.keys[0].printALayer()

    tree.printTree()
    # print(current.values)
    # while current.next!=None:
    #     current = current.next
    #     print(current.values)
    # print("testing:", tree.root.keys[0].next.next.values)
    # print("testing:", tree.root.keys[1].next.next.next.values)
    # tree.printTree()