from spade import agent
from Behaviours.ProcessingStock import ProcessingStock_Behav

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
        
        a = ProcessingStock_Behav()
        self.add_behaviour(a)
