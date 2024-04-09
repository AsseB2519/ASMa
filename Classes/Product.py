# class Product:
#     def __init__(self, name:str, number:int):
#         self.name = name
#         self.number = number

#     def getName(self):
#         return self.name

#     def setName(self, name:int):
#         self.name = name

#     def getNumber(self):
#         return self.number

#     def setNumber(self, number:int):
#         self.number = number

#     def toString(self):
#         return "Product [Name=" + self.name + ", Number=" + str(self.number) + "]"

class Product:
    def __init__(self, name: str, quantity: int, price: float): # , description: str, expiry_date: str
        self.name = name
        self.quantity = quantity
        self.price = price
        # self.description = description
        # self.expiry_date = expiry_date

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        self.quantity = quantity

    def get_price(self) -> float:
        return self.price

    def set_price(self, price: float) -> None:
        self.price = price

    # def get_description(self) -> str:
    #     return self.description

    # def set_description(self, description: str) -> None:
    #     self.description = description

    # def get_expiry_date(self) -> str:
    #     return self.expiry_date

    # def set_expiry_date(self, expiry_date: str) -> None:
    #     self.expiry_date = expiry_date

    def toString(self):
        return "Product [Name=" + self.name + ", Quantity=" + str(self.number) + ", Price=" + str(self.price) + "]"