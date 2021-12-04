class Node:
    def __init__(self, maxLength=5):
        self.maxLength = self.maxLength

        self.values = []
        self.keys = []
        self.next: Node = None
        self.parent: Node = None
        self.isLeaf = False

class BPTree:
    def __init__(self, maxLength=5):
        self.root = Node(maxLength)