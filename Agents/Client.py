import random
import datetime
import re
from spade import agent
from Behaviours.ReceiveStockAndPurchase import ReceiveStockAndPurchase_Behav
from Behaviours.RequestProducts import RequestProducts_Behav
from Behaviours.Return import Return_Behav
from Classes.Position import Position

class ClientAgent(agent.Agent):

    async def setup(self):
        # print("Agent {}".format(str(self.jid)) + " starting...")
        
        self.position = Position(random.randint(1, 100), random.randint(1, 100), 1434791917)

        self.productsBought = {}
        self.productsBought_notDelivered = []

        match = re.search(r"client(\d+)", str(self.jid))
        if match:
            x = int(match.group(1))
        else:
            print("No number found in the JID")

        start_at = datetime.datetime.now() + datetime.timedelta(seconds=x)
        a = RequestProducts_Behav(start_at=start_at)
        self.add_behaviour(a)
        # a = RequestProducts_Behav(period=10)
        # self.add_behaviour(a)
        b = ReceiveStockAndPurchase_Behav()
        self.add_behaviour(b)
        c = Return_Behav(period=30)
        self.add_behaviour(c)

