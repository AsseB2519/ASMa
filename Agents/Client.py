import random
from spade import agent
from Behaviours.ReceiveProcessingMessage import ReceiveProcessingMessage_Behav
from Behaviours.Purchase import Purchase_Behav
from Behaviours.RequestProducts import RequestProducts_Behav
from spade.behaviour import OneShotBehaviour
from Classes.Position import Position

class ClientAgent(agent.Agent):
    class WaitingBehav(OneShotBehaviour):
        async def run(self):
            await self.agent.c.join() 
            print("Waiting Behaviour has finished")

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        self.position = Position(random.randint(1, 100), random.randint(1, 100))
        self.productsBought = {}

        # self.productsAvailable = []
        self.productsAvailable = ['Apple', 'Banana', 'Grapefruit', 'Orange', 'Pear', 'Melon', 'Strawberry']

        a = RequestProducts_Behav()        
        d = self.WaitingBehav()
        self.c = ReceiveProcessingMessage_Behav()
        b = Purchase_Behav()
    
        self.add_behaviour(a)
        self.add_behaviour(self.c)
        self.add_behaviour(d)
        self.add_behaviour(b)
        self.add_behaviour(self.c)
