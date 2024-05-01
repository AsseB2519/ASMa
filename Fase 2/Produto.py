
class Produto:
    def __init__(self, nome="", peso=0.0, preco=0.0):
        self.name = nome
        self.peso = peso
        self.preco = preco
        self.entregue = False

    def __str__(self):
        return "Produto: " + self.name + " Peso: " + self.peso

    def getName(self):
        return self.name

    def getPeso(self):
        return self.peso

    def getPreco(self):
        return self.preco

    def getEstado(self):
        return self.entregue

    def passouEntregue(self):
        self.entregue = True