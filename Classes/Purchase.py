from Classes.Position import Position

class Purchase:
    def __init__(self, agent_jid: str, init: Position, products: list):
        self.agent_jid = agent_jid
        self.init = init
        self.products = products
        # self.purchase = purchase

    def getAgent(self):
        return self.agent_jid

    def getInit(self):
        return self.init

    def setInit(self, x: int, y: int):
        self.init = Position(x, y)

    def getProducts(self):
        return self.products

    def setProducts(self, products: list):
        self.products = products

    def toString(self):
        product_str = ", ".join(product.toString() for product in self.products)
        return "Purchase [agent=" + self.agent_jid + ", position=" + self.init.toString() + ", products=[" + product_str + "]]"
