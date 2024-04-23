import random 
from spade import agent

from Behaviours.Register import Register_Behav
from Behaviours.Transport import Transport_Behav
from Classes.Position import Position

class DeliverymanAgent(agent.Agent):

    available = True

    async def setup(self):
        self.position = Position(random.randint(1, 100), random.randint(1, 100))
        
        print("Agent {}".format(str(self.jid)) + " starting...")

        a = Register_Behav()
        self.add_behaviour(a)
        b = Transport_Behav()
        self.add_behaviour(b)
        