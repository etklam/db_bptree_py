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
        # split on Leaf
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

                if (len(upNode.keys) > upNode.maxLength):
                    # split a Right New Node, copy the right half values and keys into Right
                    upLeft, newKey, upRight = self.split(upNode)
                    
                    # updating childs's parent pointer
                    self.updateChildsPointer(upLeft)
                    self.updateChildsPointer(upRight)

                    self.updateParent(upLeft, [newKey], upRight) # recursive update the parent node

    def split(self, node):
        mid = node.maxLength //2
        right = Node()
        left = node
        right.parent = node.parent

        right.values = node.values[mid+1:]
        right.keys = node.keys[mid+1:]

        left.values = node.values[:mid]
        left.keys = node.keys[:mid+1]
        newKey = right.values[0]
        return left, newKey, right

    
    def updateChildsPointer(self, parent):
        for child in parent.keys:
            child.parent = parent

    def search(self, value):
        current = self.root
        while not current.isLeaf:
            temp = current.values
            if type(temp) == int:
                temp = [temp]
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

    def delete(self, value):
        # get the leaf node that might contain the value
        key = value # In this project, we assume all key = value
        leaf = self.search(value)
        delSuccess = False
        for i, item in enumerate(leaf.values):
            if item == value:
                # remove the pointer of the data entry
                # The index() function is used to find the position of the first matching item of a value from a list.
                # leaf.keys[i] is the data entry page, it removes the data of the matching item.
                # check if more than one records sharing a pointer
                if len(leaf.keys[i])>1:
                    # only delete the first matching item if there are multiple records
                    leaf.keys[i].pop(leaf.keys[i].index(key))
                else:
                    leaf.keys[i].pop(leaf.keys[i].index(key))
                    del leaf.keys[i]  #only one data record is using the pointer, it can be/should be deleted.
                    leaf.values.pop(leaf.values.index(value)) # delete the index from the tree

        if delSuccess == False:
            print("Value not found.")


    def printTree(self):
        current = self.root
        # print("root:", self.root.values)
        layer = self.countLayer()
        print(layer)
        current.printALayer()
        for i in range(layer):
            current = current.keys[0]
            current.printALayer()

    def printData(self):
        current = self.root
        # print("root:", self.root.values)
        while not current.isLeaf:
            current = current.keys[0]
        token = "data: "
        token += str(current.keys)
        while current.next != None:
            current = current.next
            token += str(current.keys)
        print(token)
            
    def countLayer(self):
        current = self.root
        counter = 0
        while not current.isLeaf:
            current = current.keys[0]
            counter += 1
        return counter

class main():
    f = open("./test.txt", "r")
    tree = BPTree(5)
    for x in f:
        tree.insert(int(x.rstrip()), int(x.rstrip()))

    #current = tree.root.keys[0].printALayer()
    tree.delete(10)
    tree.delete(10)
    tree.printTree()
    tree.printData()
    # print(current.values)
    # while current.next!=None:
    #     current = current.next
    #     print(current.values)
    # print("testing:", tree.root.keys[0].next.next.values)
    # print("testing:", tree.root.keys[1].next.next.next.values)
    # tree.printTree()