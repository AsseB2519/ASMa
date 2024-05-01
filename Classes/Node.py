class Positions:
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y

    def __str__(self):
        return "X: " + self.x + "; Y: " + self.y

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setX(self, newX):
        self.x = newX

    def setY(self, newY):
        self.y = newY

class Node: # Interseção de ruas
    def __init__(self, id=0, posicao=Positions(), street_count=0):
        self.m_id = id
        self.pos = posicao # não é suposto ser -1
        self.street_count = street_count

    def __str__(self):
        return "node " + str(self.m_id)

    def __repr__(self):
        return "node " + str(self.m_id)

    def getId(self):
        return self.m_id
    
    def setId(self, id):
        self.m_id = id

    def getCortada(self):
        return self.cortada
    
    def setCortada(self, newCortada):
        self.cortada = newCortada

    def getTransito(self):
        return self.transito
    
    def setTransito(self, newTransito):
        self.transito = newTransito

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.m_id == other.m_id
        return False
    
    def __hash__(self):
        return hash(self.m_id)