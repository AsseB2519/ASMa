from spade import agent
import config

from Behaviours.TransportSupply import TransportSupply_Behav
from Classes.Position import Position

class SupplierAgent(agent.Agent):
    async def setup(self):
        # print("Agent {}".format(str(self.jid)) + " starting...")

        self.position = Position(int(config.WAREHOUSE_X), int(config.WAREHOUSE_Y))

        a = TransportSupply_Behav()
        self.add_behaviour(a)