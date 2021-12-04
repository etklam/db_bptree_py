from typing import ValuesView, cast
import os
import sys
import random
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
        self.prev: Node = None
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
        right.prev = left
        print("left:", left.keys)
        print("right:", right.keys)
        print("key", right.values[0])
        return left, right.keys[0], right

    def printALayer(self):
        current = self
        token = ":::"
        token += str(current.values)
        while current.next != None:
            current = current.next
            token += str(current.values)
        token += ":::"
        print(token)


class BPTree:
    def __init__(self, maxLength=5):
        self.root = Node(maxLength)
        self.root.isLeaf = True

    def insert(self, key, value=0):
        node = self.search(key)
        node.insert(node, value, key)

        # if > maxOrder:
        if (len(node.values) == node.maxLength):
            left, key, right = node.split()
            self.updateParent(left, key, right)
            # self.split(left, keys, right)

    def updateParent(self, left, key, right):
        if(self.root == left):
            # this is a init split
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
                    # the new pointer(right pointer) should be one behind the original(pointer)
                    upNode.keys = upNode.keys[:i+1]+[right]+upNode.keys[i+1:]

                if (len(upNode.keys) > upNode.maxLength):
                    # split a Right New Node, copy the right half values and keys into Right
                    upLeft, newKey, upRight = self.split(upNode)

                    # updating childs's parent pointer
                    self.updateChildsPointer(upLeft)
                    self.updateChildsPointer(upRight)

                    # recursive update the parent node
                    self.updateParent(upLeft, [newKey], upRight)

    def split(self, node):
        mid = node.maxLength // 2
        right = Node()
        left = node
        right.parent = node.parent

        right.values = node.values[mid:]
        right.keys = node.keys[mid:]

        left.values = node.values[:mid]
        left.keys = node.keys[:mid+1]
        left.next = right
        right.prev = left
        newKey = right.values[0]
        if type(newKey) == list:
            if len(newkey) > 1:
                newKey = list(set(newKey))
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
                    current = current.keys[i]
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
        key = value  # In this project, we assume all key = value
        leaf = self.search(value)
        delSuccess = False
        for i, item in enumerate(leaf.values):
            if item == value:
                delSuccess = True
                # remove the pointer of the data entry
                # The index() function is used to find the position of the first matching item of a value from a list.
                # leaf.keys[i] is the data entry page, it removes the data of the matching item.
                # check if more than one records sharing a pointer
                if len(leaf.keys[i]) > 1:
                    # only delete the first matching item if there are multiple records
                    leaf.keys[i].pop(leaf.keys[i].index(key))
                else:
                    leaf.keys[i].pop(leaf.keys[i].index(key))
                    # only one data record is using the pointer, it can be/should be deleted.
                    del leaf.keys[i]
                    # delete the index from the tree
                    leaf.values.pop(leaf.values.index(value))
                    # check if the deleted value is in the parent Node
                    # if value in leaf.parent.values:
                    #     parent = leaf.parent
                    #     parent.values[parent.values.index(value)] = leaf.values[0]
                    self.updateParentAfterDel(leaf, value)
                    mid = leaf.maxLength // 2
                    ### deletion rules
                    #1. borrow from left
                    #2. Merge with left
                    #3. Borrow from right, only the left most Node can borrow and merge from right
                    #4. Merge with right, only the left most Node can borrow and merge from right
                    ###
                    if len(leaf.values) < mid:
                        self.borrowFromLeft(leaf)
                        
        if delSuccess == False:
            print("Value not found.")

    def borrowFromLeft(self, node):
        mid = node.maxLength //2
        prev = node.prev
        if prev != None:
            if len(prev.values) > mid:
                
                borrowV = prev.values.pop(-1)
                print("borrow: ", borrowV)
                borrowK = prev.keys.pop(-1)
                node.values.insert(0,borrowV)
                node.keys.insert(0,borrowK)
                self.updateParentAfterDel(node, borrowV)
            else:
                print("cannot borrow!, need merge")

    def merge(self):
        index = self.parent.index(self.values[0])
        # merge with the prev node
        prev = self.prev
        next = self.next
        parent = self.parent
        prev.values.append(self.values[0])
        for child in self.keys:
            child.parent = prev
        parent.values.pop(index)
        parent.keys.pop(self)

    def updateParentAfterBorrow(self, node, value):
        if node.parent !=None:
            parent = node.parent
            if value in parent.values:
                parent.values[parent.values.index(value)] = value
                if parent.parent != None:
                    self.updateParent(parent, value)

    def updateParentAfterDel(self, updatedNode, value):
        # while updatedNode.parent != None:
        if updatedNode.parent == None:
            return

        while value in updatedNode.parent.values:
            parent = updatedNode.parent
            if updatedNode.values == []:
                parent.values.pop(parent.values.index(value)) # exception if there are no value in leafNode
            else:
                parent.values[parent.values.index(value)] = updatedNode.values[0]
            self.updateParentAfterDel(parent, value)

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

    def rangeSearch(self, a, b):
        minV = min(a,b)
        maxV = max(a,b)
        keyArr = []
        current = self.search(minV)
        
        while current.next != None:
            for value in current.values:
                if value>=minV and value <maxV:
                    keyArr.append(value)
            current = current.next
        return keyArr

