from Classes.Position import Position

class Delivery:
    def __init__(self, id: int, agent_jid: str, position: Position, weight: float): 
        self.id = id
        self.agent_jid = agent_jid
        self.position = position
        self.weight = weight

    def getId(self):
        return self.id

    def getAgent(self):
        return self.agent_jid

    def getPosition(self):
        return self.position

    def setPosition(self, x: int, y: int):
        self.position = Position(x, y)

    def setPosition(self, position: Position):
        self.position = position

    def getWeight(self):
        return self.weight

    def setWeight(self, weight: float):
        self.weight = weight

    def toString(self):
        return "InformPosition [id=" + str(self.id) + ", agent_jid=" + self.agent_jid + ", position=" + self.position.toString() + ", available=" + str(self.weight) + "]"
