from Classes.Position import Position

class Return:
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

    # def getPurchase(self):
    #     return self.purchase

    # def setPurchase(self, purchase: bool):
    #     self.purchase = purchase

    def toString(self):
        product_str = ", ".join(product.toString() for product in self.products)
        return "Return [agent=" + self.agent_jid + ", position=" + self.init.toString() + ", products=[" + product_str + "]]"
