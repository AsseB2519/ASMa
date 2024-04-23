from spade import agent

from Behaviours.Register import Register_Behav
from Behaviours.Transport import Transport_Behav

class DeliverymanAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")

        a = Register_Behav()
        self.add_behaviour(a)
        b = Transport_Behav()
        self.add_behaviour(b)
        