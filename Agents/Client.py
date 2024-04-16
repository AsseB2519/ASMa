import random
from spade import agent
from Behaviours.ReceiveStockAndPurchase import ReceiveStockAndPurchase_Behav
from Behaviours.RequestProducts import RequestProducts_Behav
from Classes.Position import Position

class ClientAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        self.position = Position(random.randint(1, 100), random.randint(1, 100))

        self.productsBought = {}

        a = RequestProducts_Behav() 
        self.add_behaviour(a)
        b = ReceiveStockAndPurchase_Behav()
        self.add_behaviour(b)





















        self.add_behaviour(a)
