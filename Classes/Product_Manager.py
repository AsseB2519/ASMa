class Product:
    def __init__(self, product_id: int, name: str, category: str, quantity: int, price: float):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price

    def get_product_id(self) -> int:
        return self.product_id

    def set_product_id(self, product_id: int) -> None:
        self.product_id = product_id

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_category(self) -> str:
        return self.category

    def set_category(self, category: str) -> None:
        self.category = category

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int) -> None:
        self.quantity = quantity

    def get_price(self) -> float:
        return self.price

    def set_price(self, price: float) -> None:
        self.price = price

    def __str__(self):
        return f"Product [ID={self.product_id}, Name={self.name}, Category={self.category}, Quantity={self.quantity}, Price={self.price}]"
