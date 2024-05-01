from Node import Node
from Client import Client

class Order:
    current_id = 0
    def __init__(self, weight=0.0, localizacao="", goods=[], origem="", destino="", time="", client=Client()): # nao pode ultrapassar 100 kg
        Order.current_id += 1
        self.id = Order.current_id
        self.weight = weight
        self.localizacao = localizacao
        self.goods = goods
        self.start_street = origem
        self.delivery_street = destino
        self.delivery_time = time
        self.client = client
        self.entregue = False

    def __str__(self):
        return "Order " + str(self.id) + " To: " + str(self.client) + " Goods: " + str(self.goods)

    def __repr__(self):
        return "Order " + self.id + " To: " + self.client
    
    def getId(self):
        return self.id

    def getWeight(self):
        return self.weight
    
    def getGoods(self):
        return self.goods
    
    def getStreet(self):
        return self.delivery_street
    
    def getTime(self):
        return self.delivery_time
    
    def getClient(self):
        return self.client

    def getEstado(self):
        return self.entregue

    def getTime(self):
        return self.delivery_time

    def getDestino(self):
        return self.delivery_street

    def getOrigem(self):
        return self.start_street

    def getLocalizacao(self):
        return self.localizacao
    
    def setId(self, newId):
        self.id = newId

    def setWeight(self, newWeight):
        self.weigth = newWeight
    
    def setGoods(self, newGoods):
        self.goods = newGoods

    def setStreet(self, newStreet):
        self.delivery_street = newStreet

    def setTime(self, newTime):
        self.delivery_time = newTime

    def setClient(self, newClient):
        self.client = newClient

    def passouEntregue(self):
        self.entregue = True

    def __eq__(self, other):
        if other.isinstance(Order):
            return self.id == other.id and self.client == other.client and self.goods == other.goods
        return False
    
    def __hash__(self):
        return hash(self.id)