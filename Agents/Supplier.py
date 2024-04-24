import random
from spade import agent
from Behaviours.ReceiveStockAndPurchase import ReceiveStockAndPurchase_Behav
from Behaviours.RequestProducts import RequestProducts_Behav
from Behaviours.Return import Return_Behav
from Classes.Position import Position

class SupplierAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")