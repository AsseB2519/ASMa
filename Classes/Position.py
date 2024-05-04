class Position:
    def __init__(self, x:int, y:int, node:int):
        self.x = x
        self.y = y
        self.node=node

    def getX(self):
        return self.x

    def setX(self, x:int):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y:int):
        self.y = y

    def setNode(self, node:int):
        self.node = node

    def getNode(self):
        return self.node        

    def toString(self):
        return "Position [X=" + str(self.x) + ", Y=" + str(self.y) + ", Node=" + str(self.node) + "]"


       

    

    

