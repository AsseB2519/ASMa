class Product:
    def __init__(self, name:str, number:int):
        self.name = name
        self.number = number

    def getName(self):
        return self.name

    def setName(self, name:int):
        self.name = name

    def getNumber(self):
        return self.number

    def setNumber(self, number:int):
        self.number = number

    def toString(self):
        return "Product [Name=" + self.name + ", Number=" + str(self.number) + "]"