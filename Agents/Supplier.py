from spade import agent

from Behaviours.TransportSupply import TransportSupply_Behav

class SupplierAgent(agent.Agent):
    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        a = TransportSupply_Behav()
        self.add_behaviour(a)