from spade import agent
from Behaviours.ProcessingStock import ProcessingStock_Behav
from Classes.Product import Product

class StockManagerAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        
        self.products = {
            'Apple': Product('Apple', 20, 1.50),
            'Banana': Product('Banana', 20, 0.80),
            'Grapefruit': Product('Grapefruit', 20, 2.00),
            'Orange': Product('Orange', 20, 1.20),
            'Pear': Product('Pear', 20, 1.80),
            'Melon': Product('Melon', 20, 3.50),
            'Strawberry': Product('Strawberry', 20, 2.50)
        }
        
        a = ProcessingStock_Behav()
        self.add_behaviour(a)
