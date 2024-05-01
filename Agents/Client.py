import random
from spade import agent
from Behaviours.ReceiveStockAndPurchase import ReceiveStockAndPurchase_Behav
from Behaviours.RequestProducts import RequestProducts_Behav
from Behaviours.Return import Return_Behav
from Classes.Position import Position

class ClientAgent(agent.Agent):

    # def __init__(self, jid, password, gui):
        # super().__init__(jid, password)
        # self.gui = gui

    def set_gui(self, gui):
        self.gui = gui

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        # self.gui.update_log(f"Agent {str(self.jid)} starting...")
 # self.gui.add_client()
        
        self.position = Position(random.randint(1, 100), random.randint(1, 100), 1434791917)

        self.productsBought = {}
        self.productsBought_notDelivered = []

        a = RequestProducts_Behav(period=10)
        self.add_behaviour(a)
        b = ReceiveStockAndPurchase_Behav()
        self.add_behaviour(b)
        c = Return_Behav(period=30)
        self.add_behaviour(c)

