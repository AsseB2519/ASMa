
class Ruas:
    def __init__(self, name="", origem=0, destino=0, oneway=False, highway="", rotunda=False, ponte=False, tunnel=False, vel=[], len=0, ref=False, cortada=False, transito=False):
        self.nome = name
        self.nodo_origem = origem # id do nodo
        self.nodo_destino = destino
        self.oneway = oneway
        self.highway = highway # Lista do tipo de highway (pode ser mais que 1) !n é uma lista
        self.rotunda = rotunda # Por enquanto apenas encontramos rotundas, mas poderá haver mais??
        self.ponte = ponte
        self.tunnel = tunnel
        self.vel_max = vel
        self.length = len
        self.cortada = cortada # Estes valores são ligados aleatóriamente
        self.transito = transito
        self.ref = ref

    def isCortada(self):
        return self.cortada
    
    def isTransito(self):
        return self.transito
    
    def getOrigem(self):
        return self.nodo_origem
    
    def getDestino(self):
        return self.nodo_destino
    
    def getName(self):
        return self.nome

    def getHighway(self):
        return self.highway

    def getRoundabout(self):
        return self.rotunda

    def getRef(self):
        return self.ref

    def getBridge(self):
        return self.ponte

    def getTunnel(self):
        return self.tunnel
    
    def getLength(self):
        return self.length
    def setCortada(self):
        self.cortada=True

    def __str__(self):
        list_str = ', '.join(map(str, self.highway))
        return f"Rua: {self.nome} ; Origem: {self.nodo_origem} ; Destino: {self.nodo_destino} ; Oneway: {self.oneway} ; Highway: {list_str}"

    def __repr__(self):
        list_str = ', '.join(map(str, self.highway))
        return f"Rua: {self.nome} ; Origem: {self.nodo_origem} ; Destino: {self.nodo_destino} ; Oneway: {self.oneway} ; Highway: {list_str}"
