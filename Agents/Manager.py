from spade import agent
from Behaviours.Processing import Processing_Behav

class ManagerAgent(agent.Agent):

    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        self.productsAvailable = ['Apple', 'Banana', 'Grapefruit', 'Orange', 'Pear', 'Melon', 'Strawberry']

        a = Processing_Behav()
        self.add_behaviour(a)