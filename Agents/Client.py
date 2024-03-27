import random
from spade import agent
from Behaviours.ReceiveProcessingMessage import ReceiveProcessingMessage_Behav
from Behaviours.Purchase import Purchase_Behav
from Classes.Position import Position

class ClientAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        self.position = Position(random.randint(1, 100), random.randint(1, 100))
        self.productsBought = {}

        self.productsAvailable = ['Apple', 'Banana', 'Grapefruit', 'Orange', 'Pear', 'Melon', 'Strawberry'] 
        # self.products = [Product('Apple', 10), Product('Banana', 20), Product('Grapefruit', 15), Product('Orange', 12), Product('Pear', 8), Product('Melon', 5), Product('Strawberry', 25)]
        a = Purchase_Behav()
        b = ReceiveProcessingMessage_Behav()
        
        self.add_behaviour(a)
        self.add_behaviour(b)