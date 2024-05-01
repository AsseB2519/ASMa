from Node import Node

class Client:
    current_id = 0
    def __init__(self, name="", password="", history=[]):
        Client.current_id += 1
        self.id = Client.current_id
        self.name = name
        self.order_history = history
        self.password = password

    def __str__(self) -> str:
        return "Client: " + str(self.id) + " Name: " + self.name
    
    def getName(self):
        return self.name
    
    def getHistory(self):
        return self.order_history
    
    def setId(self, newId):
        self.id = newId

    def setName(self, newName):
        self.name = newName

    def setId(self, newHistory):
        self.order_history = newHistory

    def add_nova_entrega(self, entrega):
        self.order_history.append(entrega)

    def __eq__(self, other):
        if other.isinstance(Client):
            return self.id == other.id and self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.name)