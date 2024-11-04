
class Data:
    def __init__(self):
        self.left = []
        self.right = []
        self.back = []
        self.front = []

    def setLeft(self, value):
        if len(self.left) >= 3:
            self.left.pop(0)
        self.left.append(value)

    def setRight(self, value):
        if len(self.right) >= 3:
            self.right.pop(0)
        self.right.append(value)

    def setFront(self, value):
        if len(self.front) >= 3:
            self.front.pop(0)
        self.front.append(value)

    def setBack(self, value):
        if len(self.back) >= 3:
            self.back.pop(0)
        self.back.append(value)

    def getLeft(self):
        return self.left
    
    def getRight(self):
        return self.right
    
    def getBack(self):
        return self.back
    
    def getFront(self):
        return self.front