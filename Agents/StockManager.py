from spade import agent
from Behaviours.ProcessingStock import StockProcessing_Behav
from Classes.Product import Product

class StockManagerAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        self.products = {
                'Apple': 20,
                'Banana': 20,
                'Grapefruit': 20,
                'Orange': 20,
                'Pear': 20,
                'Melon': 20,
                'Strawberry': 20
            }
        a = StockProcessing_Behav()
        self.add_behaviour(a)
