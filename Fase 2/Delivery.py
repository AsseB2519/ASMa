from Worker import worker
from Vehicles import Vehicle

class Delivery:
    current_id = 0
    def __init__(self, produtos=[], worker=worker(), price=0.0, vehicle=Vehicle(), rating=0.0):
        Delivery.current_id += 1
        self.id = Delivery.current_id
        self.list_products = produtos # lista de objetos order
        self.worker = worker
        self.price = price
        self.vehicle = vehicle
        self.rating = rating

    def __str__(self):
        return "Delivery: " + str(self.id)
    
    def getId(self):
        return self.id
    
    def getProducts(self):
        return self.list_products
    
    def getWorker(self):
        return self.worker
    
    def getPrice(self):
        return self.price
    
    def getVehicle(self):
        return self.vehicle
    
    def getRating(self):
        return self.rating
    
    def setId(self, newId):
        self.id = newId

    def setProducts(self, newProds):
        self.list_products = newProds

    def setWorker(self, newWorker):
        self.worker = newWorker

    def setPrice(self, newPrice):
        self.price = newPrice

    def setVehicle(self, newVehicle):
        self.vehicle = newVehicle

    def setRating(self, newRating):
        self.rating = newRating

    def __eq__(self, other):
        if other.isinstance(Delivery):
            return self.id == other.id and self.list_orders == other.list_orders and self.worker == other.worker
        return False
    
    def __hash__(self):
        return hash(self.id)
                