class main():
    f = open("./test.txt", "r")
    tree = BPTree(5)
    for x in f:
        tree.insert(int(x.rstrip()), int(x.rstrip()))
        tree.printTree()
        tree.printData()

    #current = tree.root.keys[0].printALayer()

    tree.printTree()
    tree.printData()
    tree.delete(8)
    tree.printTree()
    tree.printData()

    #print(current.values)
    # while current.next!=None:
    #     current = current.next
    #     print(current.values)
    # print("testing:", tree.root.keys[0].next.next.values)
    # print("testing:", tree.root.keys[1].next.next.next.values)
    tree.printTree()
    print(tree.rangeSearch(7,20))


def btree(fanme):
    tree = BPTree(5)
    start = True
    with open(fanme, "r", encoding='utf-8') as f:
        print("Building an initial B+-Tree...")
        for line in f:
            tree.insert(int(line), int(line))

        print("Launching B+-Tree test program...")
        while start:
            print("Waiting for your commands:")
            i = input()
            cmd = i.split(" ")
            if cmd[0].lower() == "insert":
                if len(cmd) < 4 or len(cmd) > 4:
                    print(f"command insert format: insert <low> <high> <num>")
                elif int(cmd[1]) > int(cmd[2]):
                    print(f"command insert format: insert <low> <high> <num>")
                else:
                    low = int(cmd[1])
                    high = int(cmd[2])
                    for i in range(int(cmd[3])):
                        key = random.randint(low, high)
                        tree.insert(key=key)
                    print(
                        f"{cmd[3]} data entries with keys randomly chosen between [{low}, {high}] are inserted!")
            elif cmd[0].lower() == "delete":
                if len(cmd) < 3 or len(cmd) > 3:
                    print(f"command delete format: delete <low> <high>")
                elif int(cmd[1]) > int(cmd[2]):
                    print(f"command delete format: delete <low> <high>")
                else:
                    low = int(cmd[1])
                    high = int(cmd[2])
                    key = random.randint(low, high)
                    tree.delete(key)
                    print(
                        f"The data entries for values in [{low}, {high}] are deleted.")
            elif cmd[0].lower() == "search":
                if len(cmd) < 3 or len(cmd) > 3:
                    print("command search format: search <low> <high>")
                elif int(cmd[1]) > int(cmd[2]):
                    print("command search format: search <low> <high>")
                else:
                    low = int(cmd[1])
                    high = int(cmd[2])
                    result = tree.search(low)
                    print("key in range: ", result.keys)
                    # for i in range(low, high):
                    #     result = tree.search(i)
                    #     print("key in range: ", result.keys)
            elif cmd[0].lower() == "print":
                tree.printData()
            elif cmd[0].lower() == "stats":
                # tree.dumpStatistic()
                print("dump stat")
            elif cmd[0].lower() == "quit":
                start = False
                print("Thanks!Byebye")
            else:
                print("unknown command")


if __name__ == "__main__":
    arg = str(sys.argv[1])
    if arg == None:
        print("Please input argument [fname] or -help for help")

    if arg == "-help":
        print(
            "Usage: btree [fname] \n      fname: the name of the data file storing the search key values")
    elif arg.endswith(".txt"):
        btree(fanme=arg)
