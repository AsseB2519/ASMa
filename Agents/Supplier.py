from spade import agent
import config

from Behaviours.TransportSupply import TransportSupply_Behav
from Classes.Position import Position

class SupplierAgent(agent.Agent):
    # def __init__(self, jid, password, app_instance):
        # super().__init__(jid, password)
        # self.app = app_instance

    async def setup(self):
        # self.app.print_to_gui(f"Agent {str(self.jid)} starting...")
        # print("Agent {}".format(str(self.jid)) + " starting...")

        self.position = Position(int(config.WAREHOUSE_X), int(config.WAREHOUSE_Y), int(config.WAREHOUSE))

        a = TransportSupply_Behav()
        self.add_behaviour(a)