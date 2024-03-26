from Classes.Position import Position

class MakeRequest:
    def __init__(self, agent_jid: str, init: Position, product: str):
        self.agent_jid = agent_jid
        self.init = init
        self.product = product

    def getAgent(self):
        return self.agent_jid

    def getInit(self):
        return self.init

    def setInit(self, x: int, y: int):
        self.init = Position(x, y)

    def getProduct(self):
        return self.product

    def setProduct(self, product : str):
        self.product = product

    def toString(self):
        return "MakeRequest [agent=" + self.agent_jid + ", init=" + self.init.toString() + ", product=" + self.product + "]"