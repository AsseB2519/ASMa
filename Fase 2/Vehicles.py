
class Vehicle():
    current_id=0
    def __init__(self):
        Vehicle.current_id += 1
        self.id = Vehicle.current_id


class Bike(Vehicle):
    def __init__(self):
        super().__init__()
        self.max_weight = 5 # kg
        self.velocity = 10 # km/h
        self.polution = 0 # kg of polution per km
        
    def __str__(self):
        return "Bicicleta: " + str(self.id)
    
    def getVel(self):
        return self.velocity

    def reduceVel(self, weight):
        self.velocity -= weight*0.6

    def canCarry(self, weight):
        return weight <= self.max_weight

    def __eq__(self, other):
        return self.id == other.id and self.__class__ == other.__class__

    def __hash__(self):
        hash(self.id)

class Motorcycle(Vehicle):
    def __init__(self):
        super().__init__()
        self.max_weight = 20
        self.velocity = 35
        self.polution = 0.13

    def __str__(self):
        return "Moto: " + str(self.id)
    
    def getVel(self):
        return self.velocity

    def reduceVel(self, weight):
        self.velocity -= weight*0.5

    def incresePol(self, weight):
        self.polution += weight*0.005

    def canCarry(self, weight):
        return weight <= self.max_weight

    def __eq__(self, other):
        return self.id == other.id and self.__class__ == other.__class__

    def __hash__(self):
        hash(self.id)

class Car(Vehicle):
    def __init__(self):
        super().__init__()
        self.max_weight = 100
        self.velocity = 50
        self.polution = 0.37
        self.type = "Car"
    def __str__(self):
        return "Carro: " + str(self.id)
    
    def getVel(self):
        return self.velocity

    def reduceVel(self, weight):
        self.velocity -= weight*0.1

    def incresePol(self, weight):
        self.polution += weight*0.005

    def canCarry(self, weight):
        return weight <= self.max_weight

    def getType(self):
        return self.type
    def __eq__(self, other):
        return self.id == other.id and self.__class__ == other.__class__

    def __hash__(self):
        hash(self.id)