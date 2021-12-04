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
        print("insert:", key, value)
        
        if (self.values):
            temp1 = self.values
            for i in range(len(temp1)):
                if (value == temp1[i]):
                    self.keys[i].append(key)
                    print("after insert:", self.keys)
                    break
                elif (value < temp1[i]):
                    self.values = self.values[:i] + [value] + self.values[i:]
                    self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                    print("after insert:", self.keys)
                    break
                elif (i + 1 == len(temp1)):
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

class BPTree:
    def __init__(self, maxLength=5):
        self.root = Node(maxLength)
        self.root.isLeaf = True
        
    def insert(self, key, value = 0):
        node = self.search(key)
        node.insert(node, value, key)

        ## if > maxOrder:
        if (len(node.values) == node.maxLength):
            node.split()





    def search(self, value):
        current = self.root
        while not current.isLeaf:
            temp = current.values
            for i in range(len(temp)):
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




class main():
    f = open("./test.txt", "r")
    tree = BPTree(5)
    for x in f:
        tree.insert(int(x.rstrip()), int(x.rstrip()